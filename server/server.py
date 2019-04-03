import time
import threading

#Austin P
#main thread for server
#listens and creates jobs

if __name__ == '__main__':
	main()

#check inbox for new received emails,
#should only parse and mark ONE email as read per run
def poll_inbox():
	#check inbox for new emails
	#need to mark as seen
	#https://stackoverflow.com/questions/15317229/python-imap-cannot-mark-email-as-seen

	#upon new email, parse out username, flags, details, etc.
	res = ["tag", "flag", "etc"]
	
	#return res if new email, otherwise None
	return res


#create new email with results, send back to recv addr.
def send_results():
	#



#take in username, flags from new email,
#run clf stuff and build results
def job():

	#call send results here



def main():
	#initiate classifier(s)


	#initiate stack
	#(whatever is holding the jobs)
	#no longer needed


	#run loop 
	run = True
	while(run):
		#poll inbox
		new_job = poll_inbox()
		
		#start new job if new email found
		if new_job != None:
			#create new thread
			t = threading.Thread(target = job, args())#fill out args
			t.start()

			



		#spawn job based on new emails
		#check stack for new info 
		#use scheduler for jobs


		#might wanna sleep to give time for parse
		time.sleep(1)







