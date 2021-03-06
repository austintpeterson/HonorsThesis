#beginnings of some ml

import csv
import os.path
import string

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

#ml
import pandas as pd
from sklearn.naive_bayes import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import *
from sklearn.svm import *

#called in the load_data
#return 0 if tweet text doesn't meet standards
#(not english, just a url, etc)
def disqualify_tweet(tweet_text):
	#todo: check if english
	#check if just a url

	#else return 0
	return tweet_text

#used to apply nl processing to tweet
#takes in tweet text string and returns processes tweet text
#(future: can be modified later to return tokenized lists)
#REDO ALL THIS LATER ========================================
#currently doesn't change scores at all
def process_tweet(tweet_text):
	#tokenize
	tokens = nltk.word_tokenize(tweet_text)

	#lemmatization
	lmtzr = WordNetLemmatizer()

	lemm_tokens = [lmtzr.lemmatize(t) for t in tokens]#lemmatized_text = ' '.join([lmtzr.lemmatize(t) for t in tokens])

	#stop words
	#
	filtered_tokens = [word for word in lemm_tokens if word not in stopwords.words('english')]

	#rejoin tokens for vectorizer format
	#todo: figure out how to tokenize fully before handing to vectorizer
	processed_tweet_text = ' '.join(filtered_tokens)

	#punctuation strip
	processed_tweet_text = "".join((char for char in processed_tweet_text if char not in string.punctuation))

	return processed_tweet_text



#loads tweets by retrieving all classified users from a csv file,
#and then loading the tweets from the corresponding user csv in the
#target tweets data directory
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

			try:
				#get tweets for the user
				with open(path+"/"+target_tweet_dir+"/"+screen_name+".csv") as tweet_file:
					tweet_reader = csv.reader(tweet_file, delimiter = ',')
					next(tweet_reader, None)#skip header

					for row in tweet_reader:
						tweet_text = row[1]
						#preprocess tweets by disqualifying any tweets that aren't helpful
						pre_tweet_text = disqualify_tweet(tweet_text)
						
						#todo: switch disqualify_tweet to return null or best practice to check, (not 0?)
						if pre_tweet_text != 0:	
							tup = (botornot, pre_tweet_text)
							#append tuple to array
							tweet_list.append(tup)
							i += 1
						else:
							print("tweet skipped")
			
			#handle fact that some users on original user list were suspended before
			#tweets could be collected.  Disregard user.
			except FileNotFoundError:
				print("no tweet data file found for @"+screen_name+", not loading user tweets.")

		print("# of tweets loaded: "+str(i))
	
	#return a list of tuples 
	#[class (bot or not), text]x(# of users)
	return tweet_list




def main():
	target_user_list = input("target user csv: ")
	target_tweet_dir = input("target tweet directory: ")

	#INTERMEDIATE REPRESENTATION & PROCESSING
	#assigns user classifications to user tweets
	data_list = load_data(target_user_list+".csv", target_tweet_dir)


	col_names = ['bot', 'text']
	my_df = pd.DataFrame(columns = col_names)

	#add returned data_list to dataframe, process text
	for item in data_list:
		
		#insert new_text into dataframe instead
		new_text = process_tweet(item[1])

		#load user item into dataframe
		#print("loading dataframe: "+item[0]+" "+new_text)
		my_df.loc[len(my_df)] = [item[0], new_text]



	#determine split amt between train and test
	train_seg = .8#todo: this can be changed/tuned later(user input?)
	test_seg = 1-float(train_seg)#not used

	data_list_size = len(data_list)

	train_amt = int(train_seg*float(data_list_size))#int cast will floor float
	print("amt of tweets to be used in training: "+str(train_amt))

	#split data
	train_data = my_df[:train_amt]
	test_data = my_df[train_amt:]





	#ML
	#training
	classifier = OneVsRestClassifier(SVC(kernel='linear'))#todo: want multinom or nominal
	vectorizer = TfidfVectorizer()#todo: want Count vect later (cross test them all)

	vectorize_text = vectorizer.fit_transform(train_data.text)
	#can use vectorize_text.shape to see dimensions of vect:
	print("shape of vectorizer:"+str(vectorize_text.shape))
	classifier.fit(vectorize_text, train_data.bot)

	# score
	vectorize_text = vectorizer.transform(test_data.text)
	score = classifier.score(vectorize_text, test_data.bot)
	
	#outputs accuracy score
	print("accuracy score from classifier: "+str(score)) # .5571




























main()


