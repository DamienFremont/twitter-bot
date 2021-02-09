import os
import logging
import configparser

logger = logging.getLogger()
config = configparser.RawConfigParser()
config.read('config.properties')


def envFromProps(userID, key, required):
    propKey = f'twitter.{userID}.{key}'
    try:
        os.environ[key] = config.get('Twitter', propKey)
    except Exception as e:
        if required:
            logger.error(f"missing prop key {propKey}")
            logger.debug("you need to :")
            logger.debug("- fix your config.properties file")
            os._exit(0)
        os.environ[key] = ''


def init():
    os.environ["TWITTER_ACCOUNTS"] = config.get(
        'Twitter', 'twitter.TWITTER_ACCOUNTS')


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
    envFromProps(userID, 'TWITTER_FAVUSERTWEET_USERS', OPTIONNAL)
    envFromProps(userID, 'TWITTER_FOLLOWUSERFOLLOWING_USERS', OPTIONNAL)
    envFromProps(userID, 'TWITTER_FOLLOWFILE', OPTIONNAL)
    envFromProps(userID, 'TWITTER_RETWEETUSER_USERS', OPTIONNAL)
