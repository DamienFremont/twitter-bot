import sys, os, glob, getopt, time
import logging
import config, log
import twitterbot

# STATIC **********************************************************************

logger = logging.getLogger('twitterbot')
log.initLogger(logger, appname='twitterbot', modulename='main')

# PUBLIC **********************************************************************

# PRIVATE *********************************************************************

def batch(create, promote, network):
    logger.info("Batch | Job")
    config.loadProperties()
    if create:
        logger.info(" ")
        logger.info("Batch | Executing step: [create]")
        accountsloop(
            createstep)
    if promote:
        logger.info(" ")
        logger.info("Batch | Executing step: [promote]")
        accountsloop(
            promotestep)
    if network:
        logger.info(" ")
        logger.info("Batch | Executing step: [network]")
        accountsloop(
            networkstep)
    logger.info(" ")
    logger.info("Batch | Job finished.")

def createstep(api, features):
    if 'tweetfile' in features:
        pathname = os.getenv("TWITTER_FEATURES_TWEETFILE_PATHNAME")
        pathdir = os.getenv("TWITTERBOT_CONFIG_PATH")
        twitterbot.tweetfilerandom(api, pathname, fallback_dir=pathdir)
    # if 'retweettag' in features:
        # TODO
    # if 'retweetmentions' in features:
        # TODO

def promotestep(api, features):
    if 'favtweet' in features:
        users = os.getenv("TWITTER_FEATURES_FAVTWEET_USERS").split(',')
        max = int(os.getenv("TWITTER_FEATURES_FAVTWEET_MAX", 4))
        for userID in users:
            twitterbot.favtweet(api, userID)
    if 'retweetuser' in features:
        users = os.getenv("TWITTER_FEATURES_RETWEETUSER_USERS").split(',')
        max = int(os.getenv("TWITTER_FEATURES_RETWEETUSER_MAX", 10))
        for userId in users:
            twitterbot.retweetuser(api, userId, max)
    # if 'favmentions' in features:
        # TODO
    # if 'replymessage' in features:
        # TODO
    # if 'replyfollow' in features:
        # TODO

def networkstep(api, features):
    if 'followfile' in features:
        max = int(os.getenv("TWITTER_FEATURES_FOLLOWFILE_MAX", 9))
        pathname = os.getenv("TWITTER_FEATURES_FOLLOWFILE_PATHNAME")
        pathdir = os.getenv("TWITTERBOT_CONFIG_PATH")
        twitterbot.followfile(api, pathname = pathname, max = max, fallback_dir = pathdir)
    if 'followfriends' in features:
        users = os.getenv("TWITTER_FEATURES_FOLLOWFRIENDS_USERS").split(',')
        for userId in users:
            twitterbot.followfriends(api, userId)
    if 'followback' in features:
        twitterbot.followback(api)
    # if 'unfollowinactive' in features:
        # TODO unfollowinactive(api)

def accountsloop(method):
    accounts = os.getenv("TWITTER_ACCOUNTS").split(',')
    for account in accounts:
        api, features = initstep(account)
        logger.info("")
        logger.info(f"Batch | Processing item: [@{account}]")
        logger.info(f"Batch | Processing feat: [{features}]")
        method(api, features)

def initstep(account):
    config.switch(account)
    config.loadProperties()
    features = os.getenv("TWITTER_FEATURES").split(',')
    api = twitterbot.initapi()
    return api, features

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
    print("Running default command line with: ")
    for conf in configs:
        if not conf['longopt'] in res.keys():
            res[conf['longopt']] = conf['defarg']
        print(f"argument --{conf['longopt']}: '{res[conf['longopt']]}'")
    return res

# DEPRECATED from distutils.util import strtobool
# 'For these functions, and any others not mentioned here, you will need to reimplement the functionality yourself'
def strtobool (val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))

# SCRIPT **********************************************************************

def main(argv):
    argd = getargs(argv, [
        { 'opt':'loop',    'defarg':'true' },
        { 'opt':'wait',    'defarg':'60'   },
        { 'opt':'create',  'defarg':'true' },
        { 'opt':'promote', 'defarg':'true' },
        { 'opt':'network', 'defarg':'true' }])
    logger.info("Twitter Bot")
    logger.info(f'Exec. path : {os.getcwd()}')
    create = strtobool(argd.get('create'))
    promote = strtobool(argd.get('promote'))
    network = strtobool(argd.get('network'))
    loop = strtobool(argd.get('loop'))
    wait = int(argd.get('wait'))
    while True:
        batch(create, promote, network)
        if not loop:
            break
        logger.info(f"Waiting for {wait} minutes...")
        time.sleep(wait * 60)

if __name__ == "__main__":
    main(sys.argv[1:])
