#2
#used to add a botornot_rt score to each user in a selected csv file
#based on BotOMeter score

#going to use BotOMeter API with Twitter to get done
import botometer
import tweepy
import csv

import time
import sys
from sys import argv

#getting api keys
import os
import os.path
from os.path import join, dirname
from dotenv import load_dotenv



dotenv_path = join(dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)
 
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')

mashape_key = "8HK07BkyjOmshRCv6uHzqpJm73eSp1TUxNVjsnKYKn25VJG2rL"#get API on mashape
#note: don't need to add BotOMeter to Applc.  just need general production mashape key

twitter_app_auth = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'access_token': access_key,
    'access_token_secret': access_secret,
  }

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def get_last_rated(rated_file):
	with open(rated_file, "r") as file:
		reader = csv.reader(file, delimiter = ',')
		next(reader, None)#skip header

		screen_name = None
		#do this more efficiently some day
		for row in reader:
			screen_name = row[1]

		if screen_name == None:
			#get more elegant solution for this
			#todo: either add header or delete file and open differently
			print("_r file is empty, kill it and retry\nexiting...")
			sys.exit(0)

		print("last rated user: "+screen_name)
		return screen_name



def main():
	#user input
	#file_str = input("enter csv file: ")
	#file_str2 = file_str+".csv"

	#using system arguments for now (nohup!)
	file_str = argv[1]
	file_str_ext = file_str+".csv"



	#botometer
	bom = botometer.Botometer(wait_on_ratelimit=True,
		mashape_key=mashape_key,
		**twitter_app_auth)

	#pathways
	my_path = os.path.dirname(os.path.abspath(__file__))
	parent_path = os.path.abspath(os.path.join(my_path, os.pardir))



	with open(parent_path+"/user_collections/"+file_str_ext, "r") as file:
		reader = csv.reader(file, delimiter = ',')
		next(reader, None)#skip header

		#
		r_file = None
		writer = None
		#screen name of last rated use in _r file
		last_rated = ""

		rated_file = parent_path+"/user_collections/"+file_str+"_r.csv"

		#check if _r file exists, find last user rated
		rated_file_exists = os.path.exists(rated_file)
		
		if rated_file_exists:
			print("_r file exists")
			#get last user rated
			last_rated = get_last_rated(rated_file)

			#open file with append
			r_file = open(rated_file, "a")
			writer = csv.writer(r_file, delimiter = ',')

		else:
			#new file
			r_file = open(rated_file, "w")
			writer = csv.writer(r_file, delimiter = ',')
			#new header
			writer.writerow(['id', 'screen_name', 'name', 'date_created', 'botornot_rt', 'bot'])

		i = 0

		#fix this horrible quick fix
		catchingUp = True

		for row in reader:
			
			screen_name = row[1]

			#todo: make sure this works - start appending correctly
			if rated_file_exists and catchingUp:
				if (screen_name != last_rated):
					print("continuing past: "+screen_name)
					continue
				else:
					catchingUp = False
					continue

			#todo: add file flush to ensure new rows get saved
			try:
				print(str(i)+": now sending @"+screen_name+" BotOMeter request...")
				result = bom.check_account("@"+screen_name)
				eng_score = result['scores']['english']

				print("writing @"+screen_name+" to new .csv")
				#insert user and score to new file
				writer.writerow([str(row[0]), row[1], row[2], row[3], str(eng_score)])
				print(bcolors.OKGREEN+"SUCCESS"+bcolors.ENDC)

				r_file.flush()



			#no tweets or content.  skip
			except botometer.NoTimelineError:
				print(bcolors.WARNING+"no tweets on timeline, skipping @"+row[1]+bcolors.ENDC)

			except tweepy.error.TweepError as e:
				print(bcolors.WARNING+"tweep err: "+str(e)+bcolors.ENDC)


			print("")
			i += 1















main()


















