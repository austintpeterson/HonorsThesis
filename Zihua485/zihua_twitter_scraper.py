from twitterscraper import query_tweets

if __name__ == '__main__':
    # list_of_tweets = query_tweets("Trump OR Clinton", 10)

    #print the retrieved tweets to the screen:
    # for tweet in query_tweets("Trump OR Clinton", 10):
    #     print(tweet)

    #Or save the retrieved tweets to file:
    file = open("Tweets.json", "w", encoding="utf-8")
    for tweet in query_tweets("Trump OR Clinton", 10):
        file.write(tweet)
    file.close()