#Austin Peterson

#attempting to learn email, send emails back
#https://www.pybloggers.com/2018/12/sending-emails-with-python/

import smtplib, ssl
import yagmail

#3 things to login to gmail w/ python
#mail server, username, password

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "austinstwitterbot@gmail.com"  # Enter your address
receiver_email = "austintpeterson@gmail.com"  # Enter receiver address
password = input("Type your password and press enter: ")
message = """
Subject: Hi there

This message is sent from my python twitter bot."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, message)


#yagmail test
#works specifically with gmail
# yag = yagmail.SMTP(sender_email)
# yag.send(
# 	to=receiver_email,
# 	subject="Yagmail test with attachment",
# 	contents=[message],#can add files to attach
# )





