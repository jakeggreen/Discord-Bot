# Discord Python bot

import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from glob import glob
from discord.ext.commands import CommandNotFound

#Set the command prefix character
PREFIX = '.'

#Set list comprehension for the cogs available for the bot (includes command script)
COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
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
		await self.change_presence(activity=discord.Game('Apex Legends'))

	async def on_disconnect(self):
		print(f'{self.user} has disconnected from Discord')

	async def on_error(self, err, *args, **kwargs):
		if err == "on command error":
			await args[0].send(f'Something went wrong.')
		raise

	async def on_command_completion(self, ctx):
		print(f'{ctx.author.display_name} successfully called {ctx.command}.')

	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			pass

		# elif hasattr(exc, "original"):
		# 	raise exc.original

		# else:
		# 	raise exc

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			print(f'{self.user} is ready')

		else:
			print(f'{self.user} reconnected')

Bot = Bot()

