import random
import time

from structlog import get_logger

logger = get_logger()


def say_hello(name):
    logger.info(f"Say Hello World to {name}")
    time.sleep(5)
    if random.random() > 0.99:
        logger.error('Throw random error', cause='whatever')
        raise Exception("Random Exception")
    logger.info(f"Said Hello World to {name}")
    return f"Hello {name}"
