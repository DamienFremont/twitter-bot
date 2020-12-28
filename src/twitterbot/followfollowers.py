import tweepy
import logging
from twitterbot.config import create_api
import time

logger = logging.getLogger('twitter')


def follow_followers(api):
    count = 0
    me = api.me()
    try:
        for follower in api.followers(me.screen_name):
            if not follower.following:
                logger.info(f"Following @{follower.name}")
                follower.follow()
                count += 1
                time.sleep(5)
    except Exception as e:
        logger.warning(f"Rate limit exceeded")
    return count


def main(api):
    count = follow_followers(api)
    logger.info(f"{count} followers followed")


if __name__ == "__main__":
    api = create_api()
    main(api)
