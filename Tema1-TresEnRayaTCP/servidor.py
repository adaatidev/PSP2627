import socket
from juego import jugar

# 0.0.0.0 permite aceptar conexiones tanto locales (127.0.0.1) como desde otros PCs de la red
HOST = "0.0.0.0"
PUERTO = 50505


def main():
    try:
        # Creamos el socket TCP (AF_INET = IPv4, SOCK_STREAM = protocolo TCP)
        # El bloque 'with' cierra el socket automáticamente al terminar
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            # Permite reutilizar rápidamente el puerto si reinicias el servidor
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Asociamos el socket a la dirección IP y puerto
            servidor.bind((HOST, PUERTO))

            # Ponemos el servidor a escuchar (cola de 1 conexión pendiente)
            servidor.listen(1)
            print(f"Servidor (X). Esperando rival en el puerto {PUERTO}...")

            # accept() detiene el programa hasta que un cliente se conecte
            # Devuelve un nuevo socket ('conexion') para hablar con ese cliente
            conexion, direccion = servidor.accept()

            with conexion:
                print(f"Cliente (O) conectado desde {direccion[0]}")
                # Arrancamos el juego indicando que el servidor empieza
                jugar(conexion, empieza=True)

    except (OSError, ConnectionError, ValueError) as error:
        print(f"Error de conexión o de partida: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nPartida interrumpida.")


# Ejecuta main() solo si lanzamos este archivo directamente
if __name__ == "__main__":
    main()
