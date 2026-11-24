import socket
from juego import jugar

# Dirección IP del servidor (127.0.0.1 si ambos programas se ejecutan en el mismo ordenador)
HOST = "127.0.0.1"
PUERTO = 50505


def main():
    try:
        # Creamos el socket TCP (IPv4 + flujo TCP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            # Iniciamos la conexión contra el servidor
            cliente.connect((HOST, PUERTO))
            print(f"Conectado al servidor en {HOST}:{PUERTO}")

            # Arrancamos el juego indicando que el cliente espera el primer turno
            jugar(cliente, empieza=False)

    except (OSError, ConnectionError, ValueError) as error:
        print(f"Error de conexión o de partida: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nPartida interrumpida.")


# Ejecuta main() solo si lanzamos este archivo directamente
if __name__ == "__main__":
    main()
