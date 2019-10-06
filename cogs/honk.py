from discord.ext import commands
import discord

class Honk(commands.Cog, name="Honk Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def honk(self, ctx):
        response = discord.Embed(title="!honk", description="***HONK HONK HONK***", color=0xff4500)
        response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
        response.set_image(url="https://cdn.discordapp.com/attachments/433685563674198016/630100135623524363/JPEG_20191003_021216.jpg")
        await ctx.send(embed=response)

def setup(bot):
    bot.add_cog(Honk(bot))        