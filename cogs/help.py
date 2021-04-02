from discord.ext.commands import Cog
from discord.ext.commands import command

class Help(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.remove_command('help')


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up('help')


def setup(bot):
	bot.add_cog(Help(bot))