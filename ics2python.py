# Handles parsing the .ics file
from ics import Calendar
import datetime
import pytz
from dateutil.relativedelta import relativedelta

# from bot import tel_chatbot 

utc=pytz.UTC
# .ics file location



# Reading the .ics file and returning values/events within a given time frame
def within_limits(frm,x = None):
	src = f"fb2cal/src/files/birthdays{frm}.ics"
	file = open(src,encoding='utf8')
	print("File Successfully opened")
	text = file.read()
	cal = Calendar(text)
	cur_date = datetime.datetime.now()
	cur_date = utc.localize(cur_date) 
	val = []
	for e in list(cal.timeline):
		# e.begin = utc.localize(e.begin)
		if e.begin < x and e.begin > cur_date:
			val.append("{} is {} ".format(e.name, e.begin.humanize()))
	return val
