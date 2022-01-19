import os
import logging
from twitterbot.config import initapi
import glob
import random
import os.path
import time

# STATIC **********************************************************************

logger = logging.getLogger('twitterbot')

# PUBLIC **********************************************************************

def tweetfilerandom(api, pathname):
    #  OPEN
    if not pathname:
        me = api.verify_credentials()
        pathname = f"twitterbot-tweetfile-@{me.screen_name}"
    if not os.path.isdir(pathname):
        logger.warning(f"skip tweeting: The system cannot find the pathname specified: '{pathname}'")
        return
    logger.info(f"tweetfilerandom from {pathname}")
    # RANDOM
    files = glob.glob(f"{pathname}/*.txt")
    nb = len(files)
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
            api.update_status(status = text, media_ids = media_ids)
        else:
            api.update_status(status = text)
        logger.info(f"1 tweet {file_name} {media_file}")
        time.sleep(5)
    except Exception as e:
        logger.warning(f"error tweeting '{file_name}': {e}")

# SCRIPT **********************************************************************

def main():
    api = initapi()
    tweetfilerandom(api)

if __name__ == "__main__":
    main()
