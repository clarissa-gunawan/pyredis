import asyncio
from pyredis.commands import parse_command


class PyRedisAsyncServerProtocol(asyncio.Protocol):
    def __init__(self, datastore, persistor):
        self.transport = None
        self.remaining_data = b""
        self.datastore = datastore
        self.persistor = persistor

    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        print("Connection from {}".format(peername))
        self.transport = transport

    def data_received(self, data):
        if not data:
            self.transport.close()

        data = data + self.remaining_data

        while True:
            processed_data, size = parse_command(data, self.datastore, self.persistor)

            if processed_data is None:
                break

            # print("Send: {!r}".format(data.decode()))
            self.transport.write(processed_data)

            self.remaining_data = data[size:]
            data = self.remaining_data
