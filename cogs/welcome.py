from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.utils import get
import discord

class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.msg_delete_time = 60

	@Cog.listener()
	async def on_member_join(self, member):
		channel = member.guild.system_channel
		embed = Embed(title=f'Welcome to {member.guild.name}!', description=f'Please remember the rules and have fun!')
		embed.add_field(name=f'Rules:', values=f'Please set your nickname on the server equal to your username on Origin/Steam')
		embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/687049202089721910.png?v=1')
		embed.set_footer(text=f'Admins: {member.guild.owner.display_name}')
		embed.set_image(url='https://cdn.discordapp.com/emojis/687049202089721910.png?v=1')

		embed_welcome = Embed(title=f'{member.display_name} has joined {member.guild.name}.')

		await channel.send(embed=embed_welcome)
		await channel.send(embed=embed, delete_after=self.msg_delete_time)

	@Cog.listener()
	async def on_member_remove(self, member):
		channel = member.guild.system_channel
		await channel.send(f'{member.display_name} has left {member.guild.name}.')

def setup(bot):
	bot.add_cog(Welcome(bot))