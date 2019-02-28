#4

import tweepy
import csv
import os.path
import time
import string

#getting api keys
import os
import os.path
from os.path import join, dirname
from dotenv import load_dotenv

from sys import argv
import log

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

#check tweets dir exists, create if not
#todo: THIS IS BROKEN, FIX
#update: probably not broken
def assure_path_exists(path):
		my_dir = os.path.dirname(path)
		
		if not os.path.exists(my_dir):
			print("directory DNE")
			#build directory
			os.makedirs(my_dir)
		else:
			print("directory exists")



def main():
	file_str = argv[1]#input("choose flagged csv to collect for: ")
	file_str_ext = file_str+".csv"
	amt = int(argv[2])#input("how many tweets per user?: "))
	#user used to be able select target
	#defaults to user_collection csv file name if none given
	target_folder = ""#argv[3]#input("target folder (enter if default): ")



	#auth
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)



	#pathways
	my_path = os.path.dirname(os.path.abspath(__file__))
	parent_path = os.path.abspath(os.path.join(my_path, os.pardir))



	#set target folder to default if needed
	if target_folder == "":
		target_folder = file_str.split("_")[0]#simple name
		#print("target folder: "+target_folder)
		#print("parent: "+parent_path)

	assure_path_exists(parent_path+"/tweets_collections/"+target_folder+"/")



	#open user csv
	#todo: with makes sure file closes.  Implement on all scripts
	with open(parent_path+"/user_collections/"+file_str_ext, "r") as file:
		reader = csv.reader(file, delimiter = ',')
		next(reader, None)#skip header

		path = parent_path+"/tweets_collections/"+target_folder+"/"

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
			


			if not user_tweets:
				print(bcolors.WARNING+"no tweets data file built for @"+screen_name+bcolors.ENDC)
			else:
				#todo: don't overwrite existing tweets_data file
				#(for incomplete tweet_scraper runs, users left to run in _r_0.0 file)

				newfile = open(path+screen_name+".csv", "w+")#path needed
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

				#write to log file
				log.write(str(i)+": created "+screen_name+".csv")



			print("")

			i += 1







main()




















