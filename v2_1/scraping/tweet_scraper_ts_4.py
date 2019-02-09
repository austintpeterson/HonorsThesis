#4
#todo: talk about moving away from API in final ____

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

from twitterscraper import query_tweets

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
def assure_path_exists(path):
		my_dir = os.path.dirname(path)
		
		if not os.path.exists(my_dir):
			print("directory DNE")
			#build directory
			os.makedirs(my_dir)
		else:
			print("directory exists")


def get_user_tweets(screen_name, amt):

	#todo: fix limit issue
	user_tweets = query_tweets("-u "+screen_name,10)#" -l "+str(amt)+" lang:en"

	if user_tweets is None:
		#return None if no tweets found
		return None
	elif len(user_tweets) == 0:
		return None
	else:
		return user_tweets



def main():
	file_str = input("choose flagged csv to collect for: ")
	file_str2 = file_str+".csv"
	amt = int(input("how many tweets per user?: "))
	#user used to be able select target
	#defaults to user_collection csv file name if none given
	target_folder = input("target folder (enter if default): ")



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
	with open(parent_path+"/user_collections/"+file_str2, "r") as file:
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
				user_tweets = get_user_tweets(screen_name, amt)

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
					print("     "+str(ti)+": "+tweet.text)
					#print("")
					writer.writerow([tweet.id, tweet.text])
					ti += 1



			print("")

			i += 1







main()

