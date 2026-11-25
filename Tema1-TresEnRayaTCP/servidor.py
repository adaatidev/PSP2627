"""Jugador 1: servidor TCP. Ejecutar primero."""

import socket
from juego import jugar

# Se le pone el host 0.0.0.0 porque permite aceptar conexiones tanto locales (127.0.0.1) como desde otros PCs de la red
HOST = "0.0.0.0"
PUERTO = 50505


def main():
    try:
        # Crea el socket TCP (AF_INET = IPv4, SOCK_STREAM = protocolo TCP)
        # El bloque 'with' cierra el socket automáticamente al terminar
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            # Permite reutilizar rápidamente el puerto si se reinicia el servidor
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Se asocia el socket a la dirección IP y puerto
            servidor.bind((HOST, PUERTO))

            # Pone el servidor en escucha (cola de 1 conexión pendiente)
            servidor.listen(1)
            # Mensaje por consola para informar al usuario que el se espera al otro jugador
            print(f"Servidor (X). Esperando rival en el puerto {PUERTO}...")

            # accept() detiene el programa hasta que el cliente se conecte
            # Devuelve un nuevo socket ('conexion') para hablar con ese cliente
            conexion, direccion = servidor.accept()

            # Con el nuevo socket creado
            with conexion:
                # Mensaje por consola para informar que ya se ha conectado el segundo jugador y su dirección
                print(f"Cliente (O) conectado desde {direccion[0]}")
                # Arranca el juego indicando que el servidor empieza
                jugar(conexion, empieza=True)

    # Manejo de excepciones si hay error de conexión o si se interrumpe
    except (OSError, ConnectionError, ValueError) as error:
        print(f"Error de conexión o de partida: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nPartida interrumpida.")


# Ejecuta main() solo si se lanza este archivo directamente
if __name__ == "__main__":
    main()
