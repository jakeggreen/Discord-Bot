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

@client.command(pass_context=True)
async def chnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention}.')

@client.command(name="members")
async def members(ctx):
	guild = client.get_guild()
	memberList = guild.members
	await ctx.send({memberList})

@client.command(name="games")
async def games(ctx, player):

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
				ctx.send(f'{player} - Start: {startdate}, End: {enddate}. Played with: {legend}, Rank: {rankscore}');

@client.command(name="kills")
async def kills(ctx, member: discord.Member):

	APIKey_file = open("Apex.txt", "rt")
	APIKey = APIKey_file.read()
	player_username = member.display_name
	all_legend_names_list = ["Bloodhound", "Gibraltar", "Lifeline", "Pathfinder", "Wraith", "Bangalore", "Caustic", "Mirage", 
	"Octane", "Wattson", "Crypto", "Revenant", "Loba", "Rampart", "Horizon", "Fuse"]
	all_legend_names_set = set(all_legend_names_list)
	payload = {}
	headers = {'TRN-Api-Key': APIKey}
	legend_data = list();
	url = 'https://public-api.tracker.gg/v2/apex/standard/profile/origin/' + player_username + '/segments/legend'
	response = requests.request("GET", url, headers=headers, data=payload)
	player_data = response.json()
	for legend in all_legend_names_set:
		kills = 0;
		try:
			for item in player_data["data"]:
				if item.get("metadata").get("name") == legend:
					if item.get("stats") and item.get("stats").get("kills") and item.get("stats").get("kills").get("value"):
						kills = int(item["stats"]["kills"]["value"])
		except Exception:
			pass
		await ctx.send(f'{mention.member} - {legend} kills: {kills}');

client.run(token)


