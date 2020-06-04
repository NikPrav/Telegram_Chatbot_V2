from bot import tel_chatbot 
from ics2python import within_limits
import datetime
import pytz
from dateutil.relativedelta import relativedelta
utc=pytz.UTC

update_id = None
bot = tel_chatbot("config.cfg")
flag = 0

def make_reply(msg):
	reply = None
	if msg is '\\start':
		reply = 'Hellew. Try giving a duration:'
		flag = 1;
	else:
		try:
			buffer = msg.split(' ')
			print(type(buffer[1]))
			print(type('month'))
			print(buffer[1])
			if buffer[1] == 'month':
				no = int(buffer[0])
				print("Inside month, ",no)
				k = datetime.datetime.now() + relativedelta(months = no)
				print("yo")
				k = utc.localize(k) 
				reply = within_limits(k)
				print("Trying for reply, ",reply)

			if buffer[1] == 'day':
				no = int(buffer[0])
				print("Inside day, ",no)				
				k = datetime.datetime.now() + relativedelta(day = no)
				k = utc.localize(k) 
				reply = within_limits(k) 

			if buffer[1] == 'week':
				no = int(buffer[0])
				print("Inside day, ",no)
				k = datetime.datetime.now() + relativedelta(week = no)
				k = utc.localize(k) 
				reply = within_limits(k)

		except:
			reply = "Try Again"  

	print("reply is ", reply)
	return reply


while True:
	print ("...")
	updates = bot.get_updates(offset = update_id)
	updates = updates["result"]


	if updates:
		for item in updates:
			update_id = item["update_id"]
			try:
				message = item["message"]["text"]
			except:
				message = None
			from_ = item["message"]["from"]["id"]
			print(message)
			reply = make_reply(message)
			bot.send_message(reply,from_)