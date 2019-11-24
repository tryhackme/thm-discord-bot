import discord
import aiohttp
import asyncio
import json
from discord.utils import get
from discord.ext import commands
from discord import guild
from discord.channel import DMChannel

# This config will soon be into a JSON file.
# Guild ID
guildID = 521382216299839518
# Rank roles ID respectively from 0x1 to 0xD
rolesID = [638047504822173726, 638047659541790760, 638047662893039634, 638047665766137876, 638047668597162006, 638047670878863390, 638047673173409811, 638047675845181461, 638047678432804925, 638047682232975371, 638047685340954634, 638047689380069404, 638047691800313866]
# Subscriber role ID
subID = 538509395605061653


async def deleteCommand(ctx):
        await ctx.send("Updating roles for " + ctx.message.author.mention + "!")
        await ctx.bot.delete_message(ctx.message)

# Role managment
def hasRole(member, id):
        for role in member.roles:
                if id == role.id:
                        return True
        return False

async def removeLevelRoles(member):
        for rId in rolesID:
                if hasRole(member, rId):
                        await member.remove_roles(get(member.guild.roles, id=rId))

async def removeSubRole(member):
        await member.remove_roles(get(member.guild.roles, id=subID))

async def addRole(member, id):
        await member.add_roles(get(member.guild.roles, id=id))

# Actual command
class RoleSync(commands.Cog,name="Verifying/Role Assigning Commands"):
        def __init__(self,bot):
                self.bot = bot

        @commands.command()
        async def verify(self, ctx, userToken=None):

                # If not DM, clear the message so that the token isn't kept publicly.
                if not isinstance(ctx.channel, DMChannel):
                        await ctx.message.delete()
                        await ctx.send("Please send that command to the bot in a DM. This is to stop other people from using using your token :slight_smile:")
                        return

                # If no token sends message...
                if userToken == None:
                        await ctx.send("Usage: !verify <token>\nGet your token from https://tryhackme.com/profile.")
                        return
                # Otherwise, keeps going:
                else:
                        async with aiohttp.ClientSession() as session:
                                async with session.get("https://tryhackme.com/tokens/discord/" + userToken) as data:

                                        cmdResult = ""

                                        data = await data.read()
                                        success = json.loads(data)["success"]

                                        if success == False:
                                                cmdResult = "I'm sorry but I couldn't find the specified token!"
                                        else:
                                                server = self.bot.get_guild(guildID)
                                                if server == None:
                                                        await ctx.send("An unexpected error has occured. Please contact THM's BOT maintainers.\nERROR: Server not found.")
                                                        return

                                                user = ctx.message.author
                                                member = server.get_member(user.id)

                                                if user == None or member == None:
                                                        await ctx.send("An unexpected error has occured. Please contact THM's BOT maintainers.\nERROR: User not found.")
                                                        return

                                                level = json.loads(data)["level"]
                                                sub = json.loads(data)["subscribed"]

                                                # Checks for the users' rank.
                                                if hasRole(member, rolesID[level]):
                                                        cmdResult += "Your rank is already up-to-date!\n"
                                                else:
                                                        await removeLevelRoles(member)
                                                        await addRole(member, rolesID[level])
                                                        cmdResult += "Your rank has been updated!\n"

                                                # Checks for the users' sub status.
                                                if sub == 0:
                                                        if hasRole(member, subID):
                                                                await removeSubRole(member)
                                                                cmdResult += "You are not longer a subscriber!"
                                                else:
                                                        if not hasRole(member, subID):
                                                                await addRole(member, subID)
                                                                cmdResult += "You are now a subscriber, thanks!"
                                        
                                        await ctx.send(cmdResult)
            

def setup(bot):
        bot.add_cog(RoleSync(bot))
