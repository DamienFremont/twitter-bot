import os
import logging
from twitterbot.config import create_api
import json
import time

logger = logging.getLogger('twitter')


def get_last_tweets(api, userID, max = 4):
    return api.user_timeline(screen_name=userID,
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
                f"  liked tweet id:{tweet.id} from @{tweet.user.screen_name}")
            time.sleep(15)
        except Exception as e:
            logger.error(
                f"Error on like tweet id:{tweet.id} from @{tweet.user.screen_name}", exc_info=True)
    return count


def fav_user_tweet(api, userID, max = 4):
    count = 0
    me = api.me()
    tweets = get_last_tweets(api, userID, max)
    for tweet in tweets:
        count += on_status(me, tweet)
    logger.info(f"{count} tweets liked from @{userID}")


def main():
    api = create_api()
    userID = os.getenv("TWITTER_FAVUSERTWEET_USER")
    max = os.getenv("TWITTER_FAVUSERTWEET_MAX", 4)
    while True:
        fav_user_tweet(api, userID, max)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
