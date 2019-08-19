import discord 
import asyncio 
import aiohttp
import json
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def wiki(self,ctx,*,search):
        try:
            api_url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles="+search
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as data:
                    data = await data.read()
                    data = json.loads(data)['query']['pages']
                    data = next(iter(data.values()))
                    title = data['title']
                    content = data['extract'].split(".")
                    response = discord.Embed(color=0xffffff)
                    response.add_field(name=title,value=''.join(content[:2]))
            await ctx.send(embed=response)
        except:
            await ctx.send("Some Error Occured!")

def setup(bot):
    bot.add_cog(Utility(bot))