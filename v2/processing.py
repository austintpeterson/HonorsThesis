import csv
import os.path
import string

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
						#need to disqualify tweets?

						#preprocess tweets
						proc_tweet_text = process_tweet(tweet_text)

						my_df.loc[len(my_df)] = [botornot, proc_tweet_text]

						i += 1
						
			
			#handle fact that some users on original user list were suspended before
			#tweets could be collected.  Disregard user.
			except FileNotFoundError:
				print("no tweet data file found for @"+screen_name+", not loading user tweets.")

		print("# of tweets loaded: "+str(i))
	
	#return a dataframe
	#[class (bot or not), text]x(# of users)
	return my_df



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

	print("best score grid search: "+str(gs_clf.best_score_))
	print("best params grid search: "+str(gs_clf.best_params_))





#extracted so that different methods of scoring can be added
def score():
	#todo
	#f1 score
	#cross validation
	
	i = 0#placehold









#used to apply nl processing to tweet
#takes in tweet text string and returns processes tweet text
#(future: can be modified later to return tokenized lists)
#REDO ALL THIS LATER ========================================
#currently doesn't change scores at all, not used
def process_tweet(tweet_text):
	processed_tweet_text = ''








	#implement eventually**
	return tweet_text









