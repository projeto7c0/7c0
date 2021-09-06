import tweepy
import twitter_auth
from datetime import datetime
from json import load


with open("tweets.json", encoding='utf-8') as jsonfile:
        tweet_texts = load(jsonfile)

def list_tweets(last_id, twitter_list):
    api = twitter_auth.autentica_list()

    tweets = []

    if (last_id):
        for status in tweepy.Cursor(api.list_timeline, tweet_mode='extended', owner_id=twitter_list.owner_id, since_id=last_id.twitter_id, list_id=twitter_list.list_id, count=200).items():
            tweets.append(status)
    else:
        # first run on empty database
        for status in tweepy.Cursor(api.list_timeline, tweet_mode='extended', owner_id=twitter_list.owner_id, list_id=twitter_list.list_id, count=200).items():
            tweets.append(status)

    return tweets


def list_members(twitter_list):
    api = twitter_auth.autentica_list()

    members = []

    for member in tweepy.Cursor(api.list_members, owner_id=twitter_list.owner_id, list_id=twitter_list.list_id, count=200).items():
        members.append(member)

    return members  

def get_tweets(tweets_ids):
    api = twitter_auth.autentica_list()

    ids = []
    for tweet in tweets_ids:
        ids.append(str(tweet.twitter_id))
    tweets = []
    if len(ids) > 0:
        for status in api.statuses_lookup(ids, trim_user=True, include_entities=False, map_=False):
            tweets.append(status)
    deleted = []
    for id in ids:
        if not any(status.id_str == id for status in tweets):
            deleted.append(id)

    return tweets, deleted


def get_tweets_empty(tweets_ids):
    api = twitter_auth.autentica_list()

    ids = []
    for tweet in tweets_ids:
        ids.append(str(tweet.twitter_id))
    tweets = []
    if len(ids) > 0:
        for status in api.statuses_lookup(ids, trim_user=False, include_entities=True, map_=False, tweet_mode='extended'):
            tweets.append(status)
    deleted = []
    for id in ids:
        if not any(status.id_str == id for status in tweets):
            deleted.append(id)

    return tweets, deleted


def tweet_start():
    print(tweet_texts["inicio_publicacao"].format(horas=datetime.now().isoformat(timespec='minutes')))

def tweet_restricted_start(qt_restricted):
    print(tweet_texts["inicio_contas_restritas"].format(qtde_contas=qt_restricted))

def tweet_restricted(user, previous_status):
    if (user.withheld_scope):
        print(tweet_texts["conta_restrita"].format(nome_user= user.screen_name, tipo_restricao="conteúdo retido"))
    elif (user.protected):
        print(tweet_texts["conta_restrita"].format(nome_user= user.screen_name, tipo_restricao="tweets protegidos"))
    else:
        print(tweet_texts["conta_restrita"].format(nome_user= user.screen_name, tipo_restricao=""))
    

def tweet_start_user(user):
    print(tweet_texts["inicio_arroba"].format(nome=user.name))

def tweet_end_user(user, qt_tweets, previous_status):
    print(tweet_texts["fim_arroba"].format(nome=user.name, qtde_tuites=qt_tweets))

def tweet_erased(tweet, previous_status):
    print(tweet_texts["apagado_inicio"].format(id=tweet.twitter_id, created_at=tweet.created_at, interval=tweet.erased_at - tweet.created_at))
    print(tweet_texts["apagado_texto"].format(tweet=tweet.text[0:200]))

def tweet_end(qtde_tweets):
    print(tweet_texts["fim_publicacao"].format(qtde_tweets=qtde_tweets))
    print(tweet_texts["fim_site"])
    print(tweet_texts["fim_newsletter"])
    print(tweet_texts["fim_apoios"])
