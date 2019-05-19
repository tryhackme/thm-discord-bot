from discord.ext import commands
import discord, random, time, asyncio, requests, json


class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("twitter")
    async def twitter(self, ctx):
        await ctx.send("https://twitter.com/realtryhackme")

    @commands.command()
    async def reddit(self, ctx):
        await ctx.send("https://www.reddit.com/r/tryhackme/")

    @commands.command()
    async def website(self, ctx):
        await ctx.send("https://www.tryhackme.com")

    @commands.command()
    async def social(self, ctx):
        await ctx.send(
            """
```
Twitter: https://twitter.com/realtryhackme
Reddit: https://www.reddit.com/r/tryhackme/
Website: https://www.tryhackme.com
```
"""
        )


def setup(bot):
    bot.add_cog(Social(bot))
