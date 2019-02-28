#3
#(applies classifications)
#no nohup, happens quick enough

import csv

import os
import os.path
from os.path import join, dirname
from dotenv import load_dotenv

def main():
	file_str = input("enter file to apply flags to (_r incl.): ")
	file_str_ext = file_str+".csv"
	thresh = float(input("enter a confidence threshold for classification: "))



	#pathways
	my_path = os.path.dirname(os.path.abspath(__file__))
	parent_path = os.path.abspath(os.path.join(my_path, os.pardir))



	with open(parent_path+"/user_collections/"+file_str_ext, "r") as file:
		reader = csv.reader(file, delimiter = ',')
		next(reader, None)#skip header

		#writer
		newfile = open(parent_path+"/user_collections/"+file_str+"_"+str(thresh)+".csv", "w")
		writer = csv.writer(newfile, delimiter = ',')
		writer.writerow(['id', 'screen_name', 'name', 'date_created', 'botornot_rt', 'bot'])

		i = 0
		for row in reader:

			#determine flag based on thresh
			print(str(i)+": classifying @"+row[1]+"...")
			bot_rt = float(row[4])

			#botornot_rt exceeds user def. threshold,
			#classified as a bot (1)
			if bot_rt >= thresh:
				writer.writerow([str(row[0]), row[1], row[2], row[3], row[4], "1"])
			else:
				writer.writerow([str(row[0]), row[1], row[2], row[3], row[4], "0"])
			i += 1





main()




