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
	async def change_presence(member, activity=None, status=None):
		activity = member.activity.name
		status = member.status
		print(member, activity, status)

def setup(bot):
	bot.add_cog(Events(bot))