#1
#This will be a script used to gather followers from twitter (currently set to @realDonaldTrump)
#using the TwitterAPI

import tweepy
import time
import datetime
import csv
from sys import argv

#getting api keys
import os
import os.path
from os.path import join, dirname
from dotenv import load_dotenv
import log

#load env variables
dotenv_path = join(dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)
 
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')



def main():
    #changed to sys for nohup
    amt_str = argv[1]#get amt of followers to collect
    amt = int(amt_str)
    file_str = argv[2]#get file name to write/append to
    file_str = file_str+".csv"



    #tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #count param will allow 3000 users per 15 mins (instead of default 20)
    users = tweepy.Cursor(api.followers, screen_name = "realDonaldTrump", count = 200).items()



    #pathways
    my_path = os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.abspath(os.path.join(my_path, os.pardir))

    #file opening
    open_type = ""
    #not really used
    if os.path.exists(parent_path+"/user_collections/"+file_str):
        print("specified file exists.")
        open_type = "a"

    else:
        print("new csv file.")
        open_type = "w"

    file = open(parent_path+"/user_collections/"+file_str, open_type)
    writer = csv.writer(file, delimiter = ',')

    if open_type == "w":
        writer.writerow(['id', 'screen_name', 'name', 'date_created', 'botornot_rt', 'bot'])



    #will spin every 300 names for 15 mins?
    i = 0
    while i < amt:
        try:
          user = next(users)
        
        except StopIteration:
            print("stop iteration error.")
            break;

        except tweepy.error.RateLimitError:#used to be tweepy.TweepError
            print("tweepy error/limit. sleeping.")
            time.sleep(60*15)
            print("resumed.")
            user = next(users)
           
        #process user here
        print(str(i)+": "+user.screen_name)
        log.write(file_str+": "+str(i)+": "+user.screen_name)
        
        date_created = datetime.datetime.now()
        writer.writerow([str(user.id), user.screen_name, user.name, str(date_created)])
        
        i+=1
        print("")




main()


















