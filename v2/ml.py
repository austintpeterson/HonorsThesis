#beginnings of some ml

import csv
import os.path
import string

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

#ml
import pandas as pd
from sklearn.naive_bayes import * #multinomialFB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import *
from sklearn.svm import *
from sklearn.pipeline import Pipeline

from sklearn.model_selection import GridSearchCV

import numpy as np

#cross validation/scoring stuff
#from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score

#my stuff
import importlib
import processing



def main():
	target_user_list = input("target user csv: ")
	target_tweet_dir = input("target tweet directory: ")

	#INTERMEDIATE REPRESENTATION & PROCESSING
	#assigns user classifications to user tweets
	data_list = processing.load_data(target_user_list+".csv", target_tweet_dir)

	#determine split amt between train and test
	train_seg = .8 #todo: this can be changed/tuned later(user input?)
	test_seg = 1-float(train_seg) #not currently needed

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
	text_clf = Pipeline([
		('vect', CountVectorizer()),#can add stop_words='english' to params
		('tfidf', TfidfTransformer()),#figure this out better
		('clf', MultinomialNB()),
		])

	#support vect machine pipeline
	text_clf_svm = Pipeline([('vect', CountVectorizer()),
		('tfidf', TfidfTransformer()),
		('clf-svm', SGDClassifier(loss='hinge', penalty='l2',
		alpha=1e-3, max_iter=5, random_state=42)),
	])


	#3
	#use vect/classifier multiplexer system here to find best combo
	#its in old ml learning code somewhere

	#testing
	text_clf.fit(train_data.text, train_data.bot)
	#predict
	predicted = text_clf.predict(test_data.text)
	print("CountVectorizer score:" + str(np.mean(predicted == test_data.bot)))#0.8904761 no matter what


	#fit and predict SVM pipeline
	# text_clf_svm.fit(train_data.text, train_data.bot)
	# predicted2 = text_clf_svm.predict(test_data.text)
	# print("SVM score: "+str(np.mean(predicted2 == test_data.bot)))#same score here



	#new grid search
	processing.perform_gs(train_data, text_clf)





	









	
























main()


