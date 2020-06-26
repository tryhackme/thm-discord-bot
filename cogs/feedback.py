import json

import discord
from discord.ext import commands

import libs.config as config
from libs.embedmaker import officialEmbed


############################
# Strings & Embed Features #
############################

# Feedback variable to retrieve strings from config.json
s_feedback = config.get_string("feedback")


# Use THM logo from config.json as embed picture
c_feedback_picture = config.get_config("info")["logo"]

# Use already defined site color from config.json as embed color
c_feedback_color = config.get_config("colors")["site"]


# Embed Title
s_feedback_title = s_feedback["title"]

# Embed URL
s_feedback_url = s_feedback["url"]

# Embed Field
s_feedback_message = s_feedback["message"]


#############
# Functions #
#############

# Setup the arguments for the embed to use the features gathered from config.json + create field.

def getEmbedFeedback(n, t, c):

    response = officialEmbed(n, color=c)
    response.set_thumbnail(url=t)
    response.add_field(name="Sharing your experience:", value=s_feedback_message + " " + s_feedback_url, inline=False)
    return response

############
# COG Body #
############

class Feedback(commands.Cog, name="Provide Feedback"):
    def __init__(self, bot):
        self.bot = bot

# Use help_desc from config.json for commmand description in !help
    @commands.command(name="feedback", description=s_feedback["help_desc"])
    async def feedback(self, ctx):
        response = getEmbedFeedback(s_feedback_title, c_feedback_picture, c_feedback_color)
        await ctx.send(embed=response)


def setup(bot):
    bot.add_cog(Feedback(bot))