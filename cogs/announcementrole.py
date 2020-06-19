import discord
from discord import guild
from discord.ext import commands
from discord.utils import get

import libs.config as config
from libs.utils import has_role as has_role

####################
# Config variables #
####################

id_announcerole = config.get_config("roles")["announcementrole"]


####################
# String variables #
####################

s_announcementrole = config.get_string("announcementrole")


############
# COG Body #
############

class AnnouncementRole(commands.Cog, name="Announcements"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="notifyme", description=s_announcementrole["help_desc"])
    async def role_announce(self, ctx):
        announceRole = ctx.guild.get_role(id_announcerole)
            
        user = ctx.author

        # Then toggles the role for the target user.
        if not has_role(user, id_announcerole):
            await user.add_roles(announceRole)
            await ctx.send(s_announcementrole["on"].format(user.mention))
        else:
            await user.remove_roles(announceRole)
            await ctx.send(s_announcementrole["off"].format(user.mention))


def setup(bot):
    bot.add_cog(AnnouncementRole(bot))
