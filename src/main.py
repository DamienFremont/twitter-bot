import os
import logging
import datetime
import config
from twitterbot.config import create_api
from twitterbot import favusertweet
from twitterbot import followfollowers
from twitterbot import followuserfollowing

APP_NAME = "app"
MODULE_NAME = "twitter"

LOGGER_PREFIX = f"[{APP_NAME}] bots.twitter : "
DATE_FMT = "%Y%m%d_%H%M%S"
now = datetime.datetime.now()

logger = logging.getLogger(MODULE_NAME)

file_log_handler = logging.FileHandler(f"{APP_NAME}-{now.strftime(DATE_FMT)}.log")
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

# nice output format
formatter = logging.Formatter(f'%(asctime)s %(levelname)s {LOGGER_PREFIX} %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)

def main():
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
                favusertweet.main(api, userID)
        if 'followfollowers' in features:
            followfollowers.main(api)
        if 'followfollowing' in features:
            users = os.getenv("TWITTER_FOLLOWUSERFOLLOWING_USERS").split(',')
            for userId in users:
                followuserfollowing.main(api, userId)
        # if 'tweetrandom' in features:
            # tweetrandom.main()
        # if 'retweettag' in features:
            # TODO
        # if 'retweetall' in features:
            # TODO
        # if 'favmentions' in features:
            # TODO
        # if 'retweetmentions' in features:
            # TODO
        # if 'unfollowinactive' in features:
            # TODO
        logger.info("")
    logger.info("End with success.")


if __name__ == "__main__":
    main()
