from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class List(Base):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True)
    list_id = Column(Text)
    name = Column(Text)
    owner_id = Column(Text)
    address = Column(Text)

    def __repr__(self):
        return f'List {self.name}'


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    twitter_id = Column(String(32), index=True)
    text = Column(Text)
    twitter_user_id = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime)
    favorite_count = Column(Integer)
    is_quote = Column(Boolean)
    is_retweet = Column(Boolean)
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    reply_count = Column(Integer)
    quote_count = Column(Integer)
    quoted_status_id = Column(Text)
    retweet_count = Column(Integer)
    reply_to_screen_name = Column(Text)
    reply_to_status_id = Column(Text)
    in_reply_to_status_id = Column(Text)
    retweeted_status_id = Column(Text)
    
    five_min_check = Column(Boolean)
    hourly_check = Column(Boolean)
    daily_check = Column(Boolean)
    weekly_check = Column(Boolean)
    erased = Column(Boolean)
    erased_at = Column(DateTime)
    bot_tweeted = Column(Boolean)
    bot_tweeted_at = Column(DateTime)

    UniqueConstraint('twitter_id', 'list_id', name='unique_tweet')

    def __repr__(self):
        return f'Tweet {self.twitter_id}'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    twitter_user_id = Column(Text)
    screen_name = Column(Text)
    handle = Column(Text)
    num_followers = Column(Integer)
    num_friends = Column(Integer)
    bio = Column(Text)
    name = Column(Text)
    updated = Column(Boolean)
    withheld_scope = Column(Text)
    protected = Column(Boolean)
    verified = Column(Boolean)
    active = Column(Boolean)

class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable="False")
    text = Column(Text)


class Mention(Base):
    __tablename__ = 'mentions'

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable="False")
    screen_name = Column(Text)
    user_str_id = Column(Text)


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable="False")
    url = Column(Text)
