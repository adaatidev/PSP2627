"""Jugador 2: cliente TCP. Cambiar HOST para jugar en otro equipo."""

import socket
from juego import jugar

# Dirección IP del servidor (127.0.0.1 si ambos programas se ejecutan en el mismo ordenador, se cambia si el servidor está en otro PC de la red)
HOST = "127.0.0.1"
PUERTO = 50505


def main():
    try:
        # Crea el socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            # Inicia la conexión contra el servidor
            cliente.connect((HOST, PUERTO))
            # Mensaje por consola para mostrar que está conectado al servidor con su host y su puerto
            print(f"Conectado al servidor en {HOST}:{PUERTO}")

            # Arranca el juego indicando que el cliente espera el primer turno (el del servidor)
            jugar(cliente, empieza=False)

    # Manejo de excepciones si hay error de conexión o si se interrumpe
    except (OSError, ConnectionError, ValueError) as error:
        print(f"Error de conexión o de partida: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nPartida interrumpida.")


# Ejecuta main() solo si se lanza este archivo directamente
if __name__ == "__main__":
    main()
