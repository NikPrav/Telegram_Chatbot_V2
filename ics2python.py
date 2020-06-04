from ics import Calendar
import datetime
import pytz
from dateutil.relativedelta import relativedelta
import numpy as np
# from bot import tel_chatbot 

utc=pytz.UTC
# import fi
src = "files/birthdays.ics"
file = open(src,"r")
text = file.read()
cal = Calendar(text)

# for e in list(cal.timeline):
# 	# e = list(cal.timeline)[0]
# 	print("{} is {} ".format(e.name, e.begin))

# k = None

def within_limits(x = None):
	# cur_date = datetime.datetime.now();
	val = []
	for e in list(cal.timeline):
		# e.begin = utc.localize(e.begin)
		if e.begin < x :
			val.append("{} is {} ".format(e.name, e.begin.humanize()))

	return val


# k = datetime.datetime.now() + relativedelta(months = 2)
# k = utc.localize(k) 
# y = within_limits(k)
# print(y)