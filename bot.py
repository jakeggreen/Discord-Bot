# Discord Python bot
import traceback
import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from glob import glob
from discord.ext.commands import CommandNotFound
from datetime import datetime
from settings import Bot_Settings
from lib.db import db

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

class Bot(Bot, Bot_Settings):
	def __init__(self):
		self.ready = False
		self.cogs_ready = Ready()
		self.guild = None
		Bot_Settings.__init__(self)

		super().__init__(
			command_prefix = self.PREFIX,
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

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			print(f'{self.user} is ready')

		else:
			print(f'{self.user} reconnected')

	#error handling below

	async def on_error(self, err, *args, **kwargs):
		if err == "on command error":
			await args[0].send(f'Something went wrong.')
		raise

	async def on_command_completion(self, ctx):
		now = datetime.now()
		dt_string = now.strftime(self.date_f1)
		print(f'{dt_string}: {ctx.author.display_name} successfully called command: {ctx.command}.')
		params = ()
		db.execute("INSERT INTO tbl_commands_log VALUES (?, ?, ?)", str(ctx.author.display_name), str(ctx.command), dt_string)
		db.commit()
		db.close()

	async def on_command_error(self, ctx, exc):
		now = datetime.now()
		dt_string = now.strftime(self.date_f1)
		print(f'{dt_string}: {ctx.author.display_name} failed to call command: {ctx.command}.')
		if isinstance(exc, CommandNotFound):
			pass

		elif hasattr(exc, "original"):
			raise exc.original

		else:
			raise exc

Bot = Bot()

