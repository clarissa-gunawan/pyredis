import socket
from pyredis.commands import parse_command
from threading import Thread
import asyncio

# This is a Well Known Port assigned for Echo Protocol
# https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Well-known_ports

# The Echo Protocol is formally defined in RFC862
# https://datatracker.ietf.org/doc/html/rfc862/
PORT = 6380
HOST = ""
BUFFER_SIZE = 4096


def handle_connection(client_socket):
    remaining_message = b""
    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE)

            if not message:
                break

            message = remaining_message + message

            while True:
                value, size = parse_command(message)

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


def server():
    # the family and type default to AF_INET (Internet Addresses - Hostname or IP address)
    # and SOCK_STREAM (TCP)
    print("Initializing Server")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse address
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        while True:
            print("Waiting to accept a connection")
            try:
                client_socket, address = server_socket.accept()
                print(f"Accepting connection from: {address}")
                Thread(target=handle_connection, args=(client_socket,), daemon=True).start()
            except KeyboardInterrupt:
                print("Shutting down server")
                return

async def async_main():
    loop = asyncio.get_running_loop()
    instance_of_server = await loop.create_server(
        lambda: server()
    )
    async with instance_of_server:
        await instance_of_server.serve_forever()


if __name__ == "__main__":
    use_async = True
    if use_async:
        print("RUN with Async")
        async_main()
    else:
        print("RUN with Threading")
        Thread(target=server, daemon=True).start()
