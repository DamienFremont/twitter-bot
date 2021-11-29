import os
import logging
import log
import config
from twitterbot.config import create_api
from twitterbot.followfile import follow_file
from twitterbot.tweetfile import tweet_file_random
from twitterbot.tweetfile import tweet_file
import os

logger = logging.getLogger('twitterbot')
log.initLogger(logger, appname='twitterbot', modulename='test')


def run():
    logger.info("")
    logger.info("*****************")
    logger.info("* Test          *")
    logger.info("*****************")
    logger.info("")
    config.init()
    account = 'EuropaColonyGG'
    logger.info(f"Account @{account}")
    config.switch(account)
    api = create_api()
    # TO TEST:
    max = os.getenv("TWITTER_FEATURES_FOLLOWFILE_MAX", 9)
    pathname = os.getenv("TWITTER_FEATURES_FOLLOWFILE_PATHNAME")
    follow_file(api, pathname = pathname, max = max)


def main():
    run()


if __name__ == "__main__":
    main()
