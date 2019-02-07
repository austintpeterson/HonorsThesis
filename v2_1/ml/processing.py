import csv
import os.path
import string

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import *

import pandas as pd

from sklearn.model_selection import GridSearchCV



#loads tweets by retrieving all classified users from a csv file,
#and then loading the tweets from the corresponding user csv in the
#target tweets data directory
def load_data(target_user_list, target_tweet_dir):
	path = os.path.dirname(os.path.abspath(__file__))

	#open user list
	with open(target_user_list, "r") as user_list_file:
		reader = csv.reader(user_list_file, delimiter = ',')
		next(reader, None)#skip header

		#new load data
		col_names = ['bot', 'text']
		my_df = pd.DataFrame(columns = col_names)

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

						my_df.loc[len(my_df)] = [botornot, tweet_text]#preproptext

						i += 1
			
			#handle fact that some users on original user list were suspended before
			#tweets could be collected.  Disregard user.
			except FileNotFoundError:
				print("no tweet data file found for @"+screen_name+", not loading user tweets.")

		print("# of tweets loaded: "+str(i))
	
	#return a dataframe
	#[class (bot or not), text]x(# of users)
	return my_df






def preprocess_data(data_list):
	#new load data
	col_names = ['bot', 'text']
	my_df = pd.DataFrame(columns = col_names)

	#spin thru all tweets
	for entry in data_list:
		tweet_text = entry.text





def is_valid_data(tweet_text):
	i = 0
	return








def perform_gs(train_data, text_clf):
	#text then bot

	#change later
	# parameters = {'tfidf__ngram_range': [(1, 1), (1, 2)],
	# 			'tfidf__use_idf': (True, False),
	# 			'tfidf__max_df': [0.25, 0.5, 0.75, 1.0],
	# 			'tfidf__max_features': [10, 50, 100, 250, 500, 1000, None],
	# 			'tfidf__stop_words': ('english', None),
	# 			'tfidf__smooth_idf': (True, False),
	# 			'tfidf__norm': ('l1', 'l2', None),
	# 			}

	#vect params:
	#tfidf params:
	#clf params:


	
	#print("GRID SEARCH")
	parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
	'vect__stop_words': ('english', None),
	'tfidf__use_idf': (True, False),
	'clf__alpha': (1e-2, 1e-3),
	}

	gs_clf = GridSearchCV(text_clf, parameters, n_jobs=1, cv = 3)#can pass scoring type
	gs_clf = gs_clf.fit(train_data.text, train_data.bot)
	gs_clf2 = gs_clf.predict()

	print("best score grid search: "+str(gs_clf.best_score_))
	print("best params grid search: "+str(gs_clf.best_params_))








#extracted so that different methods of scoring can be added
def score():
	#todo
	#f1 score
	#cross validation
	
	i = 0#placehold









#used to apply nl processing to tweet
#find way to use in classifier pipeline, not load_data
#NOT USED
# def preprocess_tweet(text):
	
# 	document = ""

# 	#
# 	for sen in range(0, len(text)):  
# 	    # Remove all the special characters
# 	    document = re.sub(r'\W', ' ', str(text[sen]))

# 	    # remove all single characters
# 	    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

# 	    # Remove single characters from the start
# 	    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 

# 	    # Substituting multiple spaces with single space
# 	    document = re.sub(r'\s+', ' ', document, flags=re.I)

# 	    # Removing prefixed 'b'
# 	    document = re.sub(r'^b\s+', '', document)

# 	    # Converting to Lowercase
# 	    document = document.lower()

# 	    # Lemmatization
# 	    document = document.split()

# 	    document = [WordNetLemmatizer().lemmatize(word) for word in document]
# 	    document = ' '.join(document)

# 	    #documents.append(document)



# 	return document









