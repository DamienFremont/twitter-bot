import logging
import datetime
import os

# STATIC **********************************************************************

logger = logging.getLogger('twitterbot')

# PUBLIC **********************************************************************

def initLogger(logger, appname = "twitterbot", modulename = "twitter"):
    # CONST
    LOGGER_PREFIX = f"[{appname}] {modulename} : "
    DATE_FMT = "%Y%m%d_%H%M%S"
    now = datetime.datetime.now()
    # FILE
    file_log_handler = logging.FileHandler(f"{appname}-{now.strftime(DATE_FMT)}.log")
    logger.addHandler(file_log_handler)
    # STD
    stderr_log_handler = logging.StreamHandler()
    logger.addHandler(stderr_log_handler)
    # nice output format
    formatter = logging.Formatter(f'%(asctime)s %(levelname)s {LOGGER_PREFIX} %(message)s')
    file_log_handler.setFormatter(formatter)
    stderr_log_handler.setFormatter(formatter)
    # SET
    logger.setLevel(logging.INFO)
    return logger
