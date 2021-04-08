import pytz

class Bot_Settings(object):
	def __init__(self):
		print('initialising bot settings')
		self.PREFIX = '.'
		self.tz = pytz.timezone('Europe/London')
		self.date_f1 = '%d-%m-%Y %H:%M:%S'