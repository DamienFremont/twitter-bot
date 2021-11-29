import os
import logging
import log
import datetime
import config
from twitterbot.config import create_api
from twitterbot.followfile import follow_file
from twitterbot.followfile import init_files
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
    account = 'Cars2048'
    logger.info(f"Account @{account}")
    config.switch(account)
    api = create_api()
    # 
    # follow_file(api, 21)
    # 
    max = os.getenv("TWITTER_FEATURES_FOLLOWFILE_MAX", 9)
    pathname = os.getenv("TWITTER_FEATURES_FOLLOWFILE_PATHNAME")
    follow_file(api, pathname = pathname, max = max)
    # 
    # tweet_file(api, f"tweetfile-@{account}/txt.txt")
    # tweet_file(api, f"tweetfile-@{account}/jpg.txt")
    # tweet_file(api, f"tweetfile-@{account}/gif.txt")

def main():
    run()


if __name__ == "__main__":
    main()
