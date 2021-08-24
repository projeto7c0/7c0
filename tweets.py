import twitter
from database import recupera_ids
from database import update_tweets_db



def update_tweets(minutes):
    tweets = recupera_ids(minutes)
    print(len(tweets))

    if len(tweets) > 100:
        id_groups = split(tweets, 1+len(tweets)//100)
    else:
        id_groups = [tweets]
    if minutes > 0:
        for id_group in id_groups:
            updated_tweets, deleted = twitter.get_tweets(id_group)
            update_tweets_db(updated_tweets, deleted)
    else:
        for id_group in id_groups:
            updated_tweets, deleted = twitter.get_tweets(id_group)
            updated_tweets = []
            update_tweets_db(updated_tweets, deleted)



def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
