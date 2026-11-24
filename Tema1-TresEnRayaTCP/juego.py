# Constante para el tamaño fijo del tablero
TAMANO = 3


def crear_tablero():
    """Devuelve una matriz de 3x3 rellena con '.' para indicar casillas vacías."""
    """Se usa el _ como si fuera la i del bucle pero como no vamos a usar el número de la iteración se usa el _"""
    # La parte interior             la parte exterior
    return [["." for _ in range(TAMANO)] for _ in range(TAMANO)]


def mostrar_tablero(tablero):
    """Dibuja el tablero en consola con filas y columnas numeradas del 1 al 3."""
    # Encabezado con los números de columna
    print("\n    1 2 3")
    # Recorre cada fila numerándola desde 1 hasta 3
    for num_fila, fila in enumerate(tablero, start=1):
        # Une los elementos de la fila separados por un espacio
        print(f"{num_fila}   " + " ".join(fila))
    print()


def jugada_valida(tablero, fila, columna):
    """Comprueba que la fila y columna estén entre 1 y 3 y que la casilla esté libre."""
    # Verifica que no se salga de los límites del tablero
    if fila < 1 or fila > TAMANO or columna < 1 or columna > TAMANO:
        return False
    # Restamos 1 porque en Python las listas empiezan en el índice 0
    return tablero[fila - 1][columna - 1] == "."


def colocar_ficha(tablero, fila, columna, simbolo):
    """Guarda la ficha ('X' u 'O') en la posición indicada del tablero."""
    tablero[fila - 1][columna - 1] = simbolo


def comprobar_ganador(tablero):
    """Devuelve 'X' o 'O' si hay tres en raya; devuelve None si nadie ha ganado aún."""
    # 1. Comprobar las 3 filas (victoria horizontal)
    for fila in tablero:
        if fila[0] != "." and fila[0] == fila[1] == fila[2]:
            return fila[0]

    # 2. Comprobar las 3 columnas (victoria vertical)
    for col in range(TAMANO):
        if (
            tablero[0][col] != "."
            and tablero[0][col] == tablero[1][col] == tablero[2][col]
        ):
            return tablero[0][col]

    # 3. Comprobar diagonal principal (arriba-izquierda a abajo-derecha)
    if tablero[0][0] != "." and tablero[0][0] == tablero[1][1] == tablero[2][2]:
        return tablero[0][0]

    # 4. Comprobar diagonal secundaria (arriba-derecha a abajo-izquierda)
    if tablero[0][2] != "." and tablero[0][2] == tablero[1][1] == tablero[2][0]:
        return tablero[0][2]

    # Si no se cumple ninguna línea de 3, todavía no hay ganador
    return None


def tablero_lleno(tablero):
    """Devuelve True si no queda ninguna casilla vacía ('.'), lo que indica empate."""
    for fila in tablero:
        if "." in fila:
            return False
    return True


def enviar_mensaje(conexion, mensaje):
    """Envía un texto terminado en salto de línea ('\\n') a través del socket TCP."""
    # TCP envía bytes, por eso codificamos el texto en UTF-8
    datos = (mensaje + "\n").encode("utf-8")
    conexion.sendall(datos)


def recibir_mensaje(conexion):
    """Lee byte a byte del socket TCP hasta encontrar el salto de línea ('\\n')."""
    datos = bytearray()
    while True:
        # Leemos de 1 en 1 byte para no mezclar mensajes consecutivos
        fragmento = conexion.recv(1)
        # Si recv() devuelve vacío, el rival cerró la conexión
        if not fragmento:
            raise ConnectionError("El otro jugador se ha desconectado.")
        # Al llegar al '\n', el mensaje está completo y salimos del bucle
        if fragmento == b"\n":
            break
        datos.extend(fragmento)
        # Límite de seguridad para evitar mensajes anormalmente largos
        if len(datos) > 64:
            raise ValueError("Mensaje recibido demasiado largo.")
    # Convertimos los bytes acumulados de vuelta a texto
    return datos.decode("utf-8")


def pedir_jugada(tablero, simbolo):
    """Pide fila y columna por teclado hasta que el usuario elija una casilla válida."""
    while True:
        try:
            fila = int(input(f"[{simbolo}] Introduce fila (1-3): "))
            columna = int(input(f"[{simbolo}] Introduce columna (1-3): "))

            # Si está entre 1 y 3 y no está ocupada, devolvemos las coordenadas
            if jugada_valida(tablero, fila, columna):
                return fila, columna

            print("Casilla ocupada o fuera de rango (1-3). Prueba otra vez.")
        except ValueError:
            # Evita que el programa falle si el usuario pulsa Enter vacío o escribe letras
            print("Entrada no válida. Escribe números enteros del 1 al 3.")


def jugar(conexion, empieza):
    """Coordina los turnos entre servidor (empieza=True) y cliente (empieza=False)."""
    tablero = crear_tablero()

    # El servidor juega con 'X' y comienza; el cliente juega con 'O' y espera
    mi_simbolo = "X" if empieza else "O"
    rival_simbolo = "O" if empieza else "X"
    mi_turno = empieza
    partida_terminada = False

    print(f"Partida iniciada. Juegas con '{mi_simbolo}'.")
    mostrar_tablero(tablero)

    # Bucle que alterna turnos hasta que haya ganador o empate
    while not partida_terminada:
        if mi_turno:
            # --- TURNO PROPIO ---
            fila, columna = pedir_jugada(tablero, mi_simbolo)
            colocar_ficha(tablero, fila, columna, mi_simbolo)
            mostrar_tablero(tablero)

            # Enviamos la jugada al rival con el formato: JUGADA|fila|columna
            enviar_mensaje(conexion, f"JUGADA|{fila}|{columna}")
        else:
            # --- TURNO DEL RIVAL ---
            print(f"Esperando movimiento de '{rival_simbolo}'...")
            mensaje = recibir_mensaje(conexion)

            # Separamos el mensaje recibido por '|' -> ['JUGADA', 'fila', 'columna']
            partes = mensaje.strip().split("|")
            if len(partes) != 3 or partes[0] != "JUGADA":
                raise ValueError(f"Formato de mensaje incorrecto: {mensaje}")

            fila = int(partes[1])
            columna = int(partes[2])

            # Verificamos la jugada recibida y actualizamos nuestra copia del tablero
            if not jugada_valida(tablero, fila, columna):
                raise ValueError(
                    f"El rival envió una casilla inválida: ({fila}, {columna})"
                )

            colocar_ficha(tablero, fila, columna, rival_simbolo)
            print(f"El rival ({rival_simbolo}) jugó en fila {fila}, columna {columna}.")
            mostrar_tablero(tablero)

        # --- COMPROBAR SI LA PARTIDA HA TERMINADO ---
        # Ambos programas hacen esta comprobación tras cada jugada para salir a la vez
        ganador = comprobar_ganador(tablero)
        if ganador is not None:
            if ganador == mi_simbolo:
                print("¡Enhorabuena! Has ganado la partida.")
            else:
                print(f"Has perdido. El ganador es '{ganador}'.")
            partida_terminada = True
        elif tablero_lleno(tablero):
            print("¡Empate! El tablero está lleno.")
            partida_terminada = True
        else:
            # Si la partida sigue, pasamos el turno al otro jugador
            mi_turno = not mi_turno
