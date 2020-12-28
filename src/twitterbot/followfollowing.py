import os
import tweepy
import logging
from twitterbot.config import create_api
import time

logger = logging.getLogger('twitter')

def follow_following(api, userId):
    count = 0
    try:
        for follower in api.friends(userId):
            if not follower.following:
                logger.info(f"  Following @{follower.name}")
                follower.follow()
                count += 1
                time.sleep(5)
    except Exception as e:
        logger.warning(f"Rate limit exceeded")
    return count

def last20(api, userId):
    count = follow_following(api, userId)
    logger.info(f"{count} users followed from @{userId} following")

def last20Batch(api):
    users = os.getenv("TWITTER_FOLLOWFOLLOWING_USERS").split(',')
    for userId in users:
        last20(api, userId)

def main():
    api = create_api()
    last20Batch(api)

if __name__ == "__main__":
    main()