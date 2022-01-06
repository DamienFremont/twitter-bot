import os
import logging, log
import config
import twitterbot

logger = logging.getLogger('twitterbot')
log.initLogger(logger, appname='twitterbot', modulename='test')

def run():
    logger.info("")
    logger.info("*****************")
    logger.info("* Test          *")
    logger.info("*****************")
    logger.info("")
    config.init()
    account = 'DFremontGameDev'
    logger.info(f"Account @{account}")
    config.switch(account)
    api = twitterbot.initapi()
    # TO TEST:
    #
    # max = int(os.getenv("TWITTER_FEATURES_FOLLOWFILE_MAX", 9))
    # pathname = os.getenv("TWITTER_FEATURES_FOLLOWFILE_PATHNAME")
    # twitterbot.followfile(api, pathname = pathname, max = max)
    #

def main():
    run()

if __name__ == "__main__":
    main()
