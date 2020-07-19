import json

import discord
from discord.ext import commands

import libs.config as config
from libs.embedmaker import officialEmbed
from libs.utils import sanitize_check

####################
# Config variables #
####################

c_file_gtfobins = config.get_config("data_files")["gtfobins"]


####################
# String variables #
####################

s_not_sanitized = config.get_string("commands")["not_sanitized"]
s_gfto = config.get_string("gtfobins")


############
# COG Body #
############

class Gtfobins(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description=s_gfto["help_desc"], usage="[query]")
    async def gtfobins(self, ctx, search_term=""):
        if sanitize_check(search_term) == False:
            await ctx.send(s_not_sanitized)

        gtfobins_file = json.loads(open(c_file_gtfobins, "r").read())

        # If user is searching for something.
        if search_term != "":
            try:
                # Getting data.
                data = gtfobins_file[search_term]
                result = "".join(["- " + item[1:-1] + "\n" for item in data])

                # Generating the embed.
                response = officialEmbed(s_gfto["result_title"].format(search_term), color=0xcc0000)
    
                response.set_thumbnail(url=s_gfto["logo"])
                response.add_field(name=s_gfto["search_terms"], value=search_term)
                response.add_field(name=s_gfto["vulnerability"], value=result)
                response.add_field(name=s_gfto["url"], value="https://gtfobins.github.io/gtfobins/"+search_term)

                await ctx.send(embed=response)
            except Exception as e:
                await ctx.send(s_gfto["not_found"].format(search_term))
        
        # Otherwise display a list of possibilities.
        else:
            try:
                result = ""
                for key, value in gtfobins_file.items():
                    result += "- " + key
                    result += "\n"

                response = discord.Embed(title=s_gfto["binaries"], color=0xcc0000)
                response.set_thumbnail(url=s_gfto["logo"])
                response.add_field(name=s_gfto["binaries_list"], value=result)
                response.add_field(name="How to?", value=s_gfto["howto"])

                await ctx.send(s_gfto["sending_list"])
                await ctx.send(embed=response)
            except Exception as e:
                await ctx.send(s_gfto["error"])


def setup(bot):
    bot.add_cog(Gtfobins(bot))
