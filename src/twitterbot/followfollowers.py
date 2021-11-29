import logging
from twitterbot.config import create_api
import time

logger = logging.getLogger('twitterbot')


def follow_followers(api):
    logger.debug("Retrieving and following followers")
    count = 0
    me = api.verify_credentials()
    try:
        for follower in api.followers(me.screen_name):
            if not follower.following:
                logger.info(f"  Following @{follower.screen_name}")
                follower.follow()
                count += 1
                time.sleep(5)
    except Exception as e:
        logger.warning(f"Rate limit exceeded")
    logger.info(f"{count} followers followed")

def main():
    api = create_api()
    while True:
        follow_followers(api)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
