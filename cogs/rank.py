import discord
import aiohttp
import asyncio
import json
from discord.ext import commands

class Rank(commands.Cog,name="Rank Commands"):
        def __init__(self,bot):
                self.bot = bot

        @commands.command()
        async def leaderboard(self,ctx,*,page: int=1):
                pages = {1:5,2:10,3:15,4:20,5:25,6:30,7:35,8:40,9:45,10:50}
                if page > 10 or not isinstance(page,int):
                        await ctx.send("**Error occured\nEither enter the page number less than 10 or check your argument(s).**")
                async with aiohttp.ClientSession() as session:
                        async with session.get("https://tryhackme.com/api/leaderboards") as data:
                                data = await data.read()
                                data = json.loads(data)["topUsers"]
                                num = pages[page]-5
                                r_num = num+1
                                users = ""
                                for e,i in enumerate(data[num:pages[page]]):
                                        users += "\nUsername: {}\n".format(i["username"])
                                        users += "Rank: {}\n".format(r_num)
                                        r_num += 1
                                        users += "="*10
                                response = discord.Embed(color=0x00FFFF)
                                response.add_field(name="LeaderBoard Of TryHackMe!",value=users)
                                response.set_footer(text="From TryHackMe Official API!",icon_url="https://tryhackme.com/img/THMlogo.png")
                                
                await ctx.send(embed=response)
            

def setup(bot):
	bot.add_cog(Rank(bot))
				

        