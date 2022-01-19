import os
import logging, log
import config
import twitterbot

# STATIC **********************************************************************

logger = logging.getLogger('twitterbot')
log.initLogger(logger, appname='twitterbot', modulename='init')

# PUBLIC **********************************************************************

# PRIVATE *********************************************************************

def install():
    logger.info("Twitter Bot : Install")
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
            twitterbot.initfile(api, screen_name, file_name)
            logger.info(" ")

# SCRIPT **********************************************************************

def main():
    install()

if __name__ == "__main__":
    main()
