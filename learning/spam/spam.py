#Austin P
#https://www.kdnuggets.com/2017/03/email-spam-filtering-an-implementation-with-python-and-scikit-learn.html

#using a subset of spam and non-spam from Ling-spam corpus
#702 training, 260 testing

#preprocessed text:
#stop words removed
#lemmatized

import os
import numpy as np 
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import SVC, NuSVC, LinearSVC
import copy


#build dict of all words
def make_dict(train_dir):
	#grab emails in dataset file
	emails = [os.path.join(train_dir,f) for f in os.listdir(train_dir)]
	all_words = []
	
	#spin thru all mail
	for mail in emails:
		with open(mail) as m:
			#spin thru specific mail file
			for i, line in enumerate(m):
				#body of email starts
				if i == 2:
					words = line.split()
					all_words = all_words+words
	dictionary = Counter(all_words)
	
	#non-word removal routine
	list_to_rem = dictionary.keys()
	
	#deepcopy fix
	# ===
	#list_to_rem_2 = list_to_rem.copy()

	for item in list_to_rem:							# =======.copy().items()
		if item.isalpha() == False:#change to single if later
			del dictionary[item]
		elif len(item) == 1:
			del dictionary[item]


	#reduce to 3000 most used
	dictionary = dictionary.most_common(3000)

	return dictionary



#feature extraction
def extract_features(mail_dir):
	files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
	features_matrix = np.zeros((len(files),	3000))
	docID = 0;
	for fil in files:
		with open(fil) as fi:
			for i,line in enumerate(fi):
				if i == 2:
					words = line.split()
					for word in words:
						wordID = 0
						for i,d in enumerate(dictionary):
							if d[0] == word:
								wordID = i
								features_matrix[docID, wordID]
		docID = docID + 1
	return features_matrix







def main():
	#print("works\n")
	
	#create dict
	train_dir = 'train-mails'
	dictionary = make_dict(train_dir)

	#feature vectors
	train_labels = np.zeros(702)
	train_labels[351:701] = 1
	train_matrix = extract_features(train_dir)

	#train
	model1 = MultinomialNB()
	model2 = LinearSVC()
	model1.fit(train_matrix, train_labels)
	model2.fit(train_matrix, train_labels)

	#test unseen mails for spam
	test_dir = 'test-mails'
	test_matrix = extract_features(test_dir)
	test_labels = np.zeros(260)
	test_labels[130:260] = 1

	result1 = model1.predict(test_matrix)
	result2 = model2.predict(test_matrix)

	#print confusion_matrix(test_labels, result1)
	#print confusion_matrix(test_labels, result2)




#main()

if __name__ == '__main__':
    main()
























