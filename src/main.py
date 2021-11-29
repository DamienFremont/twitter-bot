import os
import logging
import config
import log
from twitterbot.config import create_api
from twitterbot.favtweet import fav_tweet
from twitterbot.followfollowers import follow_followers
from twitterbot.followfriends import follow_friends
from twitterbot.followfile import follow_file
from twitterbot.unfollowinactive import unfollow_inactive
from twitterbot.retweetuser import retweet_user
from twitterbot.tweetfile import tweet_file_random


logger = logging.getLogger('twitterbot')
log.initLogger(logger, appname='twitterbot', modulename='main')


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
            pathname = os.getenv("TWITTER_FEATURES_TWEETFILE_PATHNAME")
            tweet_file_random(api, pathname)
        # if 'retweettag' in features:
            # TODO
        # if 'retweetmentions' in features:
            # TODO
        logger.info("")


def step_promote():
    logger.info("")
    logger.info("* Promote *******")
    logger.info("")
    accounts = os.getenv("TWITTER_ACCOUNTS").split(',')
    for account in accounts:
        logger.info(f"Account @{account}")
        config.switch(account)
        features = os.getenv("TWITTER_FEATURES").split(',')
        logger.info(f"Features {features}")
        api = create_api()
        if 'favtweet' in features:
            users = os.getenv("TWITTER_FEATURES_FAVTWEET_USERS").split(',')
            max = os.getenv("TWITTER_FEATURES_FAVTWEET_MAX", 4)
            for userID in users:
                fav_tweet(api, userID, max)
        if 'retweetuser' in features:
            users = os.getenv("TWITTER_FEATURES_RETWEETUSER_USERS").split(',')
            for userId in users:
                retweet_user(api, userId)
        # if 'favmentions' in features:
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
        if 'followfollowers' in features:
            follow_followers(api)
        if 'followfriends' in features:
            users = os.getenv("TWITTER_FEATURES_FOLLOWFRIENDS_USERS").split(',')
            for userId in users:
                follow_friends(api, userId)
        if 'followfile' in features:
            max = os.getenv("TWITTER_FEATURES_FOLLOWFILE_MAX", 9)
            pathname = os.getenv("TWITTER_FEATURES_FOLLOWFILE_PATHNAME")
            follow_file(api, pathname = pathname, max = max)
        # if 'unfollowinactive' in features:
            # unfollow_inactive(api)
        logger.info("")


def main():
    init()
    step_content()
    step_promote()
    step_network()
    logger.info("")
    logger.info("End with success.")
    # logger.info("Waiting...")
    # time.sleep(60 * 60)


if __name__ == "__main__":
    main()
