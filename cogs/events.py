from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.utils import get
import discord

class Events(Cog):
	def __init__(self, bot):
		self.bot = bot

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
		if before.activity == None:
			channel = before.guild.system_channel
			await channel.send(f'{before.display_name} is now {after.status}!')
		else:
			channel = before.guild.system_channel
			party_min = after.activity.party.get('size')[0]
			party_max = after.activity.party.get('size')[1]
			await channel.send(f'{before.display_name} is now playing {after.activity.name}. Party size is {party_min}/{party_max}')



def setup(bot):
	bot.add_cog(Events(bot))