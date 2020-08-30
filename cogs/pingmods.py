import discord
from datetime import datetime

import libs.command_manager as command_manager
from discord.ext import commands

import libs.config as config
from libs.embedmaker import officialEmbed

from libs.command_manager import check

id_staff_lounge = config.get_config("channels")["staff_lounge"]
id_mods = config.get_config("roles")["mod"]

#id_mentor = config.get_config("roles")["mentor"]
#id_mod = config.get_config("roles")["mod"]

s_pingmods = config.get_string("ping_mods")

class PingMods(commands.Cog, name="Ping Mods"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="pingmods", description=s_pingmods["help_desc"], usage="!pingmods <reason>", hidden=True)
    @check(roles="mentor",
        channels="staff_lounge",
        dm_flag=False)
    

    async def ping_mods(self, ctx, reason=""):
        if command_manager.is_sanitized(ctx):

            modRole = ctx.guild.get_role(id_mods)

            embed = officialEmbed("Pinging Mods")

            if reason == "":
                await ctx.send("Please provide a reason as to why you are pinging the Moderator team.")

            else:
                timestamp = datetime.now()
                embed.add_field(name="Mentor:", value="{}".format(ctx.author), inline=False)
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.add_field(name="Timestamp:", value=timestamp, inline=False)
              # embed.add_field(name="Pinging:", value="<@&{}>".format((modRole)))
                embed.set_footer(text="Pinging: {}".format(modRole.mention))    
          #  await channel.send(id_pingmods.format(s_pingmods), embed=embed)
                await ctx.send(embed=embed)
        else:
            await command_manager.error_response(ctx, "not_sanitized")           

def setup(bot):
    bot.add_cog(PingMods(bot))