import random

import discord
from discord.ext import commands

import libs.config as config
from cogs.rules import send_rules
from libs.embedmaker import officialEmbed


##############################
# Config & strings variables #
##############################

# Loads data from config.
quotes = config.get_string("quotes")
channels = config.get_config("channels")

# Strings.
s_welcome_msg = config.get_string("welcome")["welcome_message"]
s_specials_quotes = quotes["special_quotes"]
s_regulars_quotes = quotes["regular_quotes"]

#IDs.
id_welcome = channels["welcome"]


#############
# Functions #
#############

# Sends the !verify instructions.
async def send_verify(channel):
    """Sends the instructions on how to verify yourself."""

    # Embed making.
    response = officialEmbed("How to get verified?")
    response.set_thumbnail(url=config.get_config("info")["logo"])

    # Loading text from JSON.
    steps = config.get_string("faq")["verify"]
    i = 0

    # Add each step to the embed.
    for step in steps:
        response.add_field(name=("Step "+str(i+1)), value=step)
        i = i + 1

    # Sending the created embed in DM to the user.
    await channel.send(embed=response)

# Getting a random quote from the non-rare pool.
def get_regular_quote():
    """Returns a quote from the regular pool."""

    return s_regulars_quotes[random.randint(0, len(s_regulars_quotes) - 1)]

# Getting a random quote from the rare pool.
def get_special_quote():
    """Returns a quote from the special pool."""

    return s_specials_quotes[random.randint(0, len(s_specials_quotes)-1)]

# Rolling dices to know if we get a special quote.
def is_special_quote():
    """Calculate if the quote has to be special or not."""

    # About 10% chance to have a special quote.
    isSpecial = random.randint(0, 100)
    return isSpecial <= 10


############
# COG Body #
############

class Welcome(commands.Cog, name="Welcome Commands"):
    def __init__(self, bot):
        self.bot = bot

    # Welcoming messages to new users + DM rules and !verify instructions.
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Retrieve the channel to send the embed in.
        channel = self.bot.get_channel(id_welcome)

        # Roles the dice for a (non) special quote, then sends it.
        if is_special_quote():
            quip = get_special_quote()
            welcome_embed = officialEmbed(
                "Welcome!", quip, color=0xf5b400, footer="")
        else:
            quip = get_regular_quote()
            welcome_embed = officialEmbed(
                "Welcome!", quip, color=0xa20606, footer="")

        # Embed creation.
        welcome_embed.add_field(
            name="Hey there!", value=member.mention + s_welcome_msg)

        # Check if user exists. (avoids join-leavers etc.)
        if member is not None:
            # DM.
            dm_channel = await member.create_dm()
            await send_rules(dm_channel)
            await send_verify(dm_channel)

            # Welcome channel.
            await channel.send(embed=welcome_embed)


def setup(bot):
    bot.add_cog(Welcome(bot))
