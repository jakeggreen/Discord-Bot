from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Member
from discord import Embed
import discord
import json
import datetime
from lib.api import Api, Mozam, GG_Tracker


all_legend_names_list = ["Bloodhound", "Gibraltar", "Lifeline", "Pathfinder", "Wraith", "Bangalore", "Caustic", "Mirage", 
		"Octane", "Wattson", "Crypto", "Revenant", "Loba", "Rampart", "Horizon", "Fuse"]


class Commands(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.mozam_api = Mozam()
		self.gg_tracker_api = GG_Tracker()
		self.msg_delete_time = 60

	@command(name="map")
	async def map(self, ctx):
		"""Shows information about the current and upcoming map rotations for Apex Legends, based on data from the Mozambique.re API.
		N.B. Might not always be accurate."""
		map_rotation_data = self.mozam_api.getMaps()
		map_name = map_rotation_data.get('current').get('map')
		start = map_rotation_data.get('current').get('readableDate_start')
		end = map_rotation_data.get('current').get('readableDate_end')
		map_time_remaining = str(map_rotation_data.get('current').get('remainingTimer'))
		next_map_name = map_rotation_data.get('next').get('map')
		next_map_start = str(map_rotation_data.get('next').get('readableDate_start'))

		embed = Embed(title=f'Apex Legends Map Rotation', description=f'Shows the current and upcoming maps on Apex Legends')
		embed.add_field(name=f'Current Map', value=f'{map_name} for {map_time_remaining}')
		embed.add_field(name=f'Next Map', value=f'{next_map_name} starts in {next_map_start}')
		#print('Length of the embed is ' + str(len(embed)))
	
		await ctx.send(embed=embed, delete_after= self.msg_delete_time)
		
	@command(name="members")
	async def members(self, ctx):
		memberList = []
		for member in ctx.guild.members:
			if not member == 'Apex Stats':
				memberList.append(member.display_name)
			else:
				pass
		# embed = Embed(title=f'Server Members List',
		# 			description=f'Shows the current members of the server',
		# 			colour=ctx.author.colour)
		# embed.add_field(name=f'Member List', value=[f'{name}' for name in memberList])
		# await ctx.send(embed=embed)
		await ctx.send([f'{name}' for name in memberList])

	@command(name="games")
	async def games(self, ctx, player):
		"""Searches the tracker.gg API for recent session data for player - use '.members' to see list of server members. 
		Members of the server should set their nickname equal to their Steam/Origin name to allow searching."""

		if not player:
			await ctx.send(f'No player name provided');
		
		player_data = self.gg_tracker_api.getGames(player)
		#check to see if player data is available
		if player_data.get('data') and player_data.get('data').get('items'):
			#get the start and end dates for matches
			msg = ""
			for dates in player_data.get('data').get('items'):
				start_dt = datetime.datetime.strptime(dates['metadata']['startDate']['value'],'%Y-%m-%dT%H:%M:%S.%fZ')
				end_dt = datetime.datetime.strptime(dates['metadata']['endDate']['value'],'%Y-%m-%dT%H:%M:%S.%fZ')

				begin = start_dt.strftime('%Y-%m-%d %H:%M')
				duration = str(end_dt - start_dt)
				#for each match get the legend used and the ending rank score
				for matches in dates.get('matches'):
					legend = matches['metadata']['character']['displayValue']
					rankscore = matches['stats']['rankScore']['value']
					msg += f'\n{begin}, Duration: {duration} . Played with: {legend}, RP: {rankscore}'
			await ctx.send(f'{msg}')
		else:
			await ctx.send(f'No session date found for username {player}')

	@command(name="kills")
	async def kills(self, ctx):
		"""Searches the Mozambique.re API for legend kills data for player - use '.members' to see list of server members. 
		Members of the server should set their nickname equal to their Steam/Origin name to allow searching."""
		username = ctx.author.display_name
		player_data = self.gg_tracker_api.getKills(username)

		if player_data is not None:
			msg = ""
			for legend in all_legend_names_list:
				kills = 0;
				try:
					for item in player_data["data"]:
						if item.get("metadata").get("name") == legend:
							if item.get("stats") and item.get("stats").get("kills") and item.get("stats").get("kills").get("value"):
								kills = int(item["stats"]["kills"]["value"])
				except Exception:
					pass
				msg += f'{legend} kills: {kills}\n '
			await ctx.send(f'{ctx.author.mention} \n{msg}')
		else:
			await ctx.send(f'Username {username} not found')

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("commands")

def setup(bot):
	bot.add_cog(Commands(bot))


	

