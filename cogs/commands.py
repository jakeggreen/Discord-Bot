from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Member
from discord import Embed
import discord
import json
from datetime import datetime, timedelta
from discord.errors import HTTPException, NotFound
from lib.api import Api, Mozam, GG_Tracker
from typing import Optional


all_legend_names_list = ["Bloodhound", "Gibraltar", "Lifeline", "Pathfinder", "Wraith", "Bangalore", "Caustic", "Mirage", 
		"Octane", "Wattson", "Crypto", "Revenant", "Loba", "Rampart", "Horizon", "Fuse"]


class Commands(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.mozam_api = Mozam()
		self.gg_tracker_api = GG_Tracker()
		self.msg_delete_time = 60

	@command(name="map", brief='Show the current and upcoming map rotations for Apex Legends')
	async def map(self, ctx):
		"""Shows information about the current and upcoming map rotations for Apex Legends, based on data from the Mozambique.re API.
		N.B. Might not always be accurate."""
		map_rotation_data = self.mozam_api.getMaps()
		map_name = map_rotation_data.get('current').get('map')
		map_time_remaining = map_rotation_data.get('current').get('remainingTimer')
		next_map_name = map_rotation_data.get('next').get('map')
		next_map_start = datetime.fromtimestamp(map_rotation_data.get('next').get('start'), self.bot.tz).strftime(self.bot.date_f1)

		embed = Embed(title=f'Apex Legends Map Rotation', description=f'Shows the current and upcoming maps on Apex Legends')
		embed.add_field(name=f'Current Map', value=f'{map_name} for another {map_time_remaining}', inline=True)
		embed.add_field(name=f'Next Map', value=f'{next_map_name} starts at {next_map_start}', inline=True)
		await ctx.message.delete()
		await ctx.send(embed=embed, delete_after= self.msg_delete_time)
		
	@command(name="members", brief='Return list of server members')
	async def members(self, ctx):
		memberList = []
		msg = ''
		for member in ctx.guild.members:
			if not member.bot:
				memberList.append(member.display_name)
			else:
				pass
		for name in memberList:
			msg += f'{name}\n'
		embed = Embed(title=f'Server Members List',
					description=f'Shows the current members of the server',
					colour=ctx.author.colour)
		embed.add_field(name=f'Member List', value=msg)
		await ctx.message.delete()
		await ctx.send(embed=embed ,delete_after= self.msg_delete_time)

	@command(name="games", brief='Lists all available session data for player/self')
	async def games(self, ctx, player: Optional[str]):
		"""Searches the tracker.gg API for recent session data for player - use '.members' to see list of server members. 
		Members of the server should set their nickname equal to their Steam/Origin name to allow searching."""
		if not player: 
			username = ctx.author.display_name
		else:
			username = player
		player_data = self.gg_tracker_api.getGames(username)
		#check to see if player data is available
		# if player_data.get('data') and player_data.get('data').get('items'):
		msg = ""
		for dates in player_data.get('data').get('items'):
			start_dt = datetime.strptime(dates['metadata']['startDate']['value'],'%Y-%m-%dT%H:%M:%S.%fZ').astimezone(self.bot.tz)
			end_dt = datetime.strptime(dates['metadata']['endDate']['value'],'%Y-%m-%dT%H:%M:%S.%fZ').astimezone(self.bot.tz)
			begin = start_dt.strftime(self.bot.date_f1)
			duration = str(end_dt - start_dt)
			for matches in dates.get('matches'):
				legend = matches['metadata']['character']['displayValue']
				rankscore = matches['stats']['rankScore']['value']
				msg += f'\n{begin}, Duration: {duration} . Played with: {legend}, RP: {rankscore}'
		embed = Embed(title=player, description=msg)
		await ctx.message.delete()
		await ctx.send(embed=embed, delete_after= self.msg_delete_time)
		# else:
		# 	await ctx.message.delete()
		# 	await ctx.send(f'No session data found for username {player}', delete_after= self.msg_delete_time)

	@games.error
	async def games_error(self, ctx, exc):
		await ctx.message.delete()
		if isinstance(exc.original, HTTPException):
			await ctx.send(f'An error occurred.', delete_after= self.msg_delete_time)
		else:
			await ctx.send(f'No session data found. Please try another player name.', delete_after= self.msg_delete_time)

	@command(name="kills", brief='Kill data for player for each legend')
	async def kills(self, ctx, player: Optional[str]):
		"""Searches the Mozambique.re API for legend kills data for player - use '.members' to see list of server members. 
		Members of the server should set their nickname equal to their Steam/Origin name to allow searching."""		
		if not player: 
			username = ctx.author.display_name
		else:
			username = player
		player_data = self.gg_tracker_api.getKills(username)
	
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
		embed = Embed(title=username, description=msg)
		await ctx.message.delete()
		await ctx.send(embed=embed, delete_after= self.msg_delete_time)

	@kills.error
	async def kills_error(self, ctx, exc):
		await ctx.message.delete()
		if isinstance(exc.original, HTTPException):
			await ctx.send(f'An error occurred.', delete_after= self.msg_delete_time)
		else:
			await ctx.send(f'No kill data found. Please try another player name.', delete_after= self.msg_delete_time)

	@command(name='status', dsecription='Shows current server status by server type.')
	async def server_status(self, ctx):
		server_status_data =  self.mozam_api.getServerStatus()

		servers_list = ('Origin_login','EA_accounts','ApexOauth_Steam','ApexOauth_Crossplay','ApexOauth_PC')

		location_list = ('EU-West','EU-East')

		embed = Embed(title=f'Apex Legends Server Status', description=f'Shows current server status by server type.')
		embed.set_footer(text='See more details at https://apexlegendsstatus.com')

		for server_type, item in server_status_data.items():
			if server_type in servers_list:
				for location in item.items():
					server_location = location[0]
					if server_location in location_list:
						server_status = '\U00002705' if location[1]['Status'] == 'UP' else '\U0000274C'
						time_stamp = datetime.fromtimestamp(location[1]['QueryTimestamp'], self.bot.tz).strftime('%H:%M:%S')
						embed.add_field(name=f'{server_type}:\n', value=f'{server_location}:\n{server_status}\nTimestamp:\n{time_stamp}', inline=True)
		
		await ctx.message.delete()
		await ctx.send(embed=embed, delete_after= self.msg_delete_time)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("commands")

def setup(bot):
	bot.add_cog(Commands(bot))


	

