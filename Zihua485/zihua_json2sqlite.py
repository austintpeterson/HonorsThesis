import json
import sqlite3
from sqlite3 import Error

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

def main():
        database = "/home/zihua/macury/MercuryChallenge/scraper/articles.db"
        # replace this database if you are not the supreme leader, so called dictator

        path = "/home/zihua/macury/twitter/twitterscraper/output.json"
        # change this path if you are not, again, the supreme leader

        counter = 0
        #read each json file included in cu_gsr
        # for filename in os.listdir(path):
        temppath = path

        with open(temppath, "r") as read_file:
            data = json.load(read_file)

        print("===========================Now reading " + path + "===========================")

        sql_create_cu_gsr_event_table = """CREATE TABLE IF NOT EXISTS twitts_info (
                                                full_name text,
                                                html text,
                                                id text,
                                                likes text,
                                                replies text,
                                                retweets text,
                                                text text,
                                                times_tamp text,
                                                url text,
                                                user_name text
                                        );"""

        #create a databse connection
        conn = create_connection(database)
        if conn is not  None:
            #create projects table
            execute_sql_comm(conn, sql_create_cu_gsr_event_table)
        else:
            print("cannot create databse connection.")

        c = conn.cursor()

        #parse json data into vars
        for entry in data:
            try:
                query = '(full_name, html, id, likes, replies, retweets, text, times_tamp, url, user_name)'

                c.execute('INSERT INTO twitts_info ' + query + ' VALUES (?,?,?,?,?,?,?,?,?,?)', (entry['fullname'], entry['html'], entry['id'], entry['likes'], entry['replies'], entry['retweets'], entry['text'], entry['timestamp'], entry['url'], entry['user']))

                print("User: " + entry['user'] + " Inserted Into " + database)
            except Error as e:
                print(entry['user'] + " not successful. Error: " + e)

        conn.commit()
        counter = counter + 1

        print(str(counter) + " json files read from " + path)

if __name__ == "__main__":
    main()

print("Test Passed")


