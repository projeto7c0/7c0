if __name__ == '__main__':
    import time
    import database
    import twitter

    twitter.tweet_start()

    restricted_users = database.get_restricted_users()

    if (len(restricted_users) > 0):
        previous_status = twitter.tweet_restricted_start(len(restricted_users))
        for user in restricted_users:
            twitter.tweet_restricted(user, previous_status)
    
    user_ids = database.get_users_that_removed()

    tweet_total = tweet_count = 0

    for user_id in user_ids:
        user = database.get_user(user_id)
        previous_status = twitter.tweet_start_user(user)
        tweets = database.get_tweets(user_id)
        for tweet in tweets:
            previous_status = twitter.tweet_erased(tweet, previous_status)
            tweet_total += 1
            tweet_count += 1
        twitter.tweet_end_user(user, len(tweets), previous_status)

        if tweet_count >= 20:
            tweet_count = 0
            time.sleep(3600)

    twitter.tweet_end(tweet_total)