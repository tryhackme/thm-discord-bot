from discord.ext import commands
import discord
import json
import random
import aiohttp

from libs.embedmaker import officialEmbed


class Fun(commands.Cog, name="Fun Commands"):
    def __init__(self, bot):
        self.bot = bot


    ###################################
    ### Skidy, Ashu, Dark's quotes. ###
    ###################################

    @commands.command(description="Sends Skidy's emote.")
    async def skidy(self, ctx):
        response = officialEmbed(title=":slight_smile:", color=0x225999, author="Skidy", author_img="https://i.imgur.com/fSMnXPt.png", footer="")
        await ctx.send(embed=response)

    @commands.command(description="Send Ashu's emote.")
    async def ashu(self, ctx):
        response = officialEmbed(title=":slight_smile:", color=0x225999, author="Ashu", author_img="https://i.imgur.com/ojiqdem.png", footer="")
        await ctx.send(embed=response)

    @commands.command(description="Send a random Dark's quote.")
    async def dark(self, ctx):
        darkF = json.loads(open("config/dark.json", "r").read())
        darkQuotes = darkF["quotes"]
        quote = darkQuotes[random.randint(0, len(darkQuotes)-1)]

        response = officialEmbed(title=quote, color=0xff4500, author="DarkStar7471", author_img="https://i.imgur.com/jZ908d1.png", footer="")
        await ctx.send(embed=response)


    #####################
    ### HONK and BOOP ###
    #####################

    @commands.command(description="HOOONK!")
    async def honk(self, ctx):
        response = officialEmbed("!honk", "***HONK HONK HONK***", 0xff4500)
        response.set_image(url="https://cdn.discordapp.com/attachments/433685563674198016/630100135623524363/JPEG_20191003_021216.jpg")
        await ctx.send(embed=response)
    
    @commands.command(description="Boop someone!", usage="{@user}")
    async def boop(self, ctx, member: discord.Member=None):
        if ctx.message.channel.name == "bot-commands" and member is not None:
                if member.id == 572908911749890053: #Yume - Asphodel#8097 572908911749890053
                    desc = "<@{}>, you can't boop <@{}>!".format(ctx.author.id, member.id)
                    response = officialEmbed("!boop", desc, color=0xFFFFFF)
                else:
                    desc = "<@{}> was booped by <@{}>!".format(member.id, ctx.author.id)
                    response = officialEmbed("!boop", desc, color=0xFFFFFF)
                    response.set_image(url="http://giphygifs.s3.amazonaws.com/media/99LhY1qc6jG8w/giphy.gif")
                await ctx.send(embed=response)
        else:
            return


    ############
    ### XKCD ###
    ############

    @commands.command(description="Send a random XKCD comic.")
    async def xkcd(self,ctx):
        comic_no = random.randint(1,1900)
        url = f"http://xkcd.com/{comic_no}/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                new_data = await data.read()
                json_data = json.loads(new_data)
                img = json_data.get("img")
                title = json_data.get("title")
                alt = json_data.get("alt")

                response = officialEmbed(color=0xffb6b9, footer="From the XKCD Official API!")
                response.add_field(name=title,value=alt)
                response.set_image(url=img)
        await ctx.send(embed=response)
            


def setup(bot):
    bot.add_cog(Fun(bot))        