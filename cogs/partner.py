from discord.ext import commands
import discord, random, time, asyncio, aiohttp, json

class Partner(commands.Cog, name="Partner Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def partner(self, ctx):
        response = discord.Embed(color=0x660099)
        response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
        response.set_thumbnail(url="https://cdn.discordapp.com/icons/521382216299839518/c0c7e9f1e258dd6d030fde8823bf8657.webp")
        response.add_field(name="Name:", value="LOCKE", inline=True)
        response.add_field(name="Link:", value="https://discord.gg/9NedjUm", inline=True)
        await ctx.send(embed=response)

def setup(bot):
    bot.add_cog(Partner(bot))