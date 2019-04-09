#library for all the server scraping stuff

import csv
import tweepy
import datetime
import time

#getting api keys
import os
import os.path
from os.path import join, dirname
from dotenv import load_dotenv

#load env variables
dotenv_path = join(dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)
 
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')

#path stuff
my_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(my_path, os.pardir))


#todo - swap all file writing to 'with open' for closing
#https://stackoverflow.com/questions/3347775/csv-writer-not-closing-file

#username - user to scrape tweets for
#amt - amt of tweets to scrape
#returns if tweets successfully found
def scrape_tweets(username, amt):
	#tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	"""
	#set up file
	#file = open(parent_path+"/server/data/user_tweets/"+username+".csv", "w")
	#writer = csv.writer(file, delimiter = ",")

	#writer.writerow(['id', 'text'])
	"""

	#
	user_tweets = []

	try:
		user_tweets = api.user_timeline(screen_name = username, count = amt, tweet_mode = "extended")

	except tweepy.error.RateLimitError:
		print("tweepy error/limit.  sleeping.")
		time.sleep(60*15)
		print("resumed.")
		user = next(users)

	except tweepy.error.TweepError:
		#todo - make sure to load correctly
		print("tweep err.  not scraping for "+username)

	except Exception as e:
		print("unspecified error")

	if not user_tweets:
		print("no tweet data file built for "+username)
		#returns false b/c not successful tweet retrieval
		return False

	else:
		file = open(my_path+"/data/user_tweets/"+username+".csv", "w")
		writer = csv.writer(file, delimiter = ",")

		writer.writerow(['id', 'text'])

		ti = 0
		for tweet in user_tweets:
			writer.writerow([tweet.id, tweet.full_text])
			ti += 1

		#returns true because at least one tweet written
		if ti > 0:
			return True



#username - user to scrape followers for
#amt - amt of followers to scrape for user
def scrape_followers(username, amt):
	#tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	users = tweepy.Cursor(api.followers, screen_name = username, count = amt).items()

	#set up file
	#csv contains list of followers for a given username supplied by user
	file = open(my_path+"/data/follower_lists/"+username+".csv", "w")
	writer = csv.writer(file, delimiter = ",")

	writer.writerow(['id', 'screen_name', 'name', 'date_created'])

	i = 0
	while i < amt:
		try:
			#using a cursor, so can get exact amt of followers needed,
			#despite failing 
			user = next(users)

		except StopIteration:
			#todo - log errors
			print("file iteration error")
			break;

		except tweepy.error.RateLimitError:
			print("tweepy error/limit.  sleeping.")
			time.sleep(60*15)
			print("resumed.")
			user = next(users)

		except Exception as e:
			print("unspecified error")

		#todo - log 

		#write to csv
		date_created = datetime.datetime.now()
		writer.writerow([str(user.id), user.screen_name, user.name, str(date_created)])

		#implement scrape_tweets for each follower here
		#todo - find a way to pass API auth to cut down on time
		successful_tweets = scrape_tweets(user.screen_name, amt)
		
		#only increments if tweets were found
		if successful_tweets:
			i += 1



#this is the outermost scraping method
def get_tweets(username, follower_amt, tweet_amt):
	#get tweets for username supplied
	scrape_tweets(username, tweet_amt)

	#get followers for user
	scrape_followers(username, follower_amt)
		#(this implements scrape_tweets as well)

































