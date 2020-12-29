import os
import logging
from twitterbot.config import create_api
import time

logger = logging.getLogger('twitter')


def follow_user_following(api, userId):
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
    logger.info(f"{count} users followed from @{userId} following")


def main():
    api = create_api()
    userId = os.getenv("TWITTER_FOLLOWUSERFOLLOWING_USER")
    while True:
        follow_user_following(api, userId)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
