import os
import logging
from twitterbot.config import create_api
import time
import os, time, sys

logger = logging.getLogger('twitter')


def follow_file_following_write(api, screen_name):
    file_name = f"following-@{screen_name}.csv"
    try:
        friends = api.friends_ids(screen_name) 
        file = open(file_name, 'w')
        # file.write("user_id\n")
        for line in friends:
            file.write(f"{str(line)}\n")
        file.close()
    except Exception as e:
        logger.warning(e)
    logger.info(f"{len(friends)} user ids write to file {file_name}")


def follow_file_following(api, file_name, max):
    count = 0
    i = 0
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()
            # file.seek(0)
            for line in lines:
                if i >= max:
                    break
                follower = api.get_user(line)
                if not follower.following:
                    logger.info(f"  Following @{follower.screen_name}")
                    follower.follow()
                    count += 1
                    time.sleep(5)
                i += 1
                logger.info(f"  removing from file {file_name} @{follower.screen_name} ")
                delete_line_in_file(file_name, f"{str(line)}")
    except Exception as e:
        logger.warning(e)
    logger.info(f"{count}/{i} users followed from file {file_name} ")


def delete_line_in_file(file_name, search_line):
    with open(file_name, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != search_line:
                f.write(i)
        f.truncate()

def main():
    api = create_api()
    userId = os.getenv("TWITTER_FOLLOWUSERFOLLOWING_USER")
    while True:
        follow_user_following(api)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
