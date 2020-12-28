import os
import logging
from twitterbot.config import create_api
import json
import time

logger = logging.getLogger('twitter')


def get_last_tweets(api, userID):
    return api.user_timeline(screen_name=userID,
                             # 200 is the maximum allowed count
                             count=50,
                             include_rts=False,
                             # Necessary to keep full_text
                             # otherwise only the first 140 words are extracted
                             tweet_mode='extended'
                             )


def on_status(me, tweet):
    count = 0
    if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == me.id:
        # This tweet is a reply or I'm its author so, ignore it
        return count
    if not tweet.favorited:
        # Mark it as Liked, since we have not done it yet
        try:
            tweet.favorite()
            count += 1
            logger.info(
                f" liked tweet id:{tweet.id} from @{tweet.user.screen_name}")
            time.sleep(15)
        except Exception as e:
            logger.error(
                f"Error on like tweet id:{tweet.id} rom @{tweet.user.screen_name}", exc_info=True)
    return count


def do(api, userID):
    me = api.me()
    if userID == me.screen_name:
        return
    count = 0
    tweets = get_last_tweets(api, userID)
    for tweet in tweets:
        count += on_status(me, tweet)
    logger.info(f"{count} tweets liked from @{userID}")


def doBatch(api):
    users = os.getenv("TWITTER_FAVTWEET_USERS").split(',')
    for userID in users:
        do(api, userID)


def main():
    api = create_api()
    doBatch(api)
