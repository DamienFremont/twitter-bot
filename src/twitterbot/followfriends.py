import os
import logging
from twitterbot.config import initapi
import time

logger = logging.getLogger('twitterbot')

def followfriends(api, user_id):
    logger.info(f"followfriends from @{user_id}")
    count = 0
    try:
        for follower in api.get_friends(user_id = user_id):
            if not follower.following or follower.follow_request_sent:
                logger.info(f"  Following @{follower.screen_name}")
                follower.follow()
                count += 1
                time.sleep(5)
    except Exception as e:
        logger.warning(e)
    logger.info(f"{count} friends followed from @{user_id}")

def main():
    api = initapi()
    userId = os.getenv("TWITTER_FEATURES_FOLLOWFRIENDS_USERS")
    while True:
        followfriends(api, userId)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
