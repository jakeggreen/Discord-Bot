# Discord Python bot
import os

import discord
from discord.ext import commands

#Pull in bot token from text file
Token_file = open('token.txt', 'rt')
token = Token_file.read()

# client = discord.Client()
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	 print(f'{client.user} has connected to Discord!')

client.run(token)


