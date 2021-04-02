# Discord Python bot

import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from glob import glob
from asyncio import sleep

#Set the command prefix character
PREFIX = '.'

#Set list comprehension for the cogs available for the bot (includes command script)
COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cogs):
		setattr(self, cog, True)
		print(f'{cog} cog ready.')

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(Bot):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.cogs_ready = Ready()
		self.guild = None

		super().__init__(
			command_prefix = PREFIX,
			intents=discord.Intents.all())

	def setup(self):
		for cog in COGS:
			self.load_extension(f'cogs.{cog}')
			print(f'{cog} cog loaded.')

		print(f'Setup complete.')

	def run(self):

		print(f'Running setup...')
		self.setup()

		with open('token.txt', 'rt') as Token_file:
			self.TOKEN = Token_file.read()

		print('Running bot...')
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print(f'{self.user} has connected to Discord')

	async def on_disconnect(self):
		print(f'{self.user} has disconnected from Discord')

	async def on_ready(self):
		if not self.ready:

			# while not self.cogs_ready.all_ready():
			# 	await sleep(0.5)

			self.ready = True
			print(f'{self.user} is ready')

		else:
			print(f'{self.user} reconnected')

	# async def on_member_join(member):
	# 	print(f'{member} has joined {member.guild.name}.')

	# async def on_member_remove(member):
	# 	print(f'{member} has left {member.guild.name}.')

	# async def on_message(message):
	# 	message.channel.send(f'Hello {message.author}')

Bot = Bot()

