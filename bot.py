import requests
import json
import configparser as cfg

class tel_chatbot():

	def __init__(self, config):
		self.token = self.read_from_cfg(config)
		self.base = "https://api.telegram.org/bot{}/".format(self.token)

	def get_updates(self, offset = None):
		url = self.base + "/getUpdates?timeout=100";
		if offset:
			url = url + "&offset={}".format(offset + 1)
		r = requests.get(url)

		return json.loads(r.content)

	def send_message(self, msg, chatid):
		url = self.base + "/sendMessage?chat_id={}&text={}".format(chatid,msg)
		if msg is not None:
			requests.get(url)

	def read_from_cfg(config):
		parser = cfg.ConfigParser()
		parser.read(config)
		return parser.get('creds', 'token')