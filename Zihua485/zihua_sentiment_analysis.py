#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Zihua He (Arizona State University)
# Initial Date: October 26, 2018

#The query I used to combine two tables in Sqlite
# create view nlp_source
# as
# 	select * from cu_gsr_event
# 	left join article_nlp_2 using (event_id);

import sqlite3
import pandas as pd
import numpy as np
# from IPython import display
#
# def location_based():

# def sqlite_to_pandas():
database = "/home/zihua/macury/MercuryChallenge/jsonToSql/mercury.db"
# query = "select * from cu_gsr_event;"
# query = "select titlefiltered from article_nlp_2;"
conn = sqlite3.connect(database)
cur = conn.cursor()

try:
    cur.execute("select contentfiltered, keywords, titlefiltered from article_nlp_2;")
    # fetch the sql query with all search results
    rows = cur.fetchall()
    cur.close()
    conn.close()
except sqlite3.IntegrityError as e:
    print(e)

print(len(rows))
# print(df)

# Let's define a set for our headlines so we don't get duplicates when running multiple times:
headlines = set()

for contentfiltered, keywords, titlefiltered in rows:
    headlines.add(titlefiltered)

print(len(headlines))
# print(headlines)

import nltk
# Please Download Packages Below If You Haven't Done This
# nltk.download('vader_lexicon')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('treebank')
# nltk.download('stopwords')
import twython
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA()
results = []

for line in headlines:
    # print(line)
    if not isinstance(line, str):
        line = str(line.encode('utf-8'))
    pol_score = sia.polarity_scores(line)
    pol_score['headline'] = line
    results.append(pol_score)

nltk.pprint(results[:10], width=100)


df = pd.DataFrame.from_records(results)
# df.head()

df['label'] = 0
df.loc[df['compound'] > 0.2, 'label'] = 1
df.loc[df['compound'] < -0.2, 'label'] = -1
df.head()

# def main():
    # my code here
    # location_based()

# if __name__ == "__main__":
#     main()