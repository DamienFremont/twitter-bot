import logging
from twitterbot.config import create_api
import time
import tweepy
from math import *
import os

logger = logging.getLogger('twitterbot')

def follow_back(api):
    """follow_back(api)
    
    Follow back. For authenticated user.

    Parameters
    ----------
    api
        |tweepy.API|

    Returns
    -------
    (void)
    """
    logger.debug("Retrieving and following followers")
    pageSize = int(os.getenv("TWITTER_FEATURES_FOLLOWBACK_MAX", 10))
    count = 0
    me = api.verify_credentials()
    try:
        pageCount = ceil(me.followers_count / pageSize)
        cursoriter = tweepy.Cursor(api.get_followers, count=pageSize).pages()
        cursoriter.num_tweets = pageCount - 1
        lastPage = cursoriter.next()
        for follower in lastPage:
            if follower.following or follower.follow_request_sent:
                logger.debug(f"  Skipping @{follower.screen_name}")
                continue
            logger.info(f"  Following @{follower.screen_name}")
            follower.follow()
            count += 1
            time.sleep(5)
    except Exception as e:
        logger.warning(e)         
    logger.info(f"{count} follow todo for last {pageSize} followers")

def main():
    api = create_api()
    while True:
        follow_back(api)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
