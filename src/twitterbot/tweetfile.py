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
    me = api.verify_credentials()
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
        mp4 = file_name.replace(".txt", ".mp4")
        # POST
        if os.path.isfile(jpg):
            media_file = jpg
        elif os.path.isfile(png):
            media_file = jpg
        elif os.path.isfile(gif):
            media_file = jpg
        elif os.path.isfile(mp4):
            media_file = mp4
        else:
            media_file = 'no file'
        if os.path.isfile(media_file):
            media = api.media_upload(filename = mp4)
            media_ids = [ media.media_id_string ]
            api.update_status(status = text, media_ids = media_ids)
        else:
            api.update_status(status = text)
        count += 1
        time.sleep(5)
    except Exception as e:
        logger.warning(f"error tweeting '{file_name}': {e}")
    logger.info(f"{count} tweet '{file_name}'")


def main():
    api = create_api()
    tweet_file_random(api)


if __name__ == "__main__":
    main()
