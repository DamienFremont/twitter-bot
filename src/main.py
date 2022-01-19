import sys, os, glob, getopt
import logging
import config, log
import twitterbot

# STATIC **********************************************************************

logger = logging.getLogger('twitterbot')
log.initLogger(logger, appname='twitterbot', modulename='main')

# PUBLIC **********************************************************************

# PRIVATE *********************************************************************

def bot(argv):
    argdic = getargs(argv, [
        { 'opt':'create',  'defarg':'true' },
        { 'opt':'promote', 'defarg':'true' },
        { 'opt':'network', 'defarg':'true' } ])
    init()
    if istrue(argdic.get('create')):
        contentstep()
    if istrue(argdic.get('promote')):
        promotestep()
    if istrue(argdic.get('network')):
        networkstep()
    logger.info("")
    logger.info("End with success.")
    # logger.info("Waiting...")
    # time.sleep(60 * 60)

def istrue(str):
    return str in ('TRUE', 'True', 'true', '1')

def init():
    logger.info("")
    logger.info("*****************")
    logger.info("* Twitter Bot   *")
    logger.info("*****************")
    logger.info("")
    config.init()

def contentstep():
    logger.info("")
    logger.info("* Content *******")
    logger.info("")
    accounts = os.getenv("TWITTER_ACCOUNTS").split(',')
    for account in accounts:
        logger.info(f"Account @{account}")
        config.switch(account)
        features = os.getenv("TWITTER_FEATURES").split(',')
        logger.info(f"Features {features}")
        api = twitterbot.initapi()
        if 'tweetfile' in features:
            pathname = os.getenv("TWITTER_FEATURES_TWEETFILE_PATHNAME")
            twitterbot.tweetfilerandom(api, pathname)
        # if 'retweettag' in features:
            # TODO
        # if 'retweetmentions' in features:
            # TODO
        logger.info("")

def promotestep():
    logger.info("")
    logger.info("* Promote *******")
    logger.info("")
    accounts = os.getenv("TWITTER_ACCOUNTS").split(',')
    for account in accounts:
        logger.info(f"Account @{account}")
        config.switch(account)
        features = os.getenv("TWITTER_FEATURES").split(',')
        logger.info(f"Features {features}")
        api = twitterbot.initapi()
        if 'favtweet' in features:
            users = os.getenv("TWITTER_FEATURES_FAVTWEET_USERS").split(',')
            max = int(os.getenv("TWITTER_FEATURES_FAVTWEET_MAX", 4))
            for userID in users:
                twitterbot.favtweet(api, userID)
        if 'retweetuser' in features:
            users = os.getenv("TWITTER_FEATURES_RETWEETUSER_USERS").split(',')
            for userId in users:
                twitterbot.retweetuser(api, userId)
        # if 'favmentions' in features:
            # TODO
        # if 'replymessage' in features:
            # TODO
        # if 'replyfollow' in features:
            # TODO
        logger.info("")

def networkstep():
    logger.info("")
    logger.info("* Network *******")
    logger.info("")
    accounts = os.getenv("TWITTER_ACCOUNTS").split(',')
    for account in accounts:
        logger.info(f"Account @{account}")
        config.switch(account)
        features = os.getenv("TWITTER_FEATURES").split(',')
        logger.info(f"Features {features}")
        api = twitterbot.initapi()
        if 'followfile' in features:
            max = int(os.getenv("TWITTER_FEATURES_FOLLOWFILE_MAX", 9))
            pathname = os.getenv("TWITTER_FEATURES_FOLLOWFILE_PATHNAME")
            twitterbot.followfile(api, pathname = pathname, max = max)
        if 'followfriends' in features:
            users = os.getenv("TWITTER_FEATURES_FOLLOWFRIENDS_USERS").split(',')
            for userId in users:
                twitterbot.followfriends(api, userId)
        if 'followback' in features:
            twitterbot.followback(api)
        # if 'unfollowinactive' in features:
            # TODO unfollowinactive(api)
        logger.info("")

# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def getargs(argv, configs, helpmsg=None):
    """getargs(argv, configs, helpmsg)
    
    Return dictionnary with long opt names as keys and arg as values. 
    From Reading command line arguments, using short or long opt names with default values from configs object.

    Parameters
    ----------
    argv
        |sys.argv[1:]|
    configs
        |array<dictionnary['opt':str,'shortopt':str,'longopt':str,'defarg':str]>|
        example : [{'opt':'myopt'},...] or [{'shortopt':'mo','longopt':'myopt','defarg':'False'},...]
    helpmsg
        |str(optionnal)|
        example : 'python myscript.py -m <myopt>'

    Returns
    -------
    dictionnary[key(longopt):str(arg or defarg)]

    Usage
    -----
    argv = sys.argv[1:]

    helpmsg = 'python myscript.py -m <myopt>'

    configs = [{ 'opt':'myopt', 'defarg':'False' } ]

    argdic = getargs(argv, configs, helpmsg)

    myoptarg = argdic.get('myopt')
    """
    shortopts = "h"
    longopts = []
    defhelpmsg = 'Usage: python [script].py'
    for conf in configs:
        # DEF VALS
        if not 'longopt' in conf.keys():
            conf['longopt'] = conf['opt']
        if not 'shortopt' in conf.keys():
            conf['shortopt'] = conf['longopt'][0]
        if not 'defarg' in conf.keys():
            conf['defarg'] = None
        # BUILD PARAMS
        shortopts += f"{conf['shortopt']}:"
        longopts.append(f"{conf['longopt']}=")
        defhelpmsg += f" --{conf['longopt']} <{conf['defarg']}>"
    help = defhelpmsg if helpmsg is None else helpmsg
    # READ OPT
    try:
        opts, args = getopt.getopt(argv,shortopts,longopts)
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    # GET ARGS
    res = {}
    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        else:
            for conf in configs:
                if opt in (f"-{conf['shortopt']}", f"--{conf['longopt']}"):
                    res[conf['longopt']] = arg
                    continue
    # DEFAULT ARGS
    for conf in configs:
        if not conf['longopt'] in res.keys():
            res[conf['longopt']] = conf['defarg']
        print(f"argument --{conf['longopt']}: '{res[conf['longopt']]}'")
    return res

# SCRIPT **********************************************************************

def main(argv):
    bot(argv)

if __name__ == "__main__":
    main(sys.argv[1:])
