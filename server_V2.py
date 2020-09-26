from bot import tel_chatbot 
from ics2python import within_limits
import datetime
import pytz
from dateutil.relativedelta import relativedelta
utc=pytz.UTC
import os
import configparser as cfg
import logging
import humanize
# # from fb2cal.src._version import __version_info__, __version__
# from src.__init__ import *
# import src.fb2cal
print(os.listdir())
update_id = None
#path to bot config that stores bot api
config = "config.cfg" 

# Storing default value for last update
# last_update = None
# naive = datetime.replace(tzinfo=None)

# Log Path
log_path = 'logs/main.log'

#Path to the fb2cal config file that stores user id and password
config_user = "fb2cal/src/config/config.ini"
#NOTE:Needs to merge these 2 into one dem config file
bot = tel_chatbot(config)
flag = 0

# Setting up a logger instance
logging.basicConfig(filename=log_path,format='%(asctime)s %(message)s',filemode='w')
logger = logging.getLogger()
# Note that the default logging level used is DEBUG
logger.setLevel(logging.DEBUG)


#Function that handles the reply statement
def make_reply(msg, frm):
    
    print(msg)
	# Switching b/w messages
    switcher = {
        '/start' : start_msg,
		'/uname' : uname_config,
		'/update' : update_ics
    }

    rep = switcher.get(msg,def_func)
    rep(msg,frm)
    # bot.send_message(reply,frm)


def start_msg(msg,frm):
	cparse = cfg.ConfigParser()
	cparse.read(config)
	last_update = None
	if cparse.has_option(str(frm),'last_update'):
		last_update = datetime.datetime.strptime(cparse[str(frm)]['last_update'],'%Y-%m-%d %H:%M:%S')
	if last_update is None:
		reply = 'Change your username and password with /uname and create the ics files with /update'
	else:
		reply = f'Last ics file update was done on {humanize.naturaltime(datetime.datetime.now() - last_update)}.To force an update, use /update command '
	
	bot.send_message(reply,frm)
	# return reply

def uname_config(msg,frm):
	global update_id	
	bot.send_message("Enter your fb username:",frm)
	print ("Waiting for username...")
	#Reading the reply
	#NOTE: Not the most elegant way, or the most optimised, need to write a proper function to handle this
	#May crash if the user takes too long to reply
	# May give the wrong output if more than one user chats with the bot
	
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
	
	bot.send_message("Enter your fb password:",from_)
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
	bot.send_message(reply,frm)
	parser = cfg.ConfigParser()
	parser.read(config_user)
	# checks if the current users creds are available
	if not(parser.has_section(f"DRIVE{frm}")):
		bot.init__drivefield(config_user,frm,uname,passwd)

# Runs the fb2cal code
def update_ics(msg,frm):
	parser = cfg.ConfigParser()
	cfgparser = cfg.ConfigParser()
	parser.read(config_user)
	global last_update
	last_update = datetime.datetime.now()
	last_update = utc.localize(last_update)
	cfgparser.read(config)
	if not cfgparser.has_section(str(frm)):
		cfgparser.add_section(str(frm))
	cfgparser[str(frm)]['last_update'] = last_update.strftime("%Y-%m-%d %H:%M:%S")

	# checks if the current users creds are available
	if parser.has_option(f"AUTH{frm}","fb_email"):
		# os.system(f'python fb2cal/src/fb2cal.py {frm}')
		logger.info(".ics file updation called")
		bot.send_message("Updated",frm)
	else:
		bot.send_message("Sorry, no username/ password found. Run the /uname command and try again",frm)
	
	with open(config,'w') as cfgfile:
		cfgparser.write(cfgfile)
	
	print("Exec")

# THe default function, that gives all the birthdays in a given period
def def_func(msg,frm):
	# try:
	buffer = msg.split(' ')
	# Splits the message into 2 parts, assuming that it is in the format "<num> <unit>"
	if (len(buffer) > 1):
		if buffer[0] >= '0' and buffer[0] <= '9':
			# try:
			no = int(buffer[0])				
			if buffer[1] == 'month' or buffer[1] == 'months' :
				# no = int(buffer[0])
				print("Inside month, ",no)
				k = datetime.datetime.now() + relativedelta(months = no)
				
				k = utc.localize(k) 
				reply = within_limits(frm, k)
				print("Trying for reply, ",reply)
			elif buffer[1] == 'day' or buffer[1] == 'days':
				# no = int(buffer[0])
				print("Inside day, ",no)				
				k = datetime.datetime.now() + relativedelta(days = no)
				k = utc.localize(k) 
				print(k)
				reply = within_limits(frm,k) 
			elif buffer[1] == 'week' or buffer[1] == 'weeks':
				# no = int(buffer[0])
				print("Inside week, ",no)
				k = datetime.datetime.now() + relativedelta(weeks = no)
				k = utc.localize(k) 
				reply = within_limits(frm,k)
			else:
				reply = "Try Again"
		else:
			reply = "Try Again"	
	else:
		reply = "Try Again"
	print("reply is ", reply)
	bot.send_message(reply,frm)
	# return reply

#The infinite loop that checks for replies
while True:
	print ("...")
	last_update = None
	cparse = cfg.ConfigParser()
	cparse.read(config)
	# Checking for last update
	for i in cparse.sections() :
		if cparse.has_option(i,'last_update'):
			last_update = datetime.datetime.strptime(cparse[i]['last_update'],'%Y-%m-%d %H:%M:%S')git
		if last_update is not None:
			if (datetime.datetime.now() - last_update).days > 0:
				logger.info("Updating ICS since last updation was more than a day ago")
				update_ics('updating',i)



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
			make_reply(message, from_)