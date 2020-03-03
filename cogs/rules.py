import discord
import aiohttp
import asyncio
import json
from discord.ext import commands

from libs.embedmaker import officialEmbed

class Rules(commands.Cog,name="Rules Commands"):
        def __init__(self,bot):
                self.bot = bot

        @commands.command(description="Sends the rules.")
        async def rules(self,ctx):
                # Make embed.
                response = officialEmbed("Rules", color=0xffff00)
                response.set_thumbnail(url="https://tryhackme.com/img/THMlogo.png")
                
                # Load the rules from config.
                rulesF = json.loads(open("config/rules.json", "r").read())
                rules = rulesF["rules"]
                i = 0

                # Add each rule.
                for rule in rules:
                        response.add_field(name=(str(i+1)+"."), value=rule)
                        i = i + 1
                
                # Send.
                await ctx.send(embed=response)

def setup(bot):
        bot.add_cog(Rules(bot))
