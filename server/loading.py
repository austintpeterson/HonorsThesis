#for loading anything the server needs

import pickle
import pandas as pd
import os.path
import csv


#loads up pickled classifier from /classifiers/ dir
def load_clf(clf_name):
	load_name = clf_name+".pkl"
	my_path = os.path.dirname(os.path.abspath(__file__))
	clf_unpickle = open(my_path+"/classifiers/"+load_name, 'rb')
	text_clf = pickle.load(clf_unpickle)

	return text_clf



def assure_csv_exists(username):
	my_path = os.path.dirname(os.path.abspath(__file__))
	file_path = my_path+"/data/user_tweets/"+username+".csv"

	if os.path.exists(file_path):
		#print("file exists")
		return True
	else:
		#print("file doesnt exist")
		return False



#loads follower lists
#returns list of followers
def load_followers(username):
	my_path = os.path.dirname(os.path.abspath(__file__))

	with open(my_path+"/data/follower_lists/"+username+".csv") as file:
		reader = csv.reader(file, delimiter = ',')

		#skip header
		next(reader, None)

		followers = []

		i = 0
		for row in reader:
			screen_name = row[1]
			#assure follower has accompanying user_tweets csv
			#doing here so I have a clean follower list when building results
			file_exists = assure_csv_exists(screen_name)

			if file_exists:
				followers.append(screen_name)

		return followers






#loads tweets for user into df
def load_tweets(username):
	my_path = os.path.dirname(os.path.abspath(__file__))

	with open(my_path+"/data/user_tweets/"+username+".csv") as file:
		reader = csv.reader(file, delimiter = ',')

		#skip header
		next(reader, None)

		tweets = []

		i = 0
		for row in reader:
			tweet = row[1]
			#don't have to assure that file exists, 
			#won't be written without tweets available

			tweets.append(tweet)

		return tweets





