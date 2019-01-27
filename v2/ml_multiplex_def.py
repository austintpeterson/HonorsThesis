from sklearn.naive_bayes import *
from sklearn.dummy import *
from sklearn.ensemble import *
from sklearn.neighbors import *
from sklearn.tree import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.calibration import *
from sklearn.linear_model import *
from sklearn.multiclass import *
from sklearn.svm import *
from sklearn.pipeline import Pipeline
import pandas

import pandas as pd

import csv
import os.path
import string


from sklearn.model_selection import GridSearchCV

import numpy as np


#tests combos of classifiers and vectorizers, shows resulting scores
#todo - modify this to run like original ml.py - with a pipeline
def perform(classifiers, vectorizers, train_data, test_data):
	for classifier in classifiers:
		for vectorizer in vectorizers:
			

			# string = ""
			# string += classifier.__class__.__name__ + ' with ' + vectorizer.__class__.__name__

			# # train
			# vectorize_text = vectorizer.fit_transform(train_data.text)
			# classifier.fit(vectorize_text, train_data.bot)

			# # score
			# vectorize_text = vectorizer.transform(test_data.text)
			# score = classifier.score(vectorize_text, test_data.bot)
			# string += ' - Has score: ' + str(score)
			# print(string)

			text_clf = Pipeline([
				('vect', vectorizer),#can add stop_words='english' to params
				#H - Transformer needed in this type of dev bc no negative vals allowed in classifiers
				('tfidf', TfidfTransformer()),#figure this out better
				('clf', classifier),
				])

			#testing
			text_clf.fit(train_data.text, train_data.bot)

			#predict
			predicted = text_clf.predict(test_data.text)
			#score = text_clf.score(test_data.text)
			string = ''
			#wanna see if they are different
			string += classifier.__class__.__name__ + ' with ' + vectorizer.__class__.__name__
			#string += '\nscore: + '+ str(score) + '\npredicted: ' + str(predicted)
			#todo - score this the 'real average' way, with positive negs accted for.
			string += '\npredicted: '+str(np.mean(predicted == test_data.bot))

			print(string)



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
						#preprocess tweets by disqualifying any tweets that aren't helpful
						#pre_tweet_text = disqualify_tweet(tweet_text)

						my_df.loc[len(my_df)] = [botornot, tweet_text]

						i += 1
						
			
			#handle fact that some users on original user list were suspended before
			#tweets could be collected.  Disregard user.
			except FileNotFoundError:
				print("no tweet data file found for @"+screen_name+", not loading user tweets.")

		print("# of tweets loaded: "+str(i))
	
	#return a dataframe
	#[class (bot or not), text]x(# of users)
	return my_df








def main():
	target_user_list = input("target user csv: ")
	target_tweet_dir = input("target tweet directory: ")

	#INTERMEDIATE REPRESENTATION & PROCESSING
	#assigns user classifications to user tweets
	data_list = load_data(target_user_list+".csv", target_tweet_dir)




	#determine split amt between train and test
	train_seg = .8 #todo: this can be changed/tuned later(user input?)
	test_seg = 1-float(train_seg) #not currently needed

	data_list_size = len(data_list)

	train_amt = int(train_seg*float(data_list_size))#int cast will floor float
	print("amt of tweets to be used in training: "+str(train_amt))

	#split data
	train_data = data_list[:train_amt]
	test_data = data_list[train_amt:]



	#ml calls
	#note - will implement/embed with tfidf transformer

	perform(
	[
		BernoulliNB(),
		#MultinomialNB(), - not working here
		RandomForestClassifier(n_estimators=100, n_jobs=-1),
		AdaBoostClassifier(),
		BaggingClassifier(),
		ExtraTreesClassifier(),
		GradientBoostingClassifier(),
		DecisionTreeClassifier(),
		CalibratedClassifierCV(),
		DummyClassifier(),
		PassiveAggressiveClassifier(),
		RidgeClassifier(),
		RidgeClassifierCV(),
		SGDClassifier(),
		OneVsRestClassifier(SVC(kernel='linear')),
		OneVsRestClassifier(LogisticRegression()),
		KNeighborsClassifier()
    ],
    [
		CountVectorizer(),
		TfidfVectorizer(),
		HashingVectorizer()
    ],
	    train_data,
	    test_data
	)






main()
























