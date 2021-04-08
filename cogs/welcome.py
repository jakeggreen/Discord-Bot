from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.utils import get
import discord

class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_member_join(self, member):
		channel = member.guild.system_channel
		await channel.send(f'{member.display_name} has joined {member.guild.name}.')

	@Cog.listener()
	async def on_member_remove(self, member):
		channel = member.guild.system_channel
		await channel.send(f'{member.display_name} has left {member.guild.name}.')

def setup(bot):
	bot.add_cog(Welcome(bot))