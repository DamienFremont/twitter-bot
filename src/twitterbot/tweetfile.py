import os
import logging
from twitterbot.config import initapi
import glob
import random
import os
import os.path
import time

# STATIC **********************************************************************

logger = logging.getLogger('twitterbot')

# PUBLIC **********************************************************************

def tweetfilerandom(api, pathname, fallback_dir = '.'):
    #  OPEN
    if not pathname:
        me = api.verify_credentials()
        pathname = f"{fallback_dir}/twitterbot-tweetfile-@{me.screen_name}"
    # CHECK
    logger.info(f"tweetfile | [folder: {pathname}/]")
    if not os.path.isdir(pathname):
        logger.warning(f"tweetfile | skip tweeting: The system cannot find the pathname specified: '{pathname}'")
        return
    files = glob.glob(f"{pathname}/*.txt")
    nb = len(files)
    if nb == 0:
        logger.warning(f"tweetfile | skip tweeting: empty folder: '{pathname}'")
        return
    # RANDOM
    random.seed(os.getpid())
    rn = random.randint(0, nb-1)
    # POST
    # os.chdir("..")
    file_name = files[rn]
    tweetfile(api, file_name)

# PRIVATE *********************************************************************

def tweetfile(api, file_name):
    with open(file_name, 'r') as file:
        text = file.read()
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
            media_file = png
        elif os.path.isfile(gif):
            media_file = gif
        elif os.path.isfile(mp4):
            media_file = mp4
        if os.path.isfile(media_file):
            media = api.media_upload(filename = media_file)
            media_ids = [ media.media_id_string ]
            logger.info(f"tweetfile | 1 tweet {media_file}")
            api.update_status(status = text, media_ids = media_ids)
        else:
            logger.info(f"tweetfile | 1 tweet {file_name}")
            api.update_status(status = text)
        time.sleep(5)
    except Exception as e:
        logger.warning(f"tweetfile | error tweeting '{file_name}': {e}")

# SCRIPT **********************************************************************

def main():
    api = initapi()
    tweetfilerandom(api)

if __name__ == "__main__":
    main()
