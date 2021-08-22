if __name__ == '__main__':
    import lists

    twitter_lists = lists.get_all()

    for twitter_list in twitter_lists:
        lists.get_members(twitter_list)
