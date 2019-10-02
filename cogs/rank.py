import discord
import aiohttp
import asyncio
import json
from discord.ext import commands

import random

quotes = [
    "C4n y0u pwn th4 m4chin3?",
    "Hacker man 0x1 0x0 0x1",
    "The quieter you become the more you are able to hear",
    "\*Morpheus\*: Red or Blue pill?",
    "Access security... Access security grid... YOU DIDN'T SAY THE MAGIC WORD!",
    "Just hack the mainframe.",
    "Z2VsdW5weHpyLnBieg==",
    "The Matrix is real",
    "No place like 127.0.0.1",
    "Hack the planet",
    "Just obfuscate it...",
    "Armitage + Hail Mary",
    "WEP, WPA, WAH?",
    "admin:password",
    "rockyou.txt",
    "tmux > screens",
    "tabs or spaces?",
    "Leeerrrroy Jeekinnnns...",
    "Enumeration is key",
    "Try harder..",
    "https://discord.gg/zGdzUad",
    "Satoshi Nakamoto",
    "Mining Bitcoin...",
    "Configuring neural network"
    ]

def getMoto():
    return quotes[random.randint(0, len(quotes) - 1)]

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
                                quip = getMoto()
                                quip = "*{}*".format(quip)
                                response = discord.Embed(title="!leaderboard", description=quip, color=0x00FFFF)
                                response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
                                response.set_thumbnail(url="https://tryhackme.com/img/THMlogo.png")
                                for e,i in enumerate(data[num:pages[page]]):
                                        response.add_field(name="Rank:", value=r_num, inline=True)
                                        response.add_field(name="Username:", value=i["username"], inline=True)

                                        r_num += 1

                                response.set_footer(text="From the TryHackMe Official API!")
                                
                await ctx.send(embed=response)
            

def setup(bot):
	bot.add_cog(Rank(bot))
				

        