import os
import logging
import datetime
import config
from twitterbot.config import create_api
from twitterbot.followfile import init_files
import os

logger = logging.getLogger('twitter')

def run():
    logger.info("")
    logger.info("*****************")
    logger.info("* Init          *")
    logger.info("*****************")
    logger.info("")
    config.init()
    account = 'Cars2048'
    logger.info(f"Account @{account}")
    config.switch(account)
    api = create_api()
    # 
    init_files(api, 'MichTheGameDev', ['Cars2048'])

def main():
    run()


if __name__ == "__main__":
    main()
