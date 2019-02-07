#beginnings of some ml

import csv
import os.path
import string

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

from sklearn.model_selection import train_test_split 

#ml
import pandas as pd
from sklearn.naive_bayes import * #multinomialFB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import *
#from sklearn.svm import *
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import FunctionTransformer

from sklearn.model_selection import GridSearchCV

import numpy as np

#cross validation/scoring stuff
#from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score

#my stuff
import importlib
import processing





#move/fix
def get_text_length(x):
    return np.array([len(t) for t in x]).reshape(-1, 1)




def main():
	target_user_list = input("target user csv: ")
	target_tweet_dir = input("target tweet directory: ")

	#INTERMEDIATE REPRESENTATION & PROCESSING
	#assigns user classifications to user tweets
	data_list = processing.load_data(target_user_list+".csv", target_tweet_dir)

	#
	data_list = processing.preprocess_data(data_list)

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

	#ML
	#training
	#note: tfidf - term freq and inverse doc freq
	#no pipeline in ml_old, traditional fit/predict arch.
	#first V2 choice
	# text_clf = Pipeline([
	# 	('vect', CountVectorizer()),#can add stop_words='english' to params
	# 	('tfidf', TfidfTransformer()),#figure this out better
	# 	('clf', MultinomialNB()),
	# 	])

	text_clf = Pipeline([
		('features', FeatureUnion([
			('text', Pipeline([
				('vect', CountVectorizer(min_df=1,max_df=2)),#new params
				('tfidf', TfidfTransformer()),
			])),
			('length', Pipeline([
				('count', FunctionTransformer(get_text_length, validate = False)),
			]))
		])),
		('clf', MultinomialNB())
	])




	#3
	#use vect/classifier multiplexer system here to find best combo
	#its in old ml learning code somewhere

	#testing
	text_clf.fit(train_data.text, train_data.bot)
	#predict
	predicted = text_clf.predict(test_data.text)
	print("CountVectorizer score:" + str(np.mean(predicted == test_data.bot)))#0.8904761 no matter what





	#new grid search
	#processing.perform_gs(train_data, text_clf)





	









	
























main()


