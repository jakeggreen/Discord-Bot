from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.utils import get
import discord

class Events(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.msg_delete_time = 60

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
		if before.status != 'online':
			channel = before.guild.system_channel
			await channel.send(f'{after.display_name} is now {after.status}!', delete_after=self.msg_delete_time)

		if before.activity == None and after.activity != None:
			channel = before.guild.system_channel
			try:
				party_min = after.activity.party['size'][0]
				party_max = after.activity.party['size'][1]
				print(party_min, party_max)
				await channel.send(f'{after.display_name} is now playing {after.activity.name}. Party size is {party_min}/{party_max}')
			except Exception:
				await channel.send(f'{after.display_name} is now playing {after.activity.name}.')
		
		if before.activity != None and after.activity == None:
			channel = before.guild.system_channel
			await channel.send(f'{after.display_name} has finished playing {before.activity.name}.')

def setup(bot):
	bot.add_cog(Events(bot))