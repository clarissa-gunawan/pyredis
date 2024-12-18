import logging
import socket
from threading import Thread
from pyredis.commands import parse_command

# This is a Well Known Port assigned for Echo Protocol
# https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Well-known_ports

# The Echo Protocol is formally defined in RFC862
# https://datatracker.ietf.org/doc/html/rfc862/

BUFFER_SIZE = 4096


class ThreadedServer:
    def __init__(self, host, port, datastore, persistor):
        self._logger = logging.getLogger(__name__)
        self._host = host
        self._port = port
        self._datastore = datastore
        self._persistor = persistor
        self._is_running = True

    def handle_connection(self, client_socket, datastore, persistor):
        remaining_message = b""
        try:
            while True:
                message = client_socket.recv(BUFFER_SIZE)

                if not message:
                    break

                message = remaining_message + message

                while True:
                    value, size = parse_command(message, datastore, persistor)

                    if value is None:
                        break

                    client_socket.send(value)

                    # Remove processed messages
                    remaining_message = message[size:]
                    message = remaining_message

        except ConnectionResetError:
            self._logger.info("Client disconnected")
            return
        finally:
            client_socket.close()

    def start(self):
        # the family and type default to AF_INET (Internet Addresses - Hostname or IP address)
        # and SOCK_STREAM (TCP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Avoid bind() exception: OSError: [Errno 48] Address already in use
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self._host, self._port))
            server_socket.listen()

            while self._is_running:
                self._logger.info("Waiting to accept a connection")
                try:
                    client_socket, address = server_socket.accept()
                    self._logger.info(f"Accepting connection from: {address}")
                    Thread(
                        target=self.handle_connection, args=(client_socket, self._datastore, self._persistor), daemon=True
                    ).start()
                except KeyboardInterrupt:
                    self._logger.info("Shutting down server")
                    return

    def stop(self):
        self._is_running = False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(self._host, self._port)
