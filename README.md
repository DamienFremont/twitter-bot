# TWITTER-BOT

[![Twitter Follow](https://img.shields.io/twitter/follow/Damien_Fremont?style=social)](https://twitter.com/Damien_Fremont)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![alt text](docs/screenshot-1.png)

---

The source code was adapted from this article: [How to Make a Twitter Bot in Python With Tweepy](https://realpython.com/twitter-bot-python-tweepy/)

---

## Requirements

### Install Python, pip

### Sign up for Twitter Developer Account

- Sign up for a separate account for your Twitter Bot and then apply for Twitter Developer Account following this link https://developer.twitter.com/en/apply-for-access 
- Enter the necessary details and await for your mail confirmation. Once confirmed, click on Create an App option.
- Enter the necessary details to generate the secret key and access tokens.
- Copy the keys and keep them safe.

---

## Getting Started

For all this we will need a Python library called Tweepy for accessing the Twitter API. We can install tweepy in three ways:

```bash
pip install -r requirements.txt --force-reinstall
```

---

## Usage

Note: for all-in-one usage use `src/main.py`. But every script in `src/twitterbot` is also standalone (eg: favtweet.py, etc).

### Standalone Scripts

1 script by launch, 1 feature, 1 account.

Steps:
1. set env vars for a twitter account
2. launch one of standalone scripts from `src/twitterbot`

eg:

```bash
set TWITTER_CONSUMER_KEY=opcOqjVo**************
set TWITTER_CONSUMER_SECRET=X27ePBXCb**************
set TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAA**************
set TWITTER_ACCESS_TOKEN=873278**************
set TWITTER_ACCESS_TOKEN_SECRET=yg0c9t**************

python .\src\twitterbot\followback.py
```

```bash
set ...
set TWITTER_FEATURES_FAVTWEET_USERS=Damien_Fremont,FremontGames

python .\src\twitterbot\favtweet.py
```

```bash
set ...
set TWITTER_FEATURES_RETWEETUSER_USERS=Damien_Fremont,FremontGames

python .\src\twitterbot\retweetuser.py
```

```bash
set ...
set TWITTER_FEATURES_FOLLOWFRIENDS_USERS=Cars2048

python .\src\twitterbot\followfriends.py
```


### Batch

Main script launched, 1 properties file, multiple features, multiple accounts.

Steps:
1. setup properties configuration file
2. put `main.properties` config file in your execution path, or add `TWITTERBOT_CONFIG_PATH` and `TWITTERBOT_CONFIG_FILE` env vars
2. launch main script

Note: default file is `./main.properties`.
```bash
set TWITTERBOT_CONFIG_PATH=.
set TWITTERBOT_CONFIG_FILE=main.properties
```


```properties
# .\main.properties file

[Twitter]
twitter.TWITTER_ACCOUNTS = <ACCOUNT_1>,<ACCOUNT_2>
# @<ACCOUNT_1>
twitter.<ACCOUNT_1>.TWITTER_CONSUMER_KEY = opcOqjVo**************
twitter.<ACCOUNT_1>.TWITTER_CONSUMER_SECRET = X27ePBXCb**************
twitter.<ACCOUNT_1>.TWITTER_BEARER_TOKEN = AAAAAAAAAAAAAA**************
twitter.<ACCOUNT_1>.TWITTER_ACCESS_TOKEN = 873278**************
twitter.<ACCOUNT_1>.TWITTER_ACCESS_TOKEN_SECRET = yg0c9t**************
...
twitter.<ACCOUNT_1>.TWITTER_FEATURES = ...<FEATURE_1>,<FEATURE_2>
...
twitter.<ACCOUNT_1>.TWITTER_FEATURES_<FEATURE_1>_<OPTION> = ...
twitter.<ACCOUNT_1>.TWITTER_FEATURES_<FEATURE_2>_<OPTION> = ...
...
# @<ACCOUNT_2>
twitter.<ACCOUNT_2>.TWITTER_CONSUMER_KEY = opcOqjVo**************
```

```bash
python .\src\main.py
```
or
```bash
python .\src\main.py --create <true|false> --promote <true|false> --network <true|false> --loop <true|false> --wait <0|...|60>
```

```bash
$ python .\src\main.py --network true
or
$ python .\src\main.py --network false
or
$ python .\src\main.py --network True --promote True --create false 
or
$ python .\src\main.py -n true -p true -c true -l false 
```

## Example (single account)

```properties
# .\main.properties file

[Twitter]
twitter.TWITTER_ACCOUNTS = FremontGames

# @FremontGames
twitter.FremontGames.TWITTER_CONSUMER_KEY = opcOqjVo**************
twitter.FremontGames.TWITTER_CONSUMER_SECRET = X27ePBXCb**************
twitter.FremontGames.TWITTER_BEARER_TOKEN = AAAAAAAAAAAAAA**************
twitter.FremontGames.TWITTER_ACCESS_TOKEN = 873278**************
twitter.FremontGames.TWITTER_ACCESS_TOKEN_SECRET = yg0c9t**************
twitter.FremontGames.TWITTER_FEATURES = followback
```

```bash
$ python .\src\main.py
```

## Example (multiple accounts)

```properties
# .\main.properties file

[Twitter]
twitter.TWITTER_ACCOUNTS = FremontGames,Cars2048

# @FremontGames
twitter.FremontGames.TWITTER_CONSUMER_KEY = opcOqjVo**************
...
# @Cars2048
twitter.Cars2048.TWITTER_CONSUMER_KEY = k1XBM**************
...
```

```bash
$ python .\src\main.py
```

## Example (more features)

```properties
# .\main.properties file
...
twitter.TWITTER_FEATURES_FOLLOWFILE_MAX = 9
twitter.TWITTER_FEATURES_FAVTWEET_MAX = 4
twitter.TWITTER_FEATURES_FOLLOWBACK_MAX = 100
...
twitter.FremontGames.TWITTER_FEATURES = ...,favtweet,followfriends,retweetuser,tweetfile,followfile
twitter.FremontGames.TWITTER_FEATURES_FAVTWEET_USERS = Cars2048,Damien_Fremont
twitter.FremontGames.TWITTER_FEATURES_FOLLOWFRIENDS_USERS = Damien_Fremont
twitter.FremontGames.TWITTER_FEATURES_RETWEETUSER_USERS = Damien_Fremont
twitter.FremontGames.TWITTER_FEATURES_TWEETFILE_PATHNAME = .\tweetfile-@FremontGames
twitter.FremontGames.TWITTER_FEATURES_FOLLOWFILE_PATHNAME = .\followfile-@FremontGames

```

## Standalone Scripts

You can use each script in standalone (ex: python tweetfile.py)

To run the bot, you must first create the environment variables for the authentication credentials. You can do this by running this commands from a terminal and replacing the values with your actual credentials:

```
$ export CONSUMER_KEY="pGBDoAaEpkliVKBOLwjtcmHGc"
$ export CONSUMER_SECRET="xF3g1wrP50b6BlZEd20u4oVfjgH1FGQcuWUzlQO5aUWOufvlhw"
$ export ACCESS_TOKEN="622518493-6VcLIPprbQbv9wkcBBPvCle8vsjU9fE85Dq9oStl"
$ export ACCESS_TOKEN_SECRET="tH9aKQbQQ1iRdYTcLSsPwitl44BkAc6jilrsU0ifnXvZhq"
```

Note: This assumes that you’re using Linux or macOS. If you’re using Windows, then the steps might be a little different.

After you run the commands, your environment variables will contain the credentials needed to use the Twitter API.

---

## References


- https://developer.twitter.com/en/portal/dashboard

- Tutorials 

  - API v2
    - https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9

  - API v1
    - https://www.geeksforgeeks.org/how-to-make-a-twitter-bot-in-python/
    - https://realpython.com/twitter-bot-python-tweepy/
  - Domain
    - https://en.wikipedia.org/wiki/Online_community_manager
  - Docs
    - http://docs.tweepy.org/en/latest/
    - https://docs.python.org/3/library/venv.html
