import os
import logging, log
import config
import twitterbot

# STATIC **********************************************************************

logger = logging.getLogger('twitterbot')
log.initLogger(logger, appname='twitterbot', modulename='test')

# PUBLIC **********************************************************************

# PRIVATE *********************************************************************

def test():
    logger.info("Twitter Bot : Test")
    config.init()
    account = 'FremontGames'
    logger.info(f"Account @{account}")
    config.switch(account)
    api = twitterbot.initapi()
    # TO TEST:
    #
    # max = int(os.getenv("TWITTER_FEATURES_FOLLOWFILE_MAX", 9))
    # pathname = os.getenv("TWITTER_FEATURES_FOLLOWFILE_PATHNAME")
    # twitterbot.followfile(api, pathname = pathname, max = max)
    #
    
# SCRIPT **********************************************************************

def main():
    test()

if __name__ == "__main__":
    main()
