import asyncio
import typer
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


def configure_logging(log="WARNING", verbose=False, quiet=False):
    if quiet:
        log_level = logging.ERROR  # Set logging to only show errors and critical issues
    elif verbose > 0:
        # Increase verbosity based on --verbose (-v)
        log_level = max(logging.DEBUG, logging.WARNING - 10)
    else:
        log_level = getattr(logging, log.upper(), logging.WARNING)  # Set logging level based on --log argument

    logging.basicConfig(
        filename="/tmp/pyredis.log", format="%(asctime)s: %(levelname)s: %(name)s: %(message)s", level=log_level
    )


def main(
    host: str = None,
    port: int = None,
    threaded: bool = False,
    locked: bool = False,
    persistance: bool = True,
    datastore=None,
    persistor_filepath=None,
    log: str = typer.Option("WARNING", "--log", "-l"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
):
    configure_logging(log, verbose, quiet)
    logger = logging.getLogger(__name__)

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
