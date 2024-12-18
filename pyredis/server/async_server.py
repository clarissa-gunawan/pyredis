import asyncio
import logging
from pyredis.commands import parse_command


class PyRedisAsyncServerProtocol(asyncio.Protocol):
    def __init__(self, datastore, persistor):
        self._logger = logging.getLogger(__name__)
        self.transport = None
        self.remaining_data = b""
        self.datastore = datastore
        self.persistor = persistor

    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        self._logger.info("Connection from {}".format(peername))
        self.transport = transport

    def data_received(self, data):
        if not data:
            self.transport.close()

        data = data + self.remaining_data

        while True:
            processed_data, size = parse_command(data, self.datastore, self.persistor)

            if processed_data is None:
                break

            self._logger.info("Send: {!r}".format(data.decode()))
            self.transport.write(processed_data)

            self.remaining_data = data[size:]
            data = self.remaining_data


class AsyncServer:
    def __init__(self, host, port, datastore, persistor):
        self._logger = logging.getLogger(__name__)
        self._host = host
        self._port = port
        self._datastore = datastore
        self._persistor = persistor
        self._server = None
        self._loop = None

    async def stop(self):
        await self._server.close()

    async def start(self):
        self._loop = asyncio.get_running_loop()
        self._server = await self._loop.create_server(
            lambda: PyRedisAsyncServerProtocol(self._datastore, self._persistor),
            self._host,
            self._port,
        )

        async with self._server:
            await self._server.serve_forever()
