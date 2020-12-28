import os
import logging
import datetime
from twitterbot import main

APP_NAME = "app"

LOGGER_PREFIX = f"[{APP_NAME}] bots : "
DATE_FMT = "%Y%m%d_%H%M%S"
now = datetime.datetime.now()

logger = logging.getLogger(APP_NAME)

file_log_handler = logging.FileHandler(f"{APP_NAME}-{now.strftime(DATE_FMT)}.log")
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

# nice output format
formatter = logging.Formatter(f'%(asctime)s %(levelname)s {LOGGER_PREFIX} %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)

def run():
    logger.info("")
    logger.info("***************************")
    logger.info("* Community Manager Bots  *")
    logger.info("***************************")
    logger.info("")
    main.main()

if __name__ == "__main__":
    run()
