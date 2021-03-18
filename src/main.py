import os
import logging
import datetime
import config
from twitterbot.config import create_api
from twitterbot.favusertweet import fav_user_tweet
from twitterbot.followfollowers import follow_followers
from twitterbot.followfriends import follow_friends
from twitterbot.followfile import follow_file
from twitterbot.unfollowinactive import unfollow_inactive
from twitterbot.retweetuser import retweet_user
from twitterbot.tweetfile import tweet_file_random
import time

APP_NAME = "app"
MODULE_NAME = "twitter"

LOGGER_PREFIX = f"[{APP_NAME}] bots.twitter : "
DATE_FMT = "%Y%m%d_%H%M%S"
now = datetime.datetime.now()

logger = logging.getLogger(MODULE_NAME)

file_log_handler = logging.FileHandler(
    f"logs/{APP_NAME}-{now.strftime(DATE_FMT)}.log")
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

# nice output format
formatter = logging.Formatter(
    f'%(asctime)s %(levelname)s {LOGGER_PREFIX} %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)


def init():
    logger.info("")
    logger.info("*****************")
    logger.info("* Twitter Bots  *")
    logger.info("*****************")
    logger.info("")
    config.init()


def step_content():
    logger.info("")
    logger.info("* Content *******")
    logger.info("")
    accounts = os.getenv("TWITTER_ACCOUNTS").split(',')
    for account in accounts:
        logger.info(f"Account @{account}")
        config.switch(account)
        features = os.getenv("TWITTER_FEATURES").split(',')
        logger.info(f"Features {features}")
        api = create_api()
        if 'tweetfile' in features:
            tweet_file_random(api)
        if 'retweetuser' in features:
            users = os.getenv("TWITTER_RETWEETUSER_USERS").split(',')
            for userId in users:
                retweet_user(api, userId)
        # if 'retweettag' in features:
            # TODO
        # if 'retweetmentions' in features:
            # TODO
        logger.info("")


def step_network():
    logger.info("")
    logger.info("* Network *******")
    logger.info("")
    accounts = os.getenv("TWITTER_ACCOUNTS").split(',')
    for account in accounts:
        logger.info(f"Account @{account}")
        config.switch(account)
        features = os.getenv("TWITTER_FEATURES").split(',')
        logger.info(f"Features {features}")
        api = create_api()
        if 'favtweet' in features:
            users = os.getenv("TWITTER_FAVUSERTWEET_USERS").split(',')
            for userID in users:
                fav_user_tweet(api, userID)
        if 'followfollowers' in features:
            follow_followers(api)
        if 'followfriends' in features:
            users = os.getenv("TWITTER_FOLLOWFRIENDS_USERS").split(',')
            for userId in users:
                follow_friends(api, userId)
        if 'followfile' in features:
            max = 21
            follow_file(api, max)
        # if 'favmentions' in features:
            # TODO
        # if 'unfollowinactive' in features:
            # unfollow_inactive(api)
        logger.info("")


def main():
    # while True:
    init()
    step_content()
    step_network()
    logger.info("")
    logger.info("End with success.")
    # logger.info("Waiting...")
    # time.sleep(60 * 60)


if __name__ == "__main__":
    main()
