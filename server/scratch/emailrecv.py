#Austin Peterson

#https://codehandbook.org/how-to-read-email-from-gmail-using-python/
#use imap@gmail.com to read incoming mail

import smtplib
import time
import imaplib
import email

import sys
#import getpass
import datetime
import base64
import email
#import BeautifulSoup

#pwd a** ONE TW

port = 993#465 in send
smtp_server = "imap.gmail.com"#use instead of smtp to recv
sender_email = "austinstwitterbot@gmail.com"
password = input("Type your password and press enter: ")

def readmail():
	mail.select('inbox')#
	type, data = mail.search(None, 'ALL')
	mail_ids = data[0]
	id_list = mail_ids.split()

	#get latest email in inbox
	latest_email_id = int(id_list[-1])

	#get email w particular ID:
	typ, data = mail.fetch(latest_email_id, '(RFC822)')



def readmail_2():
	imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
	imap.login(sender_email, password)#sender = mine
	imap.select('INBOX')

	# Use search(), not status()
	status, response = imap.search(None, 'INBOX', '(UNSEEN)')
	unread_msg_nums = response[0].split()

	# Print the count of all unread messages
	print(len(unread_msg_nums))

	# Print all unread messages from a certain sender of interest
	status, response = imap.search(None, '(UNSEEN)', '(FROM "%s")' % (sender_of_interest))
	unread_msg_nums = response[0].split()
	da = []
	for e_id in unread_msg_nums:
		_, response = imap.fetch(e_id, '(UID BODY[TEXT])')
		da.append(response[0][1])
	print(da)

	# Mark them as seen
	for e_id in unread_msg_nums:
		imap.store(e_id, '+FLAGS', '\Seen')



def readmail_3():
	M = imaplib.IMAP4_SSL(smtp_server, 993)
	M.login(sender_email, password)
	M.select()

	typ, message_numbers = M.search(None, 'ALL')  # change variable name, and use new name in for loop

	for num in message_numbers[0].split():
		typ, data = M.fetch(num, '(RFC822)')
		# num1 = base64.b64decode(num)          # unnecessary, I think
		#print(data)   # check what you've actually got. That will help with the next line
		
		#data1 = base64.b64decode(data[0][1])
		#print('Message %s\n%s\n' % (num, data1))

		raw_email = data[0][1]

		# email_message = email.message_from_string(raw_email)

		# print(email_message['To'])
		# print(email.utils.parseaddr(email_message['From']))
		# print(email.message.items())

		# email_message = email.message_from_bytes(raw_email)
		# maintype = email_message.get_content_maintype()

		# #or multipart
		# if maintype == 'text':
		# 	html = str(email_message.get_payload())

		# if html is not None:
		# 	soup = BeautifulSoup4(html, 'html.parser')
		# 	print("soup:\n")
		# 	print(soup)

		print(raw_email)

		print("\n\n\n")

		#


	M.close()
	M.logout()

# def read_all_mail():
# 	try:
# 		mail = imaplib.IMAP4_SSL(smtp_server)
# 		mail.login(sender_email, password)
# 		mail.select('inbox')

# 		type, data = mail.search(None, 'ALL')
# 		mail_ids = data[0]

# 		id_list = mail_ids.split()   
# 		first_email_id = int(id_list[0])
# 		latest_email_id = int(id_list[-1])


# 		for i in range(latest_email_id,first_email_id, -1):
# 			typ, data = mail.fetch(i, '(RFC822)' )

# 			for response_part in data:
# 				if isinstance(response_part, tuple):
# 					msg = email.message_from_string(response_part[1])
# 					email_subject = msg['subject']
# 					email_from = msg['from']
# 					print('From : ' + email_from + '\n')
# 					print('Subject : ' + email_subject + '\n')

# 	except Exception:
# 		#print(str(e))


#new try
#http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/

#process the inbox
def process_inbox(M):
	rv, data = M.search(None, "ALL")
	if rv != 'OK':
		print("No emails found in inbox")
		return

	#iter thru all data
	for num in data[0].split():
		rv, data = M.fetch(num, '(RFC822)')
		if rv != 'OK':
			print("Error getting message: "+str(num))
			return

		print(email.message_from_string(str(data[0][1])))
		# msg = email.message_from_string(data[0][1])
		# print("Message: "+str(num)+": "+str(msg['Subject']))
		# print()


readmail_3()

# #login w/ imap module
# mail = imaplib.IMAP4_SSL(smtp_server)
# mail.login(sender_email, password)

# #outlying inbox opening
# rv, data = mail.select("inbox")
# if rv == 'OK':
# 	print("processing inbox")
# 	process_inbox(mail)
# 	mail.close()
# mail.logout()




#poll the inbox every so often, and spawn a new process when 
#a new (viable) email comes in that requires processing/ml 


























