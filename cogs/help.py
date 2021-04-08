from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.menus import MenuPages, ListPageSource
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


class HelpMenu(ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx

		super().__init__(data, per_page=4)

	async def write_page(self, menu, fields=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(self.entries)

		embed = Embed(title='Help',
				description='Welcome to the BBOZ help menu.',
				colour=self.ctx.author.colour)
		#footer to show the number of commands available
		embed.set_footer(text=f'{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.')

		for name, value in fields:
			embed.add_field(name=name, value=value, inline=False)

		return embed

	async def format_page(self, menu, entries):
		fields = []

		for entry in entries:
			fields.append((syntax(entry), entry.brief or "No description"))

		return await self.write_page(menu, fields)


class Help(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.remove_command('help') #remove the inbuilt help command for help

	async def cmd_help(self, ctx, command):
		embed = Embed(title=f'Help with ".{command}"',
					description= f'Command name: {syntax(command)}',
					colour=ctx.author.colour)
		embed.add_field(name='Command description', value=command.help)
		await ctx.send(embed=embed, delete_after=60)

	@command(name='help', brief='Further help on a given command, fields in \\<> are optional parameters')
	async def show_help(self, ctx, cmd: Optional[str]):
		if cmd is None:
			await ctx.message.delete()
			menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)),
							clear_reactions_after=True,
							delete_message_after=True,
							timeout=60.0)
			await menu.start(ctx)

		else:
			if (command := get(self.bot.commands, name=cmd)):
				await self.cmd_help(ctx, command)
				await ctx.message.delete()

			else:
				await ctx.message.delete()
				await ctx.send(f'That command does not exist')


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up('help')


def setup(bot):
	bot.add_cog(Help(bot))