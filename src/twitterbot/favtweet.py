import os
import logging
from twitterbot.config import initapi
import json
import time

# STATIC **********************************************************************

logger = logging.getLogger('twitterbot')

# PUBLIC **********************************************************************

def favtweet(api, user_id, max = 4):
    me = api.verify_credentials()
    logger.info(f"favtweet | @{me.screen_name} [fav: @{user_id}]")
    count = 0
    tweets = get_last_tweets(api, user_id, max)
    for tweet in tweets:
        count += on_status(me, tweet)
    logger.info(f"favtweet | {count} tweets liked from @{user_id}")

# PRIVATE *********************************************************************

def get_last_tweets(api, user_id, max = 4):
    return api.user_timeline(screen_name=user_id,
                             # 200 is the maximum allowed count
                             count=max,
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
        # Retweet, since we have not retweeted it yet
        try:
            tweet.favorite()
            count += 1
            logger.info(
                f"favtweet | liked tweet id:{tweet.id} from @{tweet.user.screen_name}")
            time.sleep(15)
        except Exception as e:
            logger.error(
                f"favtweet | Error on like tweet id:{tweet.id} from @{tweet.user.screen_name}", exc_info=True)
    return count

# SCRIPT **********************************************************************

def main():
    api = initapi()
    user_id = os.getenv("TWITTER_FAVTWEET_USER")
    max = os.getenv("TWITTER_FEATURES_FAVTWEET_MAX", 4)
    while True:
        favtweet(api, user_id, max)
        logger.info("favtweet | Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
