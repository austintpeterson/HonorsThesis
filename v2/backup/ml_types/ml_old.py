#beginnings of some ml

import csv
import os.path

#ml
import pandas as pd
from sklearn.naive_bayes import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import *
from sklearn.svm import *

def load_data(target_user_list, target_tweet_dir):
	path = os.path.dirname(os.path.abspath(__file__))

	#open user list
	with open(target_user_list, "r") as user_list_file:
		reader = csv.reader(user_list_file, delimiter = ',')
		next(reader, None)#skip header

		#tuple list here
		tweet_list = []

		i = 0
		for row in reader:
			screen_name = row[1]
			botornot = row[5]#0 or 1 classification

			#get tweets for the user
			with open(path+"/"+target_tweet_dir+"/"+screen_name+".csv") as tweet_file:
				tweet_reader = csv.reader(tweet_file, delimiter = ',')
				next(tweet_reader, None)#skip header

				for row in tweet_reader:
					tweet_text = row[1]
					tup = (botornot, tweet_text)
					#append tuple to array
					tweet_list.append(tup)
					i += 1

		print("# of tweets loaded: "+str(i))
	
	#return a list of tuples 
	#[class (bot or not), text]x(# of users)
	return tweet_list



def main():
	target_user_list = input("target user csv: ")
	target_tweet_dir = input("target tweet directory: ")

	#"intermediate representation"
	#assigns user classifications to user tweets
	data_list = load_data(target_user_list+".csv", target_tweet_dir)

	#todo: add nlp/nltk here?

	#ml
	col_names = ['bot', 'text']
	my_df = pd.DataFrame(columns = col_names)

	#add returned data_list to dataframe
	#this is the under-developed part
	for item in data_list:
		my_df.loc[len(my_df)] = [item[0], item[1]]



	#determine split amt between train and test
	train_seg = .8#todo: this can be changed/tuned later(user input?)
	test_seg = 1-float(train_seg)#not used

	data_list_size = len(data_list)

	train_amt = int(train_seg*float(data_list_size))#int cast will floor float
	print("amt of tweets to be used in training: "+str(train_amt))

	#split data
	train_data = my_df[:train_amt]
	test_data = my_df[train_amt:]

	#training
	classifier = OneVsRestClassifier(SVC(kernel='linear'))#want multinom or nominal
	vectorizer = TfidfVectorizer()#todo: want Count vect later

	vectorize_text = vectorizer.fit_transform(train_data.text)
	classifier.fit(vectorize_text, train_data.bot)

	



	# score
	vectorize_text = vectorizer.transform(test_data.text)
	score = classifier.score(vectorize_text, test_data.bot)
	
	#outputs accuracy score
	print("accuracy score from classifier: "+str(score)) # .5571


























main()


