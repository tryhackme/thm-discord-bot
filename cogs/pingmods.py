from datetime import datetime

import discord
from discord import guild
from discord.ext import commands

from datetime import datetime

import libs.command_manager as command_manager
from libs.command_manager import check

import libs.config as config
from libs.embedmaker import officialEmbed


# Look for staff_lounge channel ID
id_staff_lounge = config.get_config("channels")["staff_lounge"]

# Look for Mod role ID from config
id_mod = config.get_config("roles")["mod"]

# Load stored strings
s_pingmods = config.get_string("ping_mods")

class PingMods(commands.Cog, name="Ping Mods"):
    def __init__(self, bot):
        self.bot = bot
    
    # Checks to see if the user is a Mentor and if so, will only send in #staff_lounge
    @commands.command(name="pingmods", description=s_pingmods["help_desc"], usage="!pingmods 'reason'", hidden=True)
    @check(roles="mentor",
        channels="staff_lounge",
        dm_flag=False)
    

    async def ping_mods(self, ctx, reason=""):
        # Sanitise input in "reason" field
        if command_manager.is_sanitized(reason):

            # Contextualise Moderator role for ctx
            modRole = ctx.guild.get_role(id_mod)

            # Setup embed util
            embed = officialEmbed("Pinging Moderators:")

            # If no reason is provided, command will error and won't ping
            if reason == "":
                await ctx.send(s_pingmods["no_reason"])

            # Otherwise, assume any input is a valid reason
            else:
                # Setup embed fields
                timestamp = datetime.now()
                embed.add_field(name="Mentor:", value="{}".format(ctx.author), inline=False)
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.add_field(name="Timestamp:", value=timestamp, inline=False)

                # Send Embed w/ provided values
                await ctx.send(embed=embed)

                # I cannot for the life of me get any role to ping in the embed
                # So at the moment two messages are sent:
                # First the embed, then a seperate message containing the actual ping to Mods

                await ctx.send(modRole.mention)

        # If input is banned, command won't fire
        else:
            await command_manager.error_response(ctx, "not_sanitized")           

def setup(bot):
    bot.add_cog(PingMods(bot))