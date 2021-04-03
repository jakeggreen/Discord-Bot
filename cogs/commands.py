from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Member
from discord import Embed
import discord


#For the API requests
import requests
import json
import datetime

#Sets the message delete time i.e. command messages will delete after 60 seconds.
DELETE_TIME = 60

class Commands(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="map")
	async def map(self, ctx):
		"""Shows information about the current and upcoming map rotations for Apex Legends, based on data from the Mozambique.re API.
		N.B. Might not always be accurate."""
		APIKey_file = open('MozHere API Key.txt', 'rt')
		APIKey = APIKey_file.read()
		payload = {}
		headers = {}
		url = 'https://api.mozambiquehe.re/maprotation?auth=' + APIKey
		response = requests.request('GET', url, headers=headers, data=payload)
		map_rotation_data = response.json()
		map_name = map_rotation_data.get('current').get('map')
		start = map_rotation_data.get('current').get('readableDate_start')
		end = map_rotation_data.get('current').get('readableDate_end')
		map_time_remaining = str(map_rotation_data.get('current').get('remainingTimer'))
		next_map_name = map_rotation_data.get('next').get('map')
		next_map_start = str(map_rotation_data.get('next').get('readableDate_start'))

		embed = Embed(title=f'Apex Legends Map Rotation', description=f'Shows the current and upcoming maps on Apex Legends')
		embed.add_field(name=f'Current Map', value=f'{map_name} for {map_time_remaining}')
		embed.add_field(name=f'Next Map', value=f'{next_map_name} starts in {next_map_start}')
		print('Length of the embed is ' + str(len(embed)))

		await ctx.send(embed=embed, delete_after=DELETE_TIME)

	@command(name="members")
	async def members(self, ctx):
		members = ctx.guild.members.display_name
		print(members)
		# memberList = []
		# for member in ctx.guild.members:
		# 	if not member == 'Apex Stats':
		# 		memberList.append(member.display_name)
		# 	else:
		# 		pass
		embed = Embed(title=f'Server Members List',
					description=f'Shows the current members of the server',
					colour=ctx.author.colour)
		embed.add_field(name=f'Member List', value=f'{members}', inline=True)
		await ctx.send(embed=embed, delete_after=DELETE_TIME)
		# await ctx.send([f'{name}' for name in memberList], delete_after=DELETE_TIME)

	@command(name="games")
	async def games(self, ctx, player):
		"""Searches the Mozambique.re API for recent session data for player - use '.members' to see list of server members. 
		Members of the server should set their nickname equal to their Steam/Origin name to allow searching."""
		APIKey_file = open('Apex.txt', 'rt')
		APIKey = APIKey_file.read()
		url = 'https://public-api.tracker.gg/v2/apex/standard/profile/origin/'
		payload = {}
		headers = {'TRN-Api-Key': APIKey}
		session_data = list();

		full_url = url + player + '/sessions'
		response = requests.request('GET', full_url, headers=headers, data=payload)
		player_data = response.json()
		#check to see if player data is available
		if player_data.get('data') and player_data.get('data').get('items'):
			#get the start and end dates for matches
			for dates in player_data.get('data').get('items'):
				startdate = datetime.datetime.strptime(dates['metadata']['startDate']['value'],'%Y-%m-%dT%H:%M:%S.%fZ')
				enddate = datetime.datetime.strptime(dates['metadata']['endDate']['value'],'%Y-%m-%dT%H:%M:%S.%fZ')
				#for each match get the legend used and the ending rank score
				for matches in dates.get('matches'):
					legend = matches['metadata']['character']['displayValue']
					rankscore = matches['stats']['rankScore']['value']
					await ctx.send(f'{player} - Start: {startdate}, End: {enddate}. Played with: {legend}, Rank: {rankscore}', delete_after=DELETE_TIME);

	@command(name="kills")
	async def kills(self, ctx):
		"""Searches the Mozambique.re API for legend kills data for player - use '.members' to see list of server members. 
		Members of the server should set their nickname equal to their Steam/Origin name to allow searching."""
		print("in kills script")
		APIKey_file = open("Apex.txt", "rt")
		APIKey = APIKey_file.read()
		player_username = ctx.author.display_name
		all_legend_names_list = ["Bloodhound", "Gibraltar", "Lifeline", "Pathfinder", "Wraith", "Bangalore", "Caustic", "Mirage", 
		"Octane", "Wattson", "Crypto", "Revenant", "Loba", "Rampart", "Horizon", "Fuse"]
		all_legend_names_set = set(all_legend_names_list)
		payload = {}
		headers = {'TRN-Api-Key': APIKey}
		legend_data = list()
		url = 'https://public-api.tracker.gg/v2/apex/standard/profile/origin/' + player_username + '/segments/legend'
		response = None
		try:
			response = requests.request("GET", url, headers=headers, data=payload)
		except Exception as e:
			print(e)
		print("status code " + str(response.status_code))
		player_data = response.json()
		for legend in all_legend_names_set:
			kills = 0;
			try:
				for item in player_data["data"]:
					if item.get("metadata").get("name") == legend:
						if item.get("stats") and item.get("stats").get("kills") and item.get("stats").get("kills").get("value"):
							kills = int(item["stats"]["kills"]["value"])
			except Exception:
				pass
			await ctx.send(f'{ctx.author.mention} - {legend} kills: {kills}', delete_after=DELETE_TIME)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("commands")

def setup(bot):
	bot.add_cog(Commands(bot))


	

