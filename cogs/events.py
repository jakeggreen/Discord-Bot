from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from discord.utils import get
import discord
import datetime
import time

class Events(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.msg_delete_time = 600

	def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

	@Cog.listener()
	async def on_message(self, message):
		# message.channel.send(f'Hello {message.author}')
		pass

	@Cog.listener()
	async def change_presence(member, activity, status):
		activity = member.activity.name
		status = member.status
		print(member.display_name, activity, status)

	@Cog.listener()
	async def on_member_update(self, before, after):
		print(before.activity, before.status, after.activity, after.status)
		if before.status != 'online' and (before.activity == None and after.activity == None): #doesn't give status updates whilst in a game
			channel = before.guild.system_channel
			embed = Embed(title=f'{after.display_name} is now {after.status}!')
			await channel.send(embed=embed, delete_after=self.msg_delete_time)

		if before.activity == None and after.activity != None:
			channel = before.guild.system_channel
			# print(after.activity.party)
			try:
				party_min = after.activity.party['size'][0]
				party_max = after.activity.party['size'][1]
				print(party_min, party_max)
				await channel.send(f'{after.display_name} is now playing {after.activity.name}. Started at: {after.activity.start}. Party size is {party_min}/{party_max}')

			except Exception:
				timer = countdown(7200)
				start = after.activity.start.strftime('%d-%m-%y %H:%M:%S')
				embed = Embed(title=f'{after.display_name} is now playing\n{after.activity.name}')
				embed.add_field(name=f'Started at:', value=start)
				embed.add_field(name=f'Countdown:', value=timer)
				embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/687049202089721910.png?v=1')
				await channel.send(embed=embed)
		
		if before.activity != None and after.activity == None:
			channel = before.guild.system_channel
			embed = Embed(title=f'{after.display_name} has finished playing\n{before.activity.name}')
			embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/687049202089721910.png?v=1')
			await channel.send(embed=embed)

def setup(bot):
	bot.add_cog(Events(bot))