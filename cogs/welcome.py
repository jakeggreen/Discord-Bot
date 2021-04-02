from discord.ext.commands import Cog
from discord.ext.commands import command
import discord

class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_member_join(self, member):
		await bot.send_message(discord.utils.get(server.channels, name = "channel_name"), (f'{member} has joined {member.guild.name}.'))

	async def on_member_remove(self, member):
		await bot.send_message(discord.utils.get(server.channels, name = "channel_name"), (f'{member} has left {member.guild.name}.'))

	async def on_message(self, message):
		# message.channel.send(f'Hello {message.author}')
		pass

def setup(bot):
	bot.add_cog(Welcome(bot))