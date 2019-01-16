#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from newspaper import Article
import cfscrape
import sqlite3
from sqlite3 import Error
import time

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


def sql_create_second_table():
    # This is the path of the database I named. Please feel free to change it your path
    # database = "/home/zihua/macury/MercuryChallenge/scraper/articles.db"

    # This is the path to mercury.db in my path. Please change it to your path if possible
    database = "/home/zihua/macury/MercuryChallenge/jsonToSql/mercury.db"
    # Create the table with 7 attributes, such as event id, authors name, publish data,
    # article content, article keywords, article summary, and article titles, respectively.

    # Detele the existing table and add more properties in the sql query below in case you want to add additional attribute this table
    sql_create_article_content_table = """CREATE TABLE IF NOT EXISTS article_info (
                                        Event_ID text,
                                        Authors text,
                                        Publish_Date datetime,
                                        Content text,
                                        Keywords text,
                                        Summary text,
                                        Title text
                                );"""

    #create a database connection
    conn = create_connection(database)
    if conn is not None:
        #create project table
        execute_sql_comm(conn, sql_create_article_content_table)
    else:
        print("Cannot create database connection.")

def select_scraper_zero_tasks():
    # database = "/home/zihua/macury/MercuryChallenge/scraper/articles.db"
    database = "/home/zihua/macury/MercuryChallenge/jsonToSql/mercury.db"
    #connect to the database
    con = sqlite3.connect(database)
    # counter = 0
    cur = con.cursor()

    #select event id and url from the sqlite table
    cur.execute("select event_id, first_reported_link from cu_gsr_event group by first_reported_link having count(event_id)>0 order by count(first_reported_link) desc;")

    #fetch the sql query with all search results
    rows = cur.fetchall()

    print(len(rows))

    # for each event id and url under the search query
    for event_id, url in rows:
        scraper = cfscrape.create_scraper(url)

        # print(event_id,', ', url)
        try:
            # scrape the url content
            gold = scraper.get(url).content
            print("URL scraped")
        except:
            # print the URL that was failed to visit
            print("Failed at ", url)
            continue

        #article function to parse the arabic webpage, especially in Arabic
        article = Article(url, memoize_articles=False, language='ar')

        #download html page by using scraper library
        try:
            article.download(input_html=gold)

            #This is another bug from the source code. Hope this solve the problem.
            #The reason behind this is some website has "deformed" format, and it takes a period of time to visit it.
            if article.download_state != 2:  # ArticleDownloadState.SUCCESS is 2
                time.sleep(1)
                article.parse()
            else:
                #parse the html page
                article.parse()

            #add sleep time here
            # time.sleep(1)

            #apply article nlp function
            article.nlp()

            #event id is given
            eventid = event_id

            #Troublemaker is Here! Article gives this value as a list,
            #but Sqlite Table does not take list as text value
            author = article.authors

            #I use join function to combine the list to be a string
            authors = " ".join(str(x) for x in author)

            #decide not to add current parsing time.
            #the publish date function gets publish date
            #depend upon the capability of this function to get publish date
            publish_date = article.publish_date
            # date = article.publish_date.date()

            #it gets title if possible
            title = article.title

            #it gets article main content
            content = article.text

            #Again, another troublemaker here! It works after combine list to be a string
            keyword = article.keywords
            if keyword is None:
                keywords = keyword
            else:
                keywords = ' '.join(str(e) for e in keyword)

            #Article summary, but assume it's same as text, which should be the main content
            summary = article.summary

            if title:
                print(title)
                # print(keywords)
            elif keywords:
                print("K Perceived")

            elif summary:
                print("S Perceived")

            elif content:
                print("C Perceived")

            else:
                print("Skipped, No Title or Any Other Needed Info")
                continue

            try:
                con2 = sqlite3.connect(database)
                # con = sqlite3.connect(database)
                with con2:
                    cur2 = con2.cursor()
                    #insert all attributes to the sqlite table
                    cur2.execute('INSERT INTO article_info (Event_ID, Authors, Publish_Date, Content, Keywords, Summary, Title) VALUES (?,?,?,?,?,?,?)', (eventid, authors, publish_date, content, keywords, summary, title))
                    # call commit on the connection...
                    con2.commit()

            except Error as e:
                print(event_id + " not successful. Error: " + database)
                pass

        except:
            print("This File May Not Been Downloaded!")
            pass

def main():
    # database = "/home/zihua/macury/MercuryChallenge/scraper/articles.db"
    # database = "/home/zihua/macury/MercuryChallenge/jsonToSql/mercury.db"
    #umcomment this function below in case you want to build this table in your sqlite database
    # sql_create_second_table()

    # Please mark comment on the function above if you have built your table and run function below to start crawling
    select_scraper_zero_tasks()

if __name__ == '__main__':
    main()