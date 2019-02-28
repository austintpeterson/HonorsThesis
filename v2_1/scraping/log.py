import time
import os
from datetime import datetime

#used to write to shared log file about updates on running scraper scripts
#needed because scripts will be run for a long time with nohup, might have interrupts
def write(logstr):
	date = datetime.now()
	
	open_type = ""
	if os.path.exists("log.txt"):
		open_type = "a"

	else:
		open_type = "w"


	with open("log.txt",open_type) as log_file:	
		log_file.write(str(date)+" - "+logstr+"\n")
		log_file.close()

	return
