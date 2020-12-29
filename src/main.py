import os
import logging
import datetime
import config
from twitterbot.config import create_api
from twitterbot.favusertweet import fav_user_tweet
from twitterbot.followfollowers import follow_followers
from twitterbot.followuserfollowing import follow_user_following
from twitterbot.unfollowinactive import unfollow_inactive
from twitterbot.retweetuser import retweet_user
import time

APP_NAME = "app"
MODULE_NAME = "twitter"

LOGGER_PREFIX = f"[{APP_NAME}] bots.twitter : "
DATE_FMT = "%Y%m%d_%H%M%S"
now = datetime.datetime.now()

logger = logging.getLogger(MODULE_NAME)

file_log_handler = logging.FileHandler(
    f"{APP_NAME}-{now.strftime(DATE_FMT)}.log")
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

# nice output format
formatter = logging.Formatter(
    f'%(asctime)s %(levelname)s {LOGGER_PREFIX} %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)


def run():
    logger.info("")
    logger.info("*****************")
    logger.info("* Twitter Bots  *")
    logger.info("*****************")
    logger.info("")
    config.init()
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
        if 'followfollowing' in features:
            users = os.getenv("TWITTER_FOLLOWUSERFOLLOWING_USERS").split(',')
            for userId in users:
                follow_user_following(api, userId)
        # if 'tweetgenerate' in features:
            # tweetgenerate.main()
        # if 'retweettag' in features:
            # TODO
        if 'retweetuser' in features:
            users = os.getenv("TWITTER_RETWEETUSER_USERS").split(',')
            for userId in users:
                retweet_user(api, userId)
        # if 'favmentions' in features:
            # TODO
        # if 'retweetmentions' in features:
            # TODO
        if 'unfollowinactive' in features:
            unfollow_inactive(api)
        logger.info("")
    logger.info("End with success.")


def main():
    while True:
        run()
        logger.info("Waiting...")
        time.sleep(60 * 60)


if __name__ == "__main__":
    main()
