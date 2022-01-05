import os
import logging
import configparser

logger = logging.getLogger()

config_pathname = os.getenv("TWITTERBOT_CONFIG", 'main.properties')
config = configparser.RawConfigParser()
config.read(config_pathname)


def envFromProps(userID, key, required):
    propKey = f'twitter.{userID}.{key}'
    try:
        os.environ[key] = config.get('Twitter', propKey)
    except Exception as e:
        if required:
            logger.error(f"missing prop key {propKey}")
            logger.debug("you need to :")
            logger.debug("- fix your main.properties file")
            os._exit(0)
        os.environ[key] = ''


def init():
    os.environ["TWITTER_ACCOUNTS"] = config.get('Twitter', 'twitter.TWITTER_ACCOUNTS')
    os.environ["TWITTER_FEATURES_FOLLOWFILE_MAX"] = config.get('Twitter', 'twitter.TWITTER_FEATURES_FOLLOWFILE_MAX')
    os.environ["TWITTER_FEATURES_FAVTWEET_MAX"] = config.get('Twitter', 'twitter.TWITTER_FEATURES_FAVTWEET_MAX')
    os.environ["TWITTER_FEATURES_FOLLOWBACK_MAX"] = config.get('Twitter', 'twitter.TWITTER_FEATURES_FOLLOWBACK_MAX')


def switch(userID):
    accounts = config.get('Twitter', 'twitter.TWITTER_ACCOUNTS').split(',')
    if(userID not in accounts):
        logger.error(f"bad env name {userID}")
        logger.debug("you need to :")
        logger.debug(
            "- get keys from https://developer.twitter.com/en/portal/dashboard")
        logger.debug("- set app permission to Read + Write + Direct Messages")
        logger.debug("- regenerate your keys")
        os._exit(0)
    REQUIRED = True
    envFromProps(userID, 'TWITTER_CONSUMER_KEY', REQUIRED)
    envFromProps(userID, 'TWITTER_CONSUMER_SECRET', REQUIRED)
    envFromProps(userID, 'TWITTER_BEARER_TOKEN', REQUIRED)
    envFromProps(userID, 'TWITTER_ACCESS_TOKEN', REQUIRED)
    envFromProps(userID, 'TWITTER_ACCESS_TOKEN_SECRET', REQUIRED)
    OPTIONNAL = False
    envFromProps(userID, 'TWITTER_FEATURES', OPTIONNAL)
    envFromProps(userID, 'TWITTER_FEATURES_FAVTWEET_USERS', OPTIONNAL)
    envFromProps(userID, 'TWITTER_FEATURES_FOLLOWFRIENDS_USERS', OPTIONNAL)
    envFromProps(userID, 'TWITTER_FEATURES_RETWEETUSER_USERS', OPTIONNAL)

    envFromProps(userID, 'TWITTER_INIT_FEATURES', OPTIONNAL)
    envFromProps(userID, 'TWITTER_INIT_FEATURES_FOLLOWFILE_USER', OPTIONNAL)
    envFromProps(userID, 'TWITTER_INIT_FEATURES_FOLLOWFILE_PATHNAME', OPTIONNAL)
