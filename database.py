from alchemy import List, Tweet, User, Hashtag, Mention, Url
from json import load

from datetime import timedelta,datetime

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

with open("config.json") as jsonfile:
    db_config = load(jsonfile)['database_dml']

engine = create_engine(URL(db_config['drivername'], db_config['username'],
                           db_config['password'], db_config['host'],
                           db_config['port'], db_config['database']))


def insere_lista(tweets, twitter_list):
    Session = sessionmaker(bind=engine)
    session = Session()

    for tweet in tweets:
        old_tweet = session.query(Tweet).filter_by(twitter_id = tweet.id_str).filter_by(list_id=twitter_list.id).first()
        if not old_tweet:
            user = session.query(User).filter_by(list_id=twitter_list.id).filter_by(twitter_user_id=tweet.user.id_str).first()
            if (user):
                new_tweet = Tweet(text=tweet.full_text,
                            twitter_id=tweet.id_str,
                            list_id=twitter_list.id,
                            user_id = user.id,
                            twitter_user_id = tweet.user.id_str,
                            created_at = tweet.created_at,
                            favorite_count = tweet.favorite_count,
                            is_quote = tweet.is_quote_status,
                            is_retweet = hasattr(tweet, 'retweeted_status'),
                            quoted_status_id = tweet.quoted_status_id_str if hasattr(tweet, 'quoted_status_id_str') else None,
                            retweet_count = tweet.retweet_count,
                            reply_to_screen_name = tweet.in_reply_to_screen_name,
                            reply_to_status_id = tweet.in_reply_to_status_id_str,
                            in_reply_to_status_id = tweet.in_reply_to_status_id_str,
                            retweeted_status_id = tweet.retweeted_status.id_str if hasattr(tweet, 'retweeted_status') else None,
                            reply_count = tweet.reply_count if hasattr(tweet, 'reply_count') else None,
                            five_min_check = True,
                            hourly_check = True,
                            daily_check = True,
                            weekly_check = True,
                            erased = False,
                            bot_tweeted = False
                            )
                session.add(new_tweet)
                session.flush()

                for hashtag in tweet.entities['hashtags']:
                    new_hashtag = Hashtag(text=hashtag['text'], tweet_id = new_tweet.id)
                    session.add(new_hashtag)

                for mention in tweet.entities['user_mentions']:
                    new_mention = Mention(user_str_id=mention['id_str'], screen_name=mention['screen_name'], tweet_id = new_tweet.id)
                    session.add(new_mention)

                for url in tweet.entities['urls']:
                    new_url = Url(url=url['expanded_url'], tweet_id = new_tweet.id)
                    session.add(new_url)

    session.commit()
    session.close()


def get_all_lists():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(List).all()


def get_all_users(exclude_blocked):
    Session = sessionmaker(bind=engine)
    session = Session()
    if (exclude_blocked):
        return session.query(User).filter(User.protected==False).filter(User.active==True).all()
    else:
        return session.query(User).all()


def get_restricted_users():
    Session = sessionmaker(bind=engine)
    session = Session()
    if (exclude_blocked):
        return session.query(User).filter(User.protected==False).filter(User.active==True).all()
    else:
        return session.query(User).all()


def get_users_that_removed():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(User).filter(User.protected==False).filter(User.active==True).all()


def recupera_ids_total(list):
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(Tweet).filter_by(list_id=list.id).order_by(Tweet.twitter_id.desc()).first()


def prepara_atualizacao():
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(User).update({User.updated:False}, synchronize_session = False)
    session.close()


def insere_membros(members, twitter_list):
    Session = sessionmaker(bind=engine)
    session = Session()

    for member in members:
        user = session.query(User).filter_by(twitter_user_id=member.id_str).filter_by(list_id=twitter_list.id).first()
        if (user == None):
            new = User(list_id=twitter_list.id,
                   twitter_user_id=member.id_str,
                   screen_name=member.screen_name,
                   name = member.name,
                   num_followers = member.followers_count,
                   num_friends = member.friends_count,
                   bio = member.description,
                   withheld_scope = member.withheld_scope if hasattr(member, 'withheld_scope') else None,
                   updated = True,
                   protected = member.protected,
                   verified = member.verified,
                   active = True
                   )
            session.add(new)
    session.commit()
    session.close()


def atualiza_membros(members):
    Session = sessionmaker(bind=engine)
    session = Session()

    for member in members:
        users = session.query(User).filter_by(twitter_user_id=member.id_str).all()
        for user in users:
            user.num_followers = member.followers_count
            user.num_friends = member.friends_count
            user.name = member.name
            user.screen_name = member.screen_name
            user.bio = member.description
            user.active = user.updated = True
            user.protected = member.protected
            user.verified = member.verified


    session.commit()


def deleta_membros():
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(User).filter_by(updated=False).update({User.active:False})

    session.commit()
    session.close()


def recupera_ids(minutes):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    if minutes > 0:
        return session.query(Tweet).filter(Tweet.erased == False).filter(Tweet.created_at >= datetime.utcnow()-timedelta(minutes=minutes)).all()
    else:
        return session.query(Tweet).filter(Tweet.erased == False).all()


def recupera_empty():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    return session.query(Tweet).filter(Tweet.is_retweet == None).all()


def update_tweets_db(updated_tweets, deleted):
    Session = sessionmaker(bind=engine)
    session = Session()

    for updated_tweet in updated_tweets:
        tweet = session.query(Tweet).filter_by(twitter_id=updated_tweet.id_str).first()
        tweet.retweet_count = updated_tweet.retweet_count
        tweet.favorite_count = updated_tweet.favorite_count

    for deleted_id in deleted:
        tweet = session.query(Tweet).filter_by(twitter_id=deleted_id).first()
        tweet.erased = True
        tweet.erased_at = datetime.utcnow()

    session.commit()
    session.close()


def upsert_tweets(updated_tweets, deleted):
    Session = sessionmaker(bind=engine)
    session = Session()

    for updated_tweet in updated_tweets:
        tweet = session.query(Tweet).filter_by(twitter_id=updated_tweet.id_str).first()

        tweet.retweet_count = updated_tweet.retweet_count
        tweet.favorite_count = updated_tweet.favorite_count
        tweet.text=updated_tweet.full_text
        tweet.twitter_user_id = updated_tweet.user.id_str
        tweet.created_at = updated_tweet.created_at
        tweet.favorite_count = updated_tweet.favorite_count
        tweet.is_quote = updated_tweet.is_quote_status
        tweet.is_retweet = hasattr(updated_tweet, 'retweeted_status')
        tweet.quoted_status_id = updated_tweet.quoted_status_id_str if hasattr(updated_tweet, 'quoted_status_id_str') else None
        tweet.retweet_count = updated_tweet.retweet_count
        tweet.reply_to_screen_name = updated_tweet.in_reply_to_screen_name
        tweet.reply_to_status_id = updated_tweet.in_reply_to_status_id_str
        tweet.in_reply_to_status_id = updated_tweet.in_reply_to_status_id_str
        tweet.retweeted_status_id = updated_tweet.retweeted_status.id_str if hasattr(updated_tweet, 'retweeted_status') else None
        tweet.reply_count = updated_tweet.reply_count if hasattr(updated_tweet, 'reply_count') else None
        tweet.five_min_check = True
        tweet.hourly_check = True
        tweet.daily_check = True
        tweet.weekly_check = True
        tweet.bot_tweeted = False

    session.commit()
    session.close()