#1
#This will be a script used to gather info from twitter and store into
#some form of database for later use with ml algorthims.
#going to use TwitterScraper library and tweepy(official Twitter API)

import tweepy
import time
import datetime
import csv
import os.path

#tweepy
#actual twitter API, quick n dirty
consumer_key = "dOrFA8vRadyMiSReJ8VOAb72J"
consumer_secret = "2fMnXFHw4VojuPHCGfFvByjhgouAjs49NzhYVsEH5toGwiPJsV"
access_key = "1072672322929098752-COq6NU34O2xVPJI48s079Czzng776J"
access_secret = "4ChGm1XDU0OVe4TxrFJGxBCEZifKEVRki0SuY5Zxc1YQc"



def main():
    #user input
    amt_str = input("enter amt: ")
    amt = int(amt_str)
    file_str = input("enter csv file: ")
    file_str = file_str+".csv"


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)

    #count param will allow 3000 users per 15 mins (instead of default 20)
    users = tweepy.Cursor(api.followers, screen_name = "realDonaldTrump", count = 200).items()

    #
    open_type = ""
    if os.path.exists(file_str):
        print("specified file exists.")
        open_type = "a"

    else:
        print("new csv file.")
        open_type = "w"

    file = open(file_str, open_type)
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
        date_created = datetime.datetime.now()
        writer.writerow([str(user.id), user.screen_name, user.name, str(date_created)])
        
        i+=1
        print("")




main()


















