import asyncio
import logging
from pyredis.server import ThreadedServer, PyRedisAsyncServerProtocol
from pyredis.datastore import LockDataStore, QueueDataStore
from pyredis.persistor import Persistor

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 6380


async def async_main(host, port, datastore, persistor):
    loop = asyncio.get_running_loop()
    instance_of_server = await loop.create_server(
        lambda: PyRedisAsyncServerProtocol(datastore, persistor),
        host,
        port,
    )
    async with instance_of_server:
        await instance_of_server.serve_forever()


def main(
    host: str = None,
    port: int = None,
    threaded: bool = False,
    locked: bool = False,
    persistance: bool = True,
    datastore=None,
    persistor_filepath=None,
):
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="/tmp/pyredis.log", format="%(asctime)s: %(levelname)s: %(name)s: %(message)s", level=logging.INFO
    )

    if host is None:
        host = DEFAULT_HOST
    if port is None:
        port = DEFAULT_PORT
    else:
        port = int(port)

    if datastore is None:
        if locked:
            logger.info("Initialize LockedDataStore")
            datastore = LockDataStore()
        else:
            logger.info("Initialize QueueDataStore")
            datastore = QueueDataStore()

    persistor = None
    if persistance:
        persistor = Persistor(datastore, persistor_filepath)
        persistor.read()

    logger.info(f"Start PyRedis on host: {host}, port: {port}")

    if threaded:
        logger.info("Run Threaded Server")
        tserver = ThreadedServer(host, port, datastore, persistor)
        tserver.threaded_server()
    else:
        logger.info("Run Async Server")
        asyncio.run(async_main(host, port, datastore, persistor))

    return 0
