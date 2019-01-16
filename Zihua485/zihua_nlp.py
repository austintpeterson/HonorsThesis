#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from newspaper import Article
import cfscrape
import sqlite3
from sqlite3 import Error
import time

# download nltk
import nltk
# nltk.download()

from nltk.corpus import treebank
import nltk
# Please Download Packages Below If You Haven't Done This
    # nltk.download('averaged_perceptron_tagger')
    # nltk.download('maxent_ne_chunker')
    # nltk.download('words')
    # nltk.download('treebank')
    # nltk.download('stopwords')

from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
ps = PorterStemmer

from nltk.stem.isri import ISRIStemmer
isrist = ISRIStemmer()

# stop words in arabic
stopWord = set(stopwords.words('arabic'))
# print(len(stopWord))

def select_articles():
    # database = "/home/zihua/macury/MercuryChallenge/scraper/articles.db"
    database = "/home/zihua/macury/MercuryChallenge/jsonToSql/mercury.db"
    #connect to the database
    con = sqlite3.connect(database)
    # counter = 0
    cur = con.cursor()

    try:
        #select event id and url from the sqlite table
        # cur.execute("select title from article_info where title != '404 Not Found';")
        cur.execute("select event_id, content, keywords, title from article_info where title != '404 Not Found';")

        #fetch the sql query with all search results
        rows = cur.fetchall()

        # print(len(rows))
    except sqlite3.IntegrityError as e:
        print(e)
        print("Error 1 Happends Here!")
        # print('ERROR: ID {}'.format(even_id))
    # Committing changes and closing the connection to the database file
    # con.commit()
    con.close()

    for event_id, content, keywords, title in rows:
        # for event_id, title in row:
        print(event_id, " -> ", title)

        # title word tokenize
        title_words = word_tokenize(title)
        # print(title_words)

        titleWordsFiltered = []

        #ignore stop word in title
        for title_word in title_words:
            if title_word not in stopWord:
                titleWordsFiltered.append(title_word)
        # print(titleWordsFiltered)

        # title stem words, I think it is not necessary
        # titleWordsStemmed = []
        # for titleWord in titleWordsFiltered:
        #     if titleWord is not None:
        #         titleStemWord = isrist.stem(titleWord)
        #         titleWordsStemmed.append(titleStemWord)
        #     else:
        #         print("No Word in titleWordsStemmed Array")
        #         continue
        # print(titleWordsStemmed)

        # for token in tit_tokens:
        #     # print(token)
        #     stem_token = st.stem(token)
        #     # print(stem_token)

        #content word tokenize
        #tokenize all aranic words
        # cont_tokens = nltk.word_tokenize(content)
        # print(cont_tokens)

        # for cont_token in cont_tokens:
        #     # print(cont_tokens)
        #     stem_token = st.stem(cont_token)
        #     # print(stem_token)

        # stop words in arabic
        data = content
        words = word_tokenize(data)
        wordsFiltered = []
        # print(words)
        # print(len(stopWord))
        for w in words:
            if w not in stopWord:
                wordsFiltered.append(w)
        # print(wordsFiltered)

        # # ignore all arabic punctuation
        # content_txt = nltk.regexp_tokenize(content, r'[،؟!.؛]\s*', gaps=True)
        # print(content_txt)

        # stem words in arabic
        wordsStemmed = []
        # stemWordComparison = []
        for word in wordsFiltered:
            # print(word)
            if word is not None:
                stemWord = isrist.stem(word)
                # print(stemWord)
                wordsStemmed.append(stemWord)
                # stemWordComparison.append(word + " -> " + stemWord)
            else:
                print("No Word in wordsFiltered Array")
                continue

        # print(wordsStemmed)

        # stop words in arabic for keywords
        # data = content
        keywordsTokenized = word_tokenize(keywords)
        keywordsFiltered = []
        # print(words)
        # print(len(stopWord))
        for w in keywordsTokenized:
            if w not in stopWord:
                keywordsFiltered.append(w)
        # print(wordsFiltered)

        # # ignore all arabic punctuation
        # content_txt = nltk.regexp_tokenize(content, r'[،؟!.؛]\s*', gaps=True)
        # print(content_txt)

        # stem words in arabic for keywords
        keywordsStemmed = []
        # stemWordComparison = []
        for wordInKeyword in keywordsFiltered:
            # print(word)
            if wordInKeyword is not None:
                keywordStemWord = isrist.stem(wordInKeyword)
                # print(stemWord)
                keywordsStemmed.append(keywordStemWord)
                # stemWordComparison.append(word + " -> " + stemWord)
            else:
                print("No Word in wordsFiltered Array")
                continue

        # Transform list to string
        keywords_keywords = "  /  ".join(str(x) for x in keywordsStemmed)
        content_keywords = "  /  ".join(str(x) for x in wordsStemmed)
        title_keywords  = "  /  ".join(str(x) for x in titleWordsFiltered)


        # for x in wordsStemmed:
        #     print(x)
        # wordsStemmed2 = [x for x in wordsStemmed if x != []]
        # print(wordsStemmed2)
        # print(stemWordComparison)

        # ps == PorterStemmer

        # pos tag on it
        # tagged = nltk.pos_tag(tokens)
        # print(tagged)

        # identify named entities
        # entities = nltk.chunk.ne_chunk(tagged)
        # print(entities)

        # display a parse tree
        # t = treebank.parsed_sents(entities)
        # t.draw()

        # Upload to Database Table Called article_nlp
        try:
            con2 = sqlite3.connect(database)
            # con = sqlite3.connect(database)
            with con2:
                cur2 = con2.cursor()
                # insert all attributes to the sqlite table
                cur2.execute(
                    'INSERT INTO article_nlp (Event_ID, ContentFiltered, Keywords, TitleFiltered) VALUES (?,?,?,?)',
                    (event_id, content_keywords, keywords_keywords, title_keywords))
                # call commit on the connection...
                con2.commit()

        except Error as e:
            print(event_id + " not successful. Error: " + database)
            pass

def execute_sql_comm(conn, sql_comm):
    try:
        c = conn.cursor()
        # execute the sql command
        c.execute(sql_comm)
    except Error as e:
        print(e)

def create_connection(db_file):
    try:
        # connect sqlite3 database
        conn = sqlite3.connect(db_file)
        return  conn
    except Error as e:
        print(e)

    return None

def sql_create_table():
    # This is the path of the database I named. Please feel free to change it your path
    # database = "/home/zihua/macury/MercuryChallenge/scraper/articles.db"

    # This is the path to mercury.db in my path. Please change it to your path if possible
    database = "/home/zihua/macury/MercuryChallenge/jsonToSql/mercury.db"
    # Create the table with 7 attributes, such as event id, authors name, publish data,
    # article content, article keywords, article summary, and article titles, respectively.

    # Detele the existing table and add more properties in the sql query below in case you want to add additional attribute this table
    sql_create_article_content_table = """CREATE TABLE IF NOT EXISTS article_nlp (
                                        Event_ID text,
                                        ContentFiltered text,
                                        Keywords text,
                                        TitleFiltered text
                                );"""

    #create a database connection
    conn = create_connection(database)
    if conn is not None:
        #create project table
        execute_sql_comm(conn, sql_create_article_content_table)
    else:
        print("Cannot create database connection.")

def main():
    # nltk process to articles
    select_articles()

    # Uncomment this if you want to create this table
    # create a new table to store results
    # sql_create_table()

if __name__ == '__main__':
    main()
