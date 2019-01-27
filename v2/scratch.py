#testing

from twitterscraper import query_tweets

#scrape from specific user
# -l is limit
list_of_tweets = query_tweets("-u realDonaldTrump -l 20", 20)

i = 0
for tweet in list_of_tweets:
	print(tweet.text)
	i += 1

print("# of tweets: "+str(i))









