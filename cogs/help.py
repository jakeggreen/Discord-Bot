from discord.ext.commands import Cog
from discord.ext.commands import command
# from discord.ext.menus import MenuPages, ListPageSource
from discord.utils import get
from discord import Embed
from typing import Optional


def syntax(command):
	cmd_and_aliases = '|'.join([str(command), *command.aliases])
	params = []

	for key, value in command.params.items():
		#makes sure it doesn't pick up itself
		if key not in ('self','ctx'):
			#shows optional and mandatory fields in the variables for a command
			params.append(f'[{key}]' if 'NoneType' in str(value) else f'<{key}>')

	params = ' '.join(params)

	return f'{cmd_and_aliases} {params}'

class Help(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.remove_command('help') #remove the inbuilt help command for help

	async def cmd_help(self, ctx, command):
		embed = Embed(title=f'Help with ".{command}"',
					description= syntax(command),
					colour=ctx.author.colour)
		embed.add_field(name='Command description', value=command.help)
		await ctx.send(embed=embed, delete_after=60)

	@command(name='help')
	async def show_help(self, ctx, cmd: Optional[str]):
		if cmd is None:
			pass

		else:
			if (command := get(self.bot.commands, name=cmd)):
				await self.cmd_help(ctx, command)

			else:
				await ctx.send(f'That command does not exist')


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up('help')


def setup(bot):
	bot.add_cog(Help(bot))