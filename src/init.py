import os
import logging
import config
import log
from twitterbot.config import create_api
from twitterbot.followfile import init_files
from twitterbot.followfile import follow_file_write


logger = logging.getLogger('twitterbot')
log.initLogger(logger, appname='twitterbot', modulename='init')


def run():
    logger.info("")
    logger.info("*****************")
    logger.info("* Init          *")
    logger.info("*****************")
    logger.info("")
    config.init()
    accounts = os.getenv("TWITTER_ACCOUNTS").split(',')
    for account in accounts:
        logger.info(f"Account @{account}")
        config.switch(account)
        features = os.getenv("TWITTER_INIT_FEATURES").split(',')
        if features == ['']:
            continue
        api = create_api()
        logger.info(f"Features {features}")
        if 'followfile' in features:
            screen_name = os.getenv("TWITTER_INIT_FEATURES_FOLLOWFILE_USER")
            file_name = os.getenv("TWITTER_INIT_FEATURES_FOLLOWFILE_PATHNAME")
            logger.info(screen_name)
            follow_file_write(api, screen_name, file_name)
            logger.info(f" ")


def main():
    run()


if __name__ == "__main__":
    main()
