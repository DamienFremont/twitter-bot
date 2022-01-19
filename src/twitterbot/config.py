import tweepy
import logging
import os

# STATIC **********************************************************************

logger = logging.getLogger('twitterbot')

# PUBLIC **********************************************************************

def initapi():
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,
                     wait_on_rate_limit=False)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error(f"Error creating session", exc_info=True)
        raise e
    logger.info(f"Session created (API v1)")
    return api

# def initclient():
#     bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
#     api = tweepy.Client(bearer_token,
#                      wait_on_rate_limit=False)
#     logger.info(f"Session created (API v2)")
#     return api