import datetime
import time

from discord.ext import commands

import libs.config as config
from libs.embedmaker import officialEmbed

####################
# Config variables #
####################

# Saving the starting time.
start_time = time.time()


#####################
# Strings variables #
#####################

s_ping = config.get_string("ping")


############
# COG Body #
############

class Core(commands.Cog, name="Core Commands"):
    def __init__(self, bot):
        self.bot = bot

        # Uptime command.
        @bot.command(description="Returns the uptime of the bot.")
        async def uptime(ctx):
            # Gets the time and substracts it to the current time.
            current_time = time.time()
            difference = int(round(current_time - start_time))
            text = str(datetime.timedelta(seconds=difference))

            # Embed.
            embed = officialEmbed(color=0x3289a8)
            embed.add_field(name="Uptime", value=text)

            # Sends.
            await ctx.channel.send(embed=embed)

        # Ping command.
        @bot.command(description="Sends a ping request to the bot.")
        async def ping(ctx):
            await ctx.send("Pong!")
            msg_ping = await ctx.send(s_ping["calculating"])

            # We round up the latency for a cleaner output.
            ping = round(bot.latency, 3)

            # Instead of sending a new msg, we edit the previous one.
            await msg_ping.edit(content=s_ping["calculated"].format(ping))


def setup(bot):
    bot.add_cog(Core(bot))
