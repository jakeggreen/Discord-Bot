import requests
import json
import datetime
import traceback

class Api(object):
	def __init__(self, name, base_url, default_headers, default_params, auth_method, std_date_format):
		self.name = name
		self.base_url = base_url
		self.default_headers = default_headers
		self.default_params = default_params
		self.auth_method = auth_method
		self.std_date_format = std_date_format

	def makeHTTPRequest(self, http_method, url_extension, headers = {}, params = [], payload = {}):
		resp = requests.request(http_method, self.base_url + url_extension, headers = self.default_headers | headers,params= self.default_params+params, data=payload)
		resp.raise_for_status()
		return resp

class Mozam(Api):
	def __init__(self):
		name = 'Mozambique Here'
		base_url = 'https://api.mozambiquehe.re'
		APIKey_file = open('MozHere API Key.txt', 'rt')
		self.APIKey = APIKey_file.read()
		default_params = [('auth', self.APIKey)]
		default_headers = {}
		std_dt_format = None
	
		super().__init__(name, base_url, default_headers, default_params, 'URL Params',  std_dt_format)

	def getMaps(self):
		response = self.makeHTTPRequest('GET','/maprotation')
		return response.json()

	def getServerStatus(self):
		response = self.makeHTTPRequest('GET', '/servers')
		return response.json()

class GG_Tracker(Api):
	def __init__(self):
		name = 'GG Tracker'
		base_url = 'https://public-api.tracker.gg/v2/apex'
		APIKey_file = open('Apex.txt', 'rt')
		self.APIKey = APIKey_file.read()
		default_params = []
		default_headers = {'TRN-Api-Key': self.APIKey}
		std_dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'

		super().__init__(name, base_url,default_headers, default_params, 'Non-Standard Header', std_dt_format)

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