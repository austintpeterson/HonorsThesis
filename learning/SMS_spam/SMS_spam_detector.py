#Austin Peterson
#sms spam detector

#data: http://www.dt.fee.unicamp.br/~tiago/smsspamcollection/ (UK)

import random
import time
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier #text.classifiers UNUSED
from sklearn.naive_bayes import MultinomialNB

#NB takes tuples as (body(text), class(ham/spam))


#get data
#creates tuple of words and their class
def get_list_tuples(read_file):
	list_tuples = []
	with open(read_file,"r") as r:
		c = 0
		#each line in data is sep msg
		for line in r:
			tabsep = line.strip().split('\t')
			msg = TextBlob(tabsep[1])#get sentence

			#print(msg)

			try:
				words = msg.words
			except:
				continue

			for word in words:
				#not stopword and not number
				if word not in stopwords.words() and not word.isdigit():
					list_tuples.append((word.lower(), tabsep[0]))

			#limiting factor
			c+= 1
			if c == 500:
				break;

	return list_tuples














def main():
	t = time.time()
	entire_data = get_list_tuples('SMSSpamCollection.txt')
	print("took "+str(time.time()-t)+" seconds to import data.")

	#shuffle word data so that test and train are cut equally
	random.seed(1)
	random.shuffle(entire_data)
	#50/50 split
	train = entire_data[:250]
	test = entire_data[251:500]

	t = time.time()



	#text classifier here
	#starting w MultinomialNB

	cl = MultinomialNB()

	


	
	#print("classifier trained.")
	#accuracy = cl.accuracy(test)
	#print("accuracy: "+str(accuracy))

	


main()






























