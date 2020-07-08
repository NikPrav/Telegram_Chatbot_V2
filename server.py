from bot import tel_chatbot 
from ics2python import within_limits
import datetime
import pytz
from dateutil.relativedelta import relativedelta
utc=pytz.UTC

# # from fb2cal.src._version import __version_info__, __version__
# from src.__init__ import *
# import src.fb2cal

update_id = None
#path to bot config that stores bot api
config = "config.cfg" 

#Path to the fb2cal config file that stores user id and password
config_user = "config/config.ini"
#NOTE:Needs to merge these 2 into one dem config file
bot = tel_chatbot(config)
flag = 0



#NOTE:Think up of a solid state machine to handle the whole shit, cos you definitely need one for that

#Function that handles the reply statement
def make_reply(msg):
	global update_id
	global config
	global bot

	reply = None
	print(msg)
	#Welcome message
	if msg == '/start':
		reply = 'Hellew. Try giving a duration: If you want to change your username/password,try /uname'
		flag = 0

	#Adding the fb uname and password
	elif msg == '/uname':
		try:
			frm = item["message"]["from"]["id"]
		except:
		    frm = item["edited_message"]["from"]["id"]
		
		bot.send_message("Enter your fb username:",from_)
		print ("Waiting for username...")
		#Reading the reply
		#NOTE: Not the most elegant way, or the most optimised, need to write a proper function to handle this
		#May crash if the user takes too long to reply
		
		updates = bot.get_updates(offset = update_id)
		updates = updates["result"]

		if updates:
			update_id = updates[0]["update_id"]

		print(update_id)
		try:
			message = updates[0]["message"]["text"]
		except:
			message = None

		uname = message
		# print("uname = ",uname)
		
		bot.send_message("Enter your fb password(Lol, it will be unencrypted, but what the hell....:] ) :",from_)
		print ("Waiting for password...")
		updates = bot.get_updates(offset = update_id)
		updates = updates["result"]
		if updates:
			update_id = updates[0]["update_id"]
		try:
			message = updates[0]["message"]["text"]
		except:
			message = None

		passwd = message
		
		#After the uname and passwd is extracted, it is then written to the fb2cal config file, with a uid tag
		# print("passwd = ",passwd)
		print(frm)
		bot.write_uname_to_cfg(config_user,frm,uname,passwd)
		reply = "Success!!"

	#Printing the birthdays using a duration
	else:
		try:
			buffer = msg.split(' ')
			print(type(buffer[1]))
			print(type('month'))
			print(buffer[1])
			#Splits the message into 2 parts, assuming that it is in the format "<num> <unit>"
			# if buffer[0] > '0' and buffer[0] < '9':
			try:
				no = int(buffer[0])				
				if buffer[1] == 'month' or buffer[1] == 'months' :
					# no = int(buffer[0])
					print("Inside month, ",no)
					k = datetime.datetime.now() + relativedelta(months = no)
					print("yo")
					k = utc.localize(k) 
					reply = within_limits(k)
					print("Trying for reply, ",reply)

				elif buffer[1] == 'day' or buffer[1] == 'days':
					# no = int(buffer[0])
					print("Inside day, ",no)				
					k = datetime.datetime.now() + relativedelta(days = no)
					k = utc.localize(k) 
					print(k)
					reply = within_limits(k) 

				elif buffer[1] == 'week' or buffer[1] == 'weeks':
					# no = int(buffer[0])
					print("Inside week, ",no)
					k = datetime.datetime.now() + relativedelta(weeks = no)
					k = utc.localize(k) 
					reply = within_limits(k)
				else:
					reply = "Try Again"
			except:
				reply = "Try Again"

		except:
			reply = "Try Again"  

	print("reply is ", reply)
	return reply

#The infinite loop that checks for replies
while True:
	print ("...")
	updates = bot.get_updates(offset = update_id)
	updates = updates["result"]
	print(update_id)
	#If a new update is found
	if updates:
		for item in updates:
			update_id = item["update_id"]
			try:
				message = item["message"]["text"]
			except:
				message = None

			try:
				from_ = item["message"]["from"]["id"]
			except:
			    from_ = item["edited_message"]["from"]["id"]
			print(message)
			reply = make_reply(message)
			bot.send_message(reply,from_)