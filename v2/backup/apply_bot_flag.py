#3
#(applies classifications)
#import botometer
#import tweepy
import csv

def main():
	file_str = input("enter file to apply flags to (_r incl.): ")
	thresh = float(input("enter a confidence threshold for classification: "))


	file_str2 = file_str+".csv"

	with open(file_str2, "r") as file:
		reader = csv.reader(file, delimiter = ',')
		next(reader, None)#skip header

		#writer
		newfile = open(file_str+"_"+str(thresh)+".csv", "w")
		writer = csv.writer(newfile, delimiter = ',')
		writer.writerow(['id', 'screen_name', 'name', 'date_created', 'botornot_rt', 'bot'])

		i = 0
		for row in reader:
			#process here
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




