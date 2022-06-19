import tweepy
from json import load


def autentica_list():
    with open("7c0/config.json") as jsonfile:
        db_config = load(jsonfile)['twitter-keys']

    auth = tweepy.OAuthHandler(db_config['api_key'], db_config['api_secret_key'])
    auth.set_access_token(db_config['access_token'], db_config['access_token_secret'])

    api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=3, retry_delay=60, retry_errors=set([503]))

    return api


def autentica_tweets():
    with open("config.json") as jsonfile:
        db_config = load(jsonfile)['twitter-keys']

    auth = tweepy.OAuthHandler(db_config['api_key'], db_config['api_secret_key'])
    auth.set_access_token(db_config['access_token'], db_config['access_token_secret'])

    api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=3, retry_delay=60, retry_errors=set([503]))

    return api
