import discord
from discord.ext import commands
import aiohttp
import json
import random

class xkcdCog(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		
	@commands.command()
	async def xkcd(self,ctx):
		comic_no = random.randint(1,1900)
		url = f"http://xkcd.com/{comic_no}/info.0.json"
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as data:
				new_data = await data.read()
				json_data = json.loads(new_data)
				img = json_data.get("img")
				title = json_data.get("title")
				alt = json_data.get("alt")
				response = discord.Embed(color=0xffb6b9)
				response.add_field(name=title,value=alt)
				response.set_image(url=img)
		await ctx.send(embed=response)
		
def setup(bot):
	bot.add_cog(xkcdCog(bot))
		