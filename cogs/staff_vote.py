import discord
from discord import guild
from discord.ext import commands
from discord.utils import get

import libs.config as config
from libs.command_manager import roles, channels, command

####################
# Config variables #
####################

id_cm_voting = config.get_config("channels")["staff_voting_cm"]


####################
# String variables #
####################

s_staff_vote = config.get_string("staff_vote")


############
# COG Body #
############

class StaffVote(commands.Cog, name="Staff Vote"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clearcm", description=s_staff_vote["help_desc"], hidden=True)
    async def clear_cm(self, ctx):
        if not await command(ctx, roles=[roles.ADMIN, roles.MODLEAD], channels=[channels.STAFF_VOTING_CM]):
            return

        await ctx.channel.purge(limit=100)
        await ctx.send(s_staff_vote["cleared"])


def setup(bot):
    bot.add_cog(StaffVote(bot))