import os
import sys
import fileinput
import tweepy

# source:
# https://python.plainenglish.io/hey-tweepy-please-dont-verify-no-certs-c7223370311
# https://github.com/raychorn/tweepy-twitter-bot1/blob/main/tweepy-bot1.py

def hackssl():
    old = 'auth, proxies'
    new = 'auth, verify=False, proxies'
    path = getTweepyPath()
    filename = os.path.join(path, 'api.py')
    if containsText(filename, new):
        print(f'...already hacked : skip')
        return
    replaceFileText(filename, old, new)
    if not containsText(filename, new):
        print(f'...ERROR! text was not replaced!')
        os._exit(0)
    print(f'...replaced with "{new}"')

def containsText(filename, new):
    with open(filename, 'rt', encoding="utf8") as file:
        if new in file.read():
            return True
    return False

def getTweepyPath():
    dirname = os.path.dirname(tweepy.__file__)
    print(f'...tweepy path is {dirname}')
    return dirname

def replaceFileText(filename, old, new):
    print(f'...hacking {filename}')
    with open(filename, 'rt', encoding="utf8") as file:
        data  = file.read()
        data  = data.replace(old, new)
    with open(filename, 'wt', encoding="utf8") as file:
        file.write(data )

# SCRIPT **********************************************************************

def main():
    hackssl()

if __name__ == "__main__":
    main()