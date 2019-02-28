#beginnings of some ml
#using new load_compiled_data()

import csv
import os.path
import string

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

#why did this break?
#from sklearn.model_selection import train_test_split 

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
from sklearn.utils import shuffle

import numpy as np

#cross validation/scoring stuff
#from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score

#my stuff
import importlib

#adding libraries
my_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(my_path, os.pardir))

import sys
sys.path.insert(0, parent_path+"/processing")
import processing

#w2v gensim
from gensim.models import Word2Vec





def main():
	#target_user_list = input("target user csv: ")
	target_tweet_coll = input("target tweet collection: ")

	#INTERMEDIATE REPRESENTATION & PROCESSING
	#assigns user classifications to user tweets
	data_list = processing.load_compiled_data(target_tweet_coll+".csv")

	#data_list_size = len(data_list)

	#todo: implement loading/processing df for _sqz here

	#implement later
	#data_list = processing.preprocess_data(data_list)

	#old todo: implement test_train_split?

	#determine split amt between train and test
	#todo: reimplement these with _sqz
	#1,0,t1,t2,m
	col_names = ['bot', 'text']

	#separate dfs for each classification
	bot_df = pd.DataFrame(columns = col_names)
	not_df = pd.DataFrame(columns = col_names)
	t1_df = pd.DataFrame(columns = col_names)
	t2_df = pd.DataFrame(columns = col_names)
	m_df = pd.DataFrame(columns = col_names)

	bot_count = not_count = t1_count = t2_count = m_count = 0

	#iterate thru loaded data list, split into classes
	for i, row in data_list.iterrows():
		classif = row[0]
		text = row[1]

		if classif == "1":
			#print("classification: "+str(classif)+" adding to bot_df")
			bot_count+= 1
			bot_df.loc[len(bot_df)] = [classif, text]
		elif classif == "0":
			#print("classification: "+str(classif)+" adding to not_df")
			not_count+= 1
			not_df.loc[len(not_df)] = [classif, text]
		elif classif == "t1":
			#print("classification: "+str(classif)+" adding to t1_df")
			t1_count+= 1
			t1_df.loc[len(t1_df)] = [classif, text]
		elif classif == "t2":
			#print("classification: "+str(classif)+" adding to t2_df")
			t2_count+= 1
			t2_df.loc[len(t2_df)] = [classif, text]
		elif classif == "m":
			#print("classification: "+str(classif)+" adding to m_df")
			m_count+= 1
			m_df.loc[len(m_df)] = [classif, text]
		else:
			print("unspecified classification")

	print("bot count: "+str(bot_count))
	print("not count: "+str(not_count))
	print("t1 count:  "+str(t1_count))
	print("t2 count:  "+str(t2_count))
	print("m count:   "+str(m_count))
	print("")

	#todo: work on updated train/test dfs

	#holds the 1,0 high confidence ratings
	train_df = pd.DataFrame(columns = col_names)
	train_df = bot_df.add(not_df)

	#holds the t1, t2 margin cases
	test_df = pd.DataFrame(columns = col_names)
	train_df = t1_df.add(t2_df)	

	#ML
	#training
	#first V2 choice
	text_clf = Pipeline([
		('vect', CountVectorizer()),#can add stop_words='english' to params
		('tfidf', TfidfTransformer()),#figure this out better
		('clf', MultinomialNB()),
	])

	# text_clf = Pipeline([
	# 	('word2vec', Word2Vec()),#can add stop_words='english' to params
	# 	('tfidf', TfidfTransformer()),#figure this out better
	# 	('clf', MultinomialNB()),
	# ])


	#fit to bot and not classifications (>= .80, <= .20)
	#todo: make sure these are input the correct way
	text_clf.fit(train_df.text, train_df.bot)

	#predict
	predicted = text_clf.predict(test_df.text)

	print("CountVectorizer score:" + str(np.mean(predicted == test_df.bot)))#0.8904761 no matter what



main()



