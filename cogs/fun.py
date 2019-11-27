from discord.ext import commands
import discord
import json
import random


class Fun(commands.Cog, name="Fun Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def skidy(self, ctx):
        response = discord.Embed(title=":slight_smile:", description="", color=0x225999)
        response.set_author(name="Skidy",icon_url="https://i.imgur.com/fSMnXPt.png")
        await ctx.send(embed=response)

    @commands.command()
    async def ashu(self, ctx):
        response = discord.Embed(title=":slight_smile:", description="", color=0x225999)
        response.set_author(name="Ashu",icon_url="https://i.imgur.com/ojiqdem.png")
        await ctx.send(embed=response)

    @commands.command()
    async def dark(self, ctx):
        darkF = json.loads(open("config/dark.json", "r").read())
        darkQuotes = darkF["quotes"]

        response = discord.Embed(title=darkQuotes[random.randint(0, len(darkQuotes)-1)], description="", color=0xff4500)
        response.set_author(name="DarkStar7471",icon_url="https://i.imgur.com/jZ908d1.png")
        await ctx.send(embed=response)


    @commands.command()
    async def honk(self, ctx):
        response = discord.Embed(title="!honk", description="***HONK HONK HONK***", color=0xff4500)
        response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
        response.set_image(url="https://cdn.discordapp.com/attachments/433685563674198016/630100135623524363/JPEG_20191003_021216.jpg")
        await ctx.send(embed=response)
    
    @commands.command()
    async def boop(self, ctx, member: discord.Member=None):
        if ctx.message.channel.name == "bot-commands":
                if member.name == "Asphodel": #Yume - Asphodel#8097
                    print("No boop")
                    desc = "<@{}>, you can't boop <@{}>!".format(ctx.author.id, member.id)
                    response = discord.Embed(title="!boop", description=desc, color=0xFFFFFF)
                    response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
                else:
                    print("Boop")
                    #user = "<@{}>".format(member)
                    desc = "<@{}> was booped by <@{}>!".format(member.id, ctx.author.id)
                    response = discord.Embed(title="!boop", description=desc, color=0xFFFFFF)
                    response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
                    response.set_image(url="http://giphygifs.s3.amazonaws.com/media/99LhY1qc6jG8w/giphy.gif")
                await ctx.send(embed=response)
        else:
            return

            


def setup(bot):
    bot.add_cog(Fun(bot))        