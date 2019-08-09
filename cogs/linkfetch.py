import discord
import asyncio

from discord.ext import commands

class Linkfetch(commands.Cog,name="Blog commands"):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def blog(self, ctx):
        response = discord.Embed(color=0x0463C4)
        response.add_field(name="TryHackMe's Blog Link", value="https://blog.tryhackme.com/")
        response.set_thumbnail(url="https://blog.tryhackme.com/content/images/size/w1000/2019/07/THMlogo-2.png")
        await ctx.send(embed=response)

    @commands.command()
    async def github(self, ctx): 
        response = discord.Embed(color=0x0463C4)
        response.add_field(name="Bot's Github Repository Link",value="https://github.com/DarkStar7471/THM-Bot")
        response.set_footer(text="Bot's Github Link",icon_url="https://raw.githubusercontent.com/DarkStar7471/THM-Bot/master/images/computer.png")
        await ctx.send(embed=response)

def setup(bot):
    bot.add_cog(Linkfetch(bot))
