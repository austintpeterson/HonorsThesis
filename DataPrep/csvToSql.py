#Austin Peterson
#used to convert csv data to standardized sql db

import json
import sqlite3
import time
import os
from pathlib import Path
import csv

#"user_id","user_key","created_at","created_str","retweet_count","retweeted","favorite_count","text","tweet_id","source","hashtags","expanded_urls","posted","mentions","retweeted_status_id","in_reply_to_status_id"
#"2532611755","kathiemrr","1488207240000","2017-02-27 14:54:00","","","","#ThingsDoneByMistake kissing auntie in the lips","836227891897651201","","[""ThingsDoneByMistake""]","[]","POSTED","[]","",""

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def execute_sql_comm(conn, sql_comm):
    try:
        c = conn.cursor()
        c.execute(sql_comm)
    except Error as e:
        print(e)

#gets Data directory path
#project might move, Data directory arch. will not
def get_data_path():
    mypath = Path().absolute()
    datapath = str(mypath)[:-4]+"/"#PosixPath
    return datapath



def main():
    database = "thesis.db"
    datapath = get_data_path()

    with open(datapath+"nbctweets.csv", 'rb') as csvfile:
        #tweet_reader = csv.reader(csvfile, )

main()