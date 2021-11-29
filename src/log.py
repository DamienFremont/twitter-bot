import logging
import datetime

logger = logging.getLogger('twitterbot')


def initLogger(logger, appname = "twitterbot", modulename = "twitter"):

    LOGGER_PREFIX = f"[{appname}] {modulename} : "
    DATE_FMT = "%Y%m%d_%H%M%S"
    now = datetime.datetime.now()

    file_log_handler = logging.FileHandler(f"logs/{appname}-{now.strftime(DATE_FMT)}.log")
    logger.addHandler(file_log_handler)

    stderr_log_handler = logging.StreamHandler()
    logger.addHandler(stderr_log_handler)

    # nice output format
    formatter = logging.Formatter(f'%(asctime)s %(levelname)s {LOGGER_PREFIX} %(message)s')
    file_log_handler.setFormatter(formatter)
    stderr_log_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)

    return logger
