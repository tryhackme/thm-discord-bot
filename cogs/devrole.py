import discord
import aiohttp
import asyncio
import json
from discord.utils import get
from discord.ext import commands
from discord import guild
from discord.channel import DMChannel

# This config will soon be into a JSON file.
devLeadID = 578349526574694421
devID = 578056412790390785

# Role managment
def hasRole(member, id):
        for role in member.roles:
                if id == role.id:
                        return True
        return False

# Actual command
class DevRole(commands.Cog,name="BOT Dev"):
        def __init__(self,bot):
                self.bot = bot

        @commands.command()
        async def botdev(self, ctx, member):

                devLeadRole = ctx.guild.get_role(devLeadID)
                devRole = ctx.guild.get_role(devID)

                if(hasRole(ctx.author, devLeadRole)):
                        await member.add_roles(member, devRole)
                        await ctx.send("Welcome on the BOT Dev team, " + member.mention + "!")
            

def setup(bot):
        bot.add_cog(DevRole(bot))
