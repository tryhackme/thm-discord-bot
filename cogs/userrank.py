import discord
import aiohttp
import asyncio
import json
from discord.ext import commands

def sanitize_check(data):
    chars = ["/",";","-",">","<",":","`","'\""]
    if any((c in chars) for c in data):
        return True
    else:
        return False

class Userrank(commands.Cog,name="Rank Commands"):
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    async def rank(self,ctx,*,user):
        if sanitize_check(user) == True:
            await ctx.send("Sorry, the characters you have entered are blacklisted, instead of trying anything here, try some rooms.")
        else:
            try:
                url = "https://tryhackme.com/api/usersRank/{}".format(user)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as data:
                        data = await data.read()
                        data = json.loads(data)
                        if data.get('userRank') != 0:
                            response = discord.Embed(color=0x148f77)
                            response.add_field(name='{} Rank'.format(user),value="Username: {}\nRank: {}".format(user,data.get('userRank')))
                            response.set_footer(text="From TryHackMe Official API!",icon_url="https://tryhackme.com/img/THMlogo.png")
                        else:
                            response.add_field(text="**Username not found**")
                    await ctx.send(embed=response)
            except:
                await ctx.send("**An issue has occured.**")
        
def setup(bot):
	bot.add_cog(Userrank(bot))
