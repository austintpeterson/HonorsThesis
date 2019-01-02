#4

import tweepy
import csv
import os.path
import time

#getting api keys
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)
 
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def main():
	file_str = input("choose flagged csv to collect for: ")
	file_str2 = file_str+".csv"
	amt = int(input("how many tweets per user?: "))
	target_folder = input("target folder: ")

	#auth
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#open user csv
	#todo: with makes sure file closes.  Implement on all scripts
	with open(file_str2, "r") as file:
		reader = csv.reader(file, delimiter = ',')
		next(reader, None)#skip header

		path = os.path.dirname(os.path.abspath(__file__))+"/"+target_folder+"/"

		#per user
		i = 0
		for row in reader:
			#get user screen_name
			screen_name = row[1]
			print(str(i)+": scraping "+str(amt)+" tweets from @"+screen_name+"...")
			
			#need to instantiate here for null check
			user_tweets = []

			try:
				#call api to get tweets
				user_tweets = api.user_timeline(screen_name = screen_name, count=amt, tweet_mode="extended")#count = 200

			except tweepy.error.RateLimitError as e:
				print(bcolors.WARNING+"rate limit reached.  sleeping."+bcolors.ENDC)
				#wait and then call again.
				#was iterating with dead api, not getting tweets
				time.sleep(60*15)
				print("resumed.")
				user_tweets = api.user_timeline(screen_name = screen_name, count=amt, tweet_mode="extended")

			except tweepy.error.TweepError:
				print(bcolors.WARNING+"tweep error, not scraping tweets for user."+bcolors.ENDC)

			except Exception as e:
				print(bcolors.WARNING+"an unspecified error occured"+bcolors.ENDC)
				print("error: "+str(e))
				#blocks so I can figure out the problem
				user_input = input("continue? ")
			

			#deal w users that have since been suspended/no tweets (tweepy err!!)
			#check if user_tweets is empty/null, and don't generate the file if so
			
			#TODO: deal with the fact that ml will look for a user tweets data file that is not there

			if not user_tweets:
				print(bcolors.WARNING+"no tweets data file built for @"+screen_name+bcolors.ENDC)
			else:
				#todo: don't overwrite existing tweets_data file
				#(for incomplete tweet_scraper runs, users left to run in _r_0.0 file)

				newfile = open(path+screen_name+".csv", "w")#path needed
				writer = csv.writer(newfile, delimiter = ',')
				#header
				writer.writerow(['id', 'text'])
				
				ti = 0
				for tweet in user_tweets:
					print(tweet.id)
					print("     "+str(ti)+": "+tweet.full_text)
					#print("")
					writer.writerow([tweet.id, tweet.full_text])
					ti += 1



			print("")

			i += 1







main()




















