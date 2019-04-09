import time
import threading
import os.path
import pandas as pd

#my stuff
import emailing
import scraping
import loading

#Austin P
#main thread for server
#listens and creates jobs

#pathways
my_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(my_path, os.pardir))

#if __name__ == '__main__':
#	main()

#check inbox for new received emails,
#should only parse and mark ONE email as read per run
def poll_inbox():
	#check inbox for new emails
	#need to mark as seen
	#https://stackoverflow.com/questions/15317229/python-imap-cannot-mark-email-as-seen

	#placeholder for parsed data
	username = "@realDonaldTrump"
	clf = "r"
	follower_amt = 50
	tweet_amt = 10

	#upon new email, parse out username, flags, details, etc.
	res = {'username':username , 'clf':clf, 'follower_amt':follower_amt, "tweet_amt":tweet_amt}
	
	#return res if new email, otherwise None
	return res


#create new email with results, send back to recv addr.
def send_results(rec_email):
	#
	port = 465
	smtp_server = "smtp.gmail.com"
	sender_email = "austinstwitterbot@gmail.com" 
	password = "IMPORT ENV PASS HERE"

	#figure out 'fancy' emails for any charts generated
	#will probably turn into a multi-part msg generation
	msg = """
	ADD EMAIL HERE
	"""

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, rec_email, msg)
		server.quit()





#take in username, flags from new email,
#run clf stuff and build results
def job(username, clf_name, f_amt, t_amt):
	#get input parsed out
	#this is coming in already, no more stuff needed

	#load clf
	clf = loading.load_clf(clf_name)

	#scrape all needed data, keep records
	scraping.get_tweets(username, f_amt, t_amt)

	#scraping and loading with intermed. file collections to maintain data,
	#preserve tweets scraped.  Slightly more expensive than continuous
	#data kept in memory, but worth it.

	#load up follower list
	followers = loading.load_followers(username)

	#load tweets and build results
	#load primary username tweets
	user_tweets = loading.load_tweets(username)

	#build results for primary username tweets
	for tweet in user_tweets:
		#currently all clf use vectorizers
		#needs iterable for pkl clf
		tweet = [tweet]
		
		predict = clf.predict(tweet)
		print(predict)


	#load follower tweets and build results
	for follower in followers:
		i = 0


	#build email deliverable
		# - csvs with classifications
		# - follower pie chart
		# - basic numbers (amt bot, amt not, etc)


	#call send results here



#def main():
if __name__ == '__main__':

	#scraping.get_tweets("realDonaldTrump", 10, 10)

	#f = loading.load_followers("realDonaldTrump")
	#print(f)

	job("realDonaldTrump", "basic", 5, 10)

	"""
	#run loop 
	run = True
	while(run):
		#poll inbox
		new_job = poll_inbox()
		
		#start new job if new email found
		if new_job != None:
			#create new thread
			t = threading.Thread(target = job, args = (new_job['username']), new_job['clf'])#args())#fill out args
			t.start()

			



		#spawn job based on new emails
		#check stack for new info 
		#use scheduler for jobs


		#might wanna sleep to give time for parse
		time.sleep(1)
	"""







