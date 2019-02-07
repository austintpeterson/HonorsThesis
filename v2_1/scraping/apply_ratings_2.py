#2
#used to add a botornot_rt score to each user in a selected csv file
#based on BotOMeter score

#going to use BotOMeter API with Twitter to get done
import botometer
import tweepy
import csv

import time

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





def main():
	#user input
	file_str = input("enter csv file: ")
	file_str2 = file_str+".csv"

	leftOff = int(input("enter last @username index if left off (0 for new run): "))

	#botometer
	bom = botometer.Botometer(wait_on_ratelimit=True,
		mashape_key=mashape_key,
		**twitter_app_auth)



	#pathways
	my_path = os.path.dirname(os.path.abspath(__file__))
	parent_path = os.path.abspath(os.path.join(my_path, os.pardir))



	with open(parent_path+"/user_collections/"+file_str2, "r") as file:
		reader = csv.reader(file, delimiter = ',')
		next(reader, None)#skip header




		#
		file = None
		writer = None



		
		#if leftOff used, open file with append
		if leftOff != 0:
			file = open(parent_path+"/user_collections/"+file_str+"_r.csv", "a")
			writer = csv.writer(file, delimiter = ',')
		else:
			#new file i/o
			file = open(parent_path+"/user_collections/"+file_str+"_r.csv", "w")
			writer = csv.writer(file, delimiter = ',')
			#new header
			writer.writerow(['id', 'screen_name', 'name', 'date_created', 'botornot_rt', 'bot'])




		i = 0

		#fix this horrible quick fix
		catchingUp = True

		for row in reader:
			
			#fix this horrible quick fix
			#if leftOff implemented, skip up until the provided @username index
			if (leftOff != 0) and catchingUp:
				if (i != leftOff) or (i < leftOff):
					i += 1
					continue
				else:
					#time.sleep(5)
					catchingUp = False
			###




			screen_name = row[1]

			#eng_score = 0.0
			try:
				print(str(i)+": now sending @"+screen_name+" BotOMeter request...")
				result = bom.check_account("@"+screen_name)
				eng_score = result['scores']['english']

				print("writing @"+screen_name+" to new .csv")
				#insert user and score to new file
				writer.writerow([str(row[0]), row[1], row[2], row[3], str(eng_score)])
				print(bcolors.OKGREEN+"SUCCESS"+bcolors.ENDC)



			#no tweets or content.  skip
			except botometer.NoTimelineError:
				print(bcolors.WARNING+"no tweets on timeline, skipping @"+row[1]+bcolors.ENDC)

			except tweepy.error.TweepError as e:
				print(bcolors.WARNING+"tweep err: "+str(e)+bcolors.ENDC)



			print("")
			i += 1















main()


















