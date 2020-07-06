import requests
import json
import configparser as cfg

class tel_chatbot():

	def __init__(self, config):
		self.token = self.read_token_from_cfg(config)
		self.base = "https://api.telegram.org/bot{}".format(self.token)

	def get_updates(self, offset = None):
		url = self.base + "/getUpdates?timeout=100";
		if offset:
			url = url + "&offset={}".format(offset + 1)

		r = requests.get(url)

		return json.loads(r.content)

	def send_message(self, msg, chatid):
		# print(type(msg))
		if type(msg) is str:
			print('Only one in msg')
			url = self.base + "/sendMessage?chat_id={}&text={}".format(chatid,msg)
			if msg is not None:
				requests.get(url)
		else:
			if msg is not None:
				for txt in msg:
					print('multiple in msg')
					url = self.base + "/sendMessage?chat_id={}&text={}".format(chatid,txt)
					requests.get(url)
			

	def read_token_from_cfg(self,config):
		parser = cfg.ConfigParser()
		parser.read(config)
		return parser.get('creds', 'token')

	def read_uname_from_cfg(self,cofig,uid):
		parser = cfg.ConfigParser()
		parser.read(cofg)
		# print(parser.get('uname_{}'.format(uid),'uname'))
		try:
			uname = parser.get('uname_{}'.format(uid),'uname')
			passwd = parser.get('uname_{}'.format(uid),'passwd')
			# print(x)
		except:
			uname = None
			passwd = None

		# print(x)
		return uname,passwd

	def write_uname_to_cfg(self,cofg,uid,uname,passwd):
		# print(cofig)
		parser = cfg.ConfigParser()
		parser.read(cofg)
		sec = 'AUTH{}'.format(uid)
		# print(sec)
		if sec not in parser:
			parser.add_section(sec)
		
		parser[sec]['uname'] = uname
		parser[sec]['passwd'] = passwd
		# print(parser[sec]['uname'])
		with open(cofg,'w') as cfgfile: 
			parser.write(cfgfile)