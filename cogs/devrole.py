import discord
from discord import guild
from discord.channel import DMChannel
from discord.ext import commands
from discord.utils import get

import libs.config as config
from libs.utils import has_role as has_role

####################
# Config variables #
####################

# Role IDs.
id_devLead = config.get_config("roles")["devLead"]
id_dev = config.get_config("roles")["dev"]


####################
# String variables #
####################

s_no_perm = config.get_string("commands")["no_perm"]
s_devrole = config.get_string("devrole")


############
# COG Body #
############

class DevRole(commands.Cog, name="BOT Dev"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="botdev", description=s_devrole["help_desc"] + " (Bot-dev Lead)", usage="{@member}", hidden=True)
    async def role_botdev(self, ctx, member: discord.Member):
        devRole = ctx.guild.get_role(id_dev)

        # Check if the user has the requiered role to issue the command. (DEV LEAD)
        if has_role(ctx.author, id_devLead):
            
            # Then toggles the role for the target user.
            if not has_role(member, id_dev):
                await member.add_roles(devRole)
                await ctx.send(s_devrole["welcome"].format(member.mention))
            else:
                await member.remove_roles(devRole)
                await ctx.send(s_devrole["leave"].format(member.mention))
        else:
            await ctx.send(s_no_perm)


def setup(bot):
    bot.add_cog(DevRole(bot))
