# Discord Python bot
import os
import discord
from discord.ext import commands
import requests
import json
import datetime

#Pull in bot token from text file
Token_file = open('token.txt', 'rt')
token = Token_file.read()

intents = discord.Intents.default()
intents.members = True

# client = discord.Client(intents=intents)

#Set client variable equal to instance of bot
client = commands.Bot(command_prefix = '.', intents=intents)

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord')

@client.event
async def on_member_join(member):
	member.server.default_channel.send(f'{member} has joined {member.guild.name}.')
	# print(f'Hello Peter')

@client.event
async def on_member_remove(member):
	server = member.server
	default_channel = server.default_channel
	client.send_message(default_channel, f'{member} has left {member.guild.name}.')
	# print(f'Goodbye Peter')

# @client.event
# async def on_message(message):
# 	message.channel.send(f'Hello {message.author}')

@client.command(name="map")
async def map(ctx):
	APIKey_file = open('MozHere API Key.txt', 'rt')
	APIKey = APIKey_file.read()
	payload = {}
	headers = {}
	url = 'https://api.mozambiquehe.re/maprotation?auth=' + APIKey
	response = requests.request('GET', url, headers=headers, data=payload)
	map_rotation_data = response.json()
	map_name = map_rotation_data.get('current').get('map')
	start = map_rotation_data.get('current').get('readableDate_start')
	end = map_rotation_data.get('current').get('readableDate_end')
	map_time_remaining = str(map_rotation_data.get('current').get('remainingTimer'))
	next_map_name = map_rotation_data.get('next').get('map')
	next_map_start = str(map_rotation_data.get('next').get('readableDate_start'))
	await ctx.send(f'Current map is {map_name} for another {map_time_remaining}')
	await ctx.send(f'Next map is {next_map_name} from {next_map_start}')

@client.command(name="games")
async def games(ctx, player):

	class Match:
		def __init__(self, player, startdate, enddate, legend, rankscore):
			self.player = player
			self.startdate = startdate
			self.enddate = enddate
			self.legend = legend
			self.rankscore = rankscore
		def getPlayer(self):
			return self.player
		def getStart(self):
			return self.startdate
		def getEnd(self):
			return self.enddate
		def getLegend(self):
			return self.legend
		def getRank(self):
			return self.rankscore

		def getPlayerName(player):
			return Match.getPlayer()

	#pull in API key from text file
	APIKey_file = open('Apex.txt', 'rt')
	APIKey = APIKey_file.read()
	url = 'https://public-api.tracker.gg/v2/apex/standard/profile/origin/'
	payload = {}
	headers = {'TRN-Api-Key': APIKey}
	session_data = list();

	full_url = url + player + '/sessions'
	response = requests.request('GET', full_url, headers=headers, data=payload)
	player_data = response.json()
	#check to see if player data is available
	if player_data.get('data') and player_data.get('data').get('items'):
		#get the start and end dates for matches
		for dates in player_data.get('data').get('items'):
			startdate = datetime.datetime.strptime(dates['metadata']['startDate']['value'],'%Y-%m-%dT%H:%M:%S.%fZ')
			enddate = datetime.datetime.strptime(dates['metadata']['endDate']['value'],'%Y-%m-%dT%H:%M:%S.%fZ')
			#for each match get the legend used and the ending rank score
			for matches in dates.get('matches'):
				legend = matches['metadata']['character']['displayValue']
				rankscore = matches['stats']['rankScore']['value']
				session_data.append(Match(player, startdate, enddate, legend, rankscore));

	for match in session_data:
		# print('-----\r' + Match.getPlayer(match) + '\r-----')
		print(Match.getPlayer(match) + ' - Start: ' + str(Match.getStart(match)) + ', End: ' 
	+ str(Match.getEnd(match)) + ', Played With: ' + str(Match.getLegend(match)) + ', Rank: ' + str(Match.getRank(match)))

client.run(token)


