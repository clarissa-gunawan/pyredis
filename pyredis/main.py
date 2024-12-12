import asyncio
from pyredis.server import threaded_server, PyRedisAsyncServerProtocol
from pyredis.datastore import LockDataStore, QueueDataStore

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


def main(host: str = None, port: int = None, threaded: bool = False, locked: bool = False, datastore=None):
    if host is None:
        host = DEFAULT_HOST
    if port is None:
        port = DEFAULT_PORT
    else:
        port = int(port)

    if datastore is None:
        if locked:
            print("Initialize LockedDataStore")
            datastore = LockDataStore()
        else:
            print("Initialize QueueDataStore")
            datastore = QueueDataStore()

    print(f"Start PyRedis on host: {host}, port: {port}")

    if threaded:
        print("Run Threaded Server")
        threaded_server(host, port, datastore)
    else:
        print("Run Async Server")
        asyncio.run(async_main(host, port, datastore))

    return 0
