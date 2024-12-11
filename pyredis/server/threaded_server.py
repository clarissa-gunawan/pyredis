import socket
from pyredis.commands import parse_command
from threading import Thread

# This is a Well Known Port assigned for Echo Protocol
# https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Well-known_ports

# The Echo Protocol is formally defined in RFC862
# https://datatracker.ietf.org/doc/html/rfc862/

BUFFER_SIZE = 4096


def handle_connection(client_socket, datastore):
    remaining_message = b""
    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE)

            if not message:
                break

            message = remaining_message + message

            while True:
                value, size = parse_command(message, datastore)

                if value is None:
                    break

                client_socket.send(value)

                # Remove processed messages
                remaining_message = message[size:]
                message = remaining_message

    except ConnectionResetError:
        print("Client disconnected")
        return
    finally:
        client_socket.close()


def threaded_server(host, port, datastore):
    # the family and type default to AF_INET (Internet Addresses - Hostname or IP address)
    # and SOCK_STREAM (TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse address
        server_socket.bind((host, port))
        server_socket.listen()

        while True:
            print("Waiting to accept a connection")
            try:
                client_socket, address = server_socket.accept()
                print(f"Accepting connection from: {address}")
                Thread(target=handle_connection, args=(client_socket, datastore), daemon=True).start()
            except KeyboardInterrupt:
                print("Shutting down server")
                return
