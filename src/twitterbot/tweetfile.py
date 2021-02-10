import os
import logging
from twitterbot.config import create_api
import glob
import random
import os.path
import time

logger = logging.getLogger('twitter')


def tweet_file_random(api):
    #  OPEN
    me = api.me()
    folder = f"tweetfile-@{me.screen_name}"
    if not os.path.isdir(folder):
        logger.warning(f"skip tweeting: The system cannot find the folder specified: '{folder}'")
        return
    # os.chdir(folder)
    # RANDOM
    text_ext = "txt"
    files = glob.glob(f"{folder}/*.txt")
    nb = len(files)
    rn = random.randint(0, nb-1)
    # POST
    # os.chdir("..")
    file_name = files[rn]
    tweet_file(api, file_name)


def tweet_file(api, file_name):
    with open(file_name, 'r') as file:
        text = file.read()
    count = 0
    try:
        # EXT
        jpg = file_name.replace(".txt", ".jpg")
        png = file_name.replace(".txt", ".png")
        gif = file_name.replace(".txt", ".gif")
        # POST
        if os.path.isfile(jpg):
            api.update_with_media(filename = jpg, status = text) 
        elif os.path.isfile(png):
            api.update_with_media(filename = png, status = text) 
        elif os.path.isfile(gif):
            api.update_with_media(filename = gif, status = text) 
        else:
            api.update_status(status = text)
        count += 1
        time.sleep(5)
    except Exception as e:
        logger.warning(f"error tweeting '{file_name}': {e}")
    logger.info(f"{count} tweet '{file_name}'")


def main():
    api = create_api()
    tweet_random_file(api)


if __name__ == "__main__":
    main()
