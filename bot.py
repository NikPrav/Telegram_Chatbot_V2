import requests
import json
import configparser as cfg

class tel_chatbot():

	def __init__(self, config):
		self.token = self.read_from_cfg(config)
		self.base = "https://api.telegram.org/bot{}".format(self.token)

	def get_updates(self, offset = None):
		url = self.base + "/getUpdates?timeout=100";
		if offset:
			url = url + "&offset={}".format(offset + 1)

		r = requests.get(url)

		return json.loads(r.content)

	def send_message(self, msg, chatid):
		print(type(msg))
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
			

	def read_from_cfg(self,config):
		parser = cfg.ConfigParser()
		parser.read(config)
		return parser.get('creds', 'token')