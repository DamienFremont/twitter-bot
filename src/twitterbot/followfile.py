import os
import logging
from twitterbot.config import create_api
import time
import os, time, sys
import shutil

logger = logging.getLogger('twitter')


def init_files(api, screen_name, targets):
    follow_file_write(api, screen_name)
    for t in targets:
        shutil.copyfile(f"friends-@{screen_name}.csv", f'followfile-@{t}.csv')


def follow_file_write(api, screen_name):
    file_name = f"friends-@{screen_name}.csv"
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


def follow_file(api, max = 9):
    me = api.verify_credentials()
    file_name = f"followfile-@{me.screen_name}.csv"
    count = 0
    i = 0
    with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            if i >= max:
                break
            try:
                follower = api.get_user(user_id = line)
                if follower != me and not follower.following:
                    logger.info(f"  Following @{follower.screen_name}")
                    follower.follow()
                    count += 1
                    time.sleep(5)
            except Exception as e:
                logger.warning(f"  Skip user_id {line}: {e}")
            i += 1
            delete_line_in_file(file_name, f"{str(line)}")
    logger.info(f"{count} users followed from file {file_name} ")
    logger.info(f"{i} lines removing from file {file_name} ")


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
    max = os.getenv("TWITTER_FOLLOWFILE_MAX", 9)
    follow_file(api, max)


if __name__ == "__main__":
    main()
