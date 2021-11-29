import os
import logging
from twitterbot.config import create_api
import time
import os, time, sys
import shutil

logger = logging.getLogger('twitterbot')

def keep_unique(array, seens):
    lines_seen = set() # holds lines already seen
    array_count = 0
    seen_count = 0
    keep_count = 0
    for seen in seens:
        lines_seen.add(seen)
        seen_count += 1
    unique = set()
    for item in array:
        if item not in lines_seen: # not a duplicate
            unique.add(item)
            keep_count += 1
        array_count += 1
    print(f'keep {keep_count}/{array_count} from {seen_count}')
    return unique

def init_files(api, screen_name, targets):
    follow_file_write(api, screen_name)
    for t in targets:
        shutil.copyfile(f"friends-@{screen_name}.csv", f'twitterbot-followfile-@{t}-following.csv')


def follow_file_write(api, screen_name, file_name):
    me = api.verify_credentials()
    try:
        yourfriends = api.get_friend_ids(screen_name = screen_name)
        time.sleep(15)
        nyfriends = api.get_friend_ids(screen_name = me.screen_name)
        futurfriends = keep_unique(yourfriends, nyfriends);
        file = open(file_name, 'w')
        for line in futurfriends:
            file.write(f"{str(line)}\n")
        file.close()
        logger.info(f"{len(futurfriends)} user ids write to file {file_name}")
    except Exception as e:
        logger.warning(e)


def follow_file(api, pathname, max = 9):
    if not pathname:
        me = api.verify_credentials()
        file_name = f"twitterbot-followfile-@{me.screen_name}.csv"
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
