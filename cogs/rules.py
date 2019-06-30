import discord
import aiohttp
import asyncio
import json
from discord.ext import commands

class Rules(commands.Cog,name="Rank Commands"):
        def __init__(self,bot):
                self.bot = bot

        @commands.command()
        async def rules(self,ctx):
            data = "1. More of a statement and less of a rule but you will never receive at everyone notifications from this discord. No one is allowed to use anything other than at specific people notifications.\n\n"
            data += "2. No personal drama or drama from any other discord community is allowed to be brought into this discord. This is a space for gaming and hanging out, keep it that way.\n\n"
            data += "3. No excessive self promotion. Linking to another discord you may own once is perfectly okay, just don't turn it into advertising.\n\n"
            data += "4. Keep it civil. If action is necessary in a dispute or any other sort of disruption on this discord punishment will be doled out evenly both to the individual(s) who started the issue and to those who reacted inappropriately in their response.\n\n"
            data += "5. No cheating is allowed whatsoever within this discord. Any cheating (other than specifically within a developmental environment where it has been preapproved by staff) will result in an immediate and permanent ban.\n\n"
            data += "6. Severe racism is not tolerated and will result in a permanent ban.\n\n"
            data += "7. Administrators reserve the right to modify the rules at any time and extend them accordingly to cover infractions which may not be currently included in these rules."
            await ctx.send("```{}```".format(data))

def setup(bot):
	bot.add_cog(Rules(bot)