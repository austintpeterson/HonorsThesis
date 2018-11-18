#Austin Peterson

#have to learn to build dataframes with working columns, and append data dynamically

import pandas as pd
from sklearn.naive_bayes import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import *
from sklearn.svm import *

#bot holds yes/no (bool?)
#text of tweet assoc.
col_names = ['bot', 'text']
my_df = pd.DataFrame(columns = col_names)

#add record to dataframe (dynamically one at a time!)
my_df.loc[len(my_df)] = ['yes', 'Trump2020 blyat!']
my_df.loc[len(my_df)] = ['no', 'Eating my sandwich']
my_df.loc[len(my_df)] = ['yes', 'MAGA guns']
my_df.loc[len(my_df)] = ['no', 'Going to concert']
my_df.loc[len(my_df)] = ['yes', 'Russia is good']
my_df.loc[len(my_df)] = ['no', 'Time to go to bed']
my_df.loc[len(my_df)] = ['yes', 'I will eat Nancy Pelosi alive']
my_df.loc[len(my_df)] = ['no', 'Eating my sandwich']

#print(my_df)

#test passing to vect/classifiers
train_data = my_df[:8]

classifier = OneVsRestClassifier(SVC(kernel='linear'))#want multinom or nominal
vectorizer = TfidfVectorizer()#want Count

#training
vectorize_text = vectorizer.fit_transform(train_data.text)
classifier.fit(vectorize_text, train_data.bot)


#user input loop
while True:
	n = input("enter text: ")
	if n == "Q":
		break
	
	else:
		vectorize_text = vectorizer.transform([n])
		predict = classifier.predict(vectorize_text)[0]

		print("Is it a bot: "+predict)























































