# Discord Python bot
import os
import discord
from discord.ext import commands
import requests
import json

#Pull in bot token from text file
Token_file = open('token.txt', 'rt')
token = Token_file.read()

#Set client variable equal to instance of bot
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	guild = client.fetch_guild()
	print(f'{client.user} has connected to Discord, {client.fetch_guild()}')

# @client.event
# async def on_member_join(member, server):
# 	send(f'{member} has joined {server}.')

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

client.run(token)


