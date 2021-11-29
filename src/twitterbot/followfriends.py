import os
import logging
from twitterbot.config import create_api
import time

logger = logging.getLogger('twitterbot')


def follow_friends(api, userId):
    count = 0
    try:
        for follower in api.friends(userId):
            if not follower.following:
                logger.info(f"  Following @{follower.screen_name}")
                follower.follow()
                count += 1
                time.sleep(5)
    except Exception as e:
        logger.warning(f"Rate limit exceeded")
    logger.info(f"{count} friends followed from @{userId}")


def main():
    api = create_api()
    userId = os.getenv("TWITTER_FEATURES_FOLLOWFRIENDS_USERS")
    while True:
        follow_friends(api, userId)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
