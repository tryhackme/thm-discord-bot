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
            response = discord.Embed(title="!rules", color=0xffff00)
            response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
            response.set_thumbnail(url="https://tryhackme.com/img/THMlogo.png")

            
            response.add_field(name="1.", value="No unsolicited direct messages (DMs) to other members of the discord. This includes staff. Verify that the member you are messaging is ok with you sending them DMs.")
            response.add_field(name="2.", value="No personal drama or drama from any other discord community is allowed to be brought into this discord. This is a space for infosec discussions and learning, keep it that way.")
            response.add_field(name="3.", value="No excessive self promotion. Linking to another discord server is strictly prohibited, just don't turn it into advertising.")
            response.add_field(name="4.", value="Keep it civil. If action is necessary in a dispute or any other sort of disruption on this discord punishment will be doled out evenly both to the individual(s) who started the issue and to those who reacted inappropriately in their response.")
            response.add_field(name="5.", value="No cheating is allowed whatsoever within this discord. Any cheating (other than specifically within a developmental environment where it has been preapproved by staff) will result in an immediate and permanent ban.")
            response.add_field(name="6.", value="Racism is not tolerated and will result in a permanent ban.")
            response.add_field(name="7.", value="Administrators reserve the right to modify the rules at any time and extend them accordingly to cover infractions which may not be currently included in these rules.")
            response.set_footer(text="From the TryHackMe Official API!")
            await ctx.send(embed=response)

def setup(bot):
        bot.add_cog(Rules(bot))
