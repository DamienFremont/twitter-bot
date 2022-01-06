import os
import logging, log
import config
import twitterbot

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
        api = twitterbot.initapi()
        logger.info(f"Features {features}")
        if 'followfile' in features:
            screen_name = os.getenv("TWITTER_INIT_FEATURES_FOLLOWFILE_USER")
            file_name = os.getenv("TWITTER_INIT_FEATURES_FOLLOWFILE_PATHNAME")
            logger.info(screen_name)
            twitterbot.writefollowfile(api, screen_name, file_name)
            logger.info(" ")

def main():
    run()

if __name__ == "__main__":
    main()
