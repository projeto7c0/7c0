import tweepy
import twitter_auth


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