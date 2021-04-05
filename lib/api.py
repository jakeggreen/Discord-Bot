import requests
import json
import datetime

class Api(object):
	def __init__(self, name, base_url, default_headers, default_params, auth_method):
		self.name = name
		self.base_url = base_url
		self.default_headers = default_headers
		self.default_params = default_params
		self.auth_method = auth_method

	def makeHTTPRequest(self, http_method, url_extension, headers = {}, params = [], payload = {}):
		try:
			resp = requests.request(http_method, self.base_url + url_extension, headers = self.default_headers | headers, params= self.default_params+params, data=payload)
			resp.raise_for_status()
			return resp
		except requests.HTTPError as exception:
			print(exception)

class Mozam(Api):
	def __init__(self):
		name = 'Mozambique Here'
		base_url = 'https://api.mozambiquehe.re'
		APIKey_file = open('MozHere API Key.txt', 'rt')
		self.APIKey = APIKey_file.read()
		default_params = [('auth', self.APIKey)]
		default_headers = {}

		super().__init__(name, base_url, default_headers, default_params, 'URL Params')

	def getMaps(self):
		response = self.makeHTTPRequest('GET','/maprotation')
		return response.json()

class GG_Tracker(Api):
	def __init__(self):
		name = 'GG Tracker'
		base_url = 'https://public-api.tracker.gg/v2/apex'
		APIKey_file = open('Apex.txt', 'rt')
		self.APIKey = APIKey_file.read()
		default_params = []
		default_headers = {'TRN-Api-Key': self.APIKey}

		super().__init__(name, base_url,default_headers, default_params, 'Non-Standard Header')

	def getKills(self, username):
		response = self.makeHTTPRequest('GET','/standard/profile/origin/' + username + '/segments/legend')
		return response.json()

	def getGames(self, username):
		response = self.makeHTTPRequest('GET','/standard/profile/origin/' + username + '/sessions')
		return response.json()

#code block for testing when running in-file.
if __name__ == '__main__':
	moz = Mozam()
	print(moz.getMaps())