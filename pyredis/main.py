import asyncio
from pyredis.server.threaded_server import threaded_server
from pyredis.server.async_server import PyRedisAsyncServerProtocol
from pyredis.datastore import DataStore

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 6380


async def async_main(host, port, datastore):
    loop = asyncio.get_running_loop()
    instance_of_server = await loop.create_server(
        lambda: PyRedisAsyncServerProtocol(datastore),
        host,
        port,
    )
    async with instance_of_server:
        await instance_of_server.serve_forever()


def main(host: str = None, port: int = None, threaded: bool = False):
    if host is None:
        host = DEFAULT_HOST
    if port is None:
        port = DEFAULT_PORT
    else:
        port = int(port)

    print("Initialize DataStore")
    datastore = DataStore()
    print(f"Start PyRedis on host: {host}, port: {port}")

    if threaded:
        print("Run Threaded Server")
        threaded_server(host, port, datastore)
    else:
        print("Run Async Server")
        asyncio.run(async_main(host, port, datastore))

    return 0
