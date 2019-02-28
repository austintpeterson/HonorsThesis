#3
#(applies classifications)
#this script applies classifications based on top/bottom 20% (1 or 0)
#and the 20-30% as t1, and 70-80% as t2
#written to determine mis-classifications in the upper/lower margins

import csv

import os
import os.path
from os.path import join, dirname
from dotenv import load_dotenv

from sys import argv

def main():
	file_str = input("enter file to apply flags to (_r incl.): ")
	file_str_ext = file_str+".csv"
	#thresh = float(arg[2])#get c
	#float(input("enter a confidence threshold for classification: "))

	#pathways
	my_path = os.path.dirname(os.path.abspath(__file__))
	parent_path = os.path.abspath(os.path.join(my_path, os.pardir))



	with open(parent_path+"/user_collections/"+file_str_ext, "r") as file:
		reader = csv.reader(file, delimiter = ',')
		next(reader, None)#skip header

		#writer
		#newfile = open(parent_path+"/user_collections/"+file_str+"_"+str(thresh)+".csv", "w")
		newfile = open(parent_path+"/user_collections/"+file_str+"_sqz"+".csv", "w")

		writer = csv.writer(newfile, delimiter = ',')
		writer.writerow(['id', 'screen_name', 'name', 'date_created', 'botornot_rt', 'bot'])

		i = 0
		for row in reader:

			#determine flag based on thresh
			print(str(i)+": classifying @"+row[1]+"...")
			bot_rt = float(row[4])

			if bot_rt >= .80:
				#upper training (bots)
				writer.writerow([str(row[0]), row[1], row[2], row[3], row[4], "1"])
			elif bot_rt <= .20:
				#lower training (nots)
				writer.writerow([str(row[0]), row[1], row[2], row[3], row[4], "0"])
			elif .20 < bot_rt <= .30:
				#lower test
				writer.writerow([str(row[0]), row[1], row[2], row[3], row[4], "t1"])
			elif .70 <= bot_rt < .80:
				#upper test
				writer.writerow([str(row[0]), row[1], row[2], row[3], row[4], "t2"])
			else:
				#middle section
				writer.writerow([str(row[0]), row[1], row[2], row[3], row[4], "m"])


			i += 1





main()




 