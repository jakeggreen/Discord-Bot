from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from discord.utils import get
import discord
from datetime import datetime
import time
import lib.util as u

class Events(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.msg_delete_time = 600
		self.status_delete_time = 60

	@Cog.listener()
	async def on_message(self, message):
		pass

	@Cog.listener()
	async def on_member_update(self, before, after):

		if before.status != 'online' and (before.activity == None and after.activity == None): #doesn't give status updates whilst in a game
			channel = before.guild.system_channel
			embed = Embed(title=f'{after.display_name} is now {after.status}!')
			await channel.send(embed=embed, delete_after=self.status_delete_time)

		if before.activity == None and after.activity != None:
			channel = before.guild.system_channel
			start = u.localizeTimezoneStr(after.activity.start, self.bot.tz, self.bot.date_f1)
			embed = Embed(title=f'{after.display_name} is now playing\n{after.activity.name}')
			embed.add_field(name=f'Started at:', value=start, inline=True)
			# embed.add_field(name=f'Countdown:', value=u.countdown(7200), inline=True) -- currently just prints to terminal
			embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/687049202089721910.png?v=1')
			await channel.send(embed=embed)
		
		if before.activity != None and after.activity == None:
			channel = before.guild.system_channel
			embed = Embed(title=f'{after.display_name} has finished playing\n{before.activity.name}')
			embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/687049202089721910.png?v=1')
			await channel.send(embed=embed)

def setup(bot):
	bot.add_cog(Events(bot))