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

#my stuff
import importlib
import processing

#I am an idiot
import warnings
warnings.filterwarnings("ignore")


#tests combos of classifiers and vectorizers, shows resulting scores
#todo - modify this to run like original ml.py - with a pipeline
def perform(classifiers, vectorizers, train_data, test_data):
	bestAccuracy = 0.0
	bestClf = ""
	bestVct = ""

	for classifier in classifiers:
		for vectorizer in vectorizers:
			
			
			text_clf = Pipeline([
				('vect', vectorizer),#can add stop_words='english' to params
				('tfidf', TfidfTransformer()),
				('clf', classifier),
				])
			
			#testing
			text_clf.fit(train_data.text, train_data.bot)

			#predict
			predicted = text_clf.predict(test_data.text)
			accuracy = np.mean(predicted == test_data.bot)
			

			string = ''
			#wanna see if they are different
			string += classifier.__class__.__name__ + ' with ' + vectorizer.__class__.__name__


			#todo - score this the 'real average' way, with positive negs accted for.


			string += '\nprediction: '+str(accuracy)

			print(string)
			print("")

			#save best performers
			if accuracy > bestAccuracy:
				bestAccuracy = accuracy
				bestClf = classifier.__class__.__name__
				bestVct = vectorizer.__class__.__name__

	print("best combo: "+bestClf+", "+bestVct+": "+str(bestAccuracy))




def main():
	target_user_list = input("target user csv: ")
	target_tweet_dir = input("target tweet directory: ")

	#INTERMEDIATE REPRESENTATION & PROCESSING
	#assigns user classifications to user tweets
	data_list = processing.load_data(target_user_list+".csv", target_tweet_dir)


	#todo: implement test_train_split?

	#determine split amt between train and test
	train_seg = .8 #todo: this can be changed/tuned later(user input?)
	test_seg = 1-float(train_seg)

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
		MultinomialNB(),
		BernoulliNB(),
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
		HashingVectorizer(non_negative=True)
    ],
	    train_data,
	    test_data
	)





main()
























