import os
import logging
import tweepy
from twitterbot.config import create_api
import time
import datetime

logger = logging.getLogger('twitter')


def unfollow_inactive(api):
    count = 0
    me = api.me()
    try:
        for page in tweepy.Cursor(api.friends).pages():
            logger.debug(f"  page")
            for follower in page:
            # for follower in api.friends(me.screen_name):
                logger.debug(f"  test @{follower.screen_name}")
                tweets = api.user_timeline(follower.screen_name, page=1)
                lastTweet = tweets[0]
                inactivity = (datetime.datetime.now() - lastTweet.created_at).days
                logger.debug(f"    test @{inactivity}")
                if inactivity > 182:
                    print(lastTweet.text.encode("utf-8"))
                    logger.info(f"  unfollow @{follower.screen_name}")
                    count += 1
                    time.sleep(5)
            time.sleep(10)
    except Exception as e:
        logger.warning(f"Rate limit exceeded")
    logger.info(f"{count} unfollowed inactive")


def main():
    api = create_api()
    while True:
        unfollow_inactive(api)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
