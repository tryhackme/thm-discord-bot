from discord.ext import commands
import discord

class Fun(commands.Cog, name="Fun Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def honk(self, ctx):
        response = discord.Embed(title="!honk", description="***HONK HONK HONK***", color=0xff4500)
        response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
        response.set_image(url="https://cdn.discordapp.com/attachments/433685563674198016/630100135623524363/JPEG_20191003_021216.jpg")
        await ctx.send(embed=response)
    
    @commands.command()
    async def boop(self, ctx, member: discord.Member=None):
        #print(member.name)
        #print(member.id)
        #print(ctx.message.channel.name)
        if ctx.message.channel.name == "bot-commands":
                if member.name == "Asphodel": #Yume - Asphodel#8097
                    print("No boop")
                    desc = "<@{}>, you can't boop <@{}>!".format(ctx.author.id, member.id)
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