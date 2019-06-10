from discord.ext import commands
import discord, random, time, asyncio, requests, json,tweepy

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
    @commands.command()
    async def tweet(self,ctx):
        #consumer key,consumer secret, api key, api secret
        creds = [cred.replace("\n","") for cred in open("creds.txt","r")]
        auth = tweepy.OAuthHandler(creds[0], creds[1])
        auth.set_access_token(creds[2], creds[3])
        api = tweepy.API(auth)
        tryhackme_tweets = api.user_timeline(screen_name = 'RealTryHackMe', count = 20, include_rts = False)
        for tweet in tryhackme_tweets:
            if not tweet.in_reply_to_screen_name:
                await ctx.send("https://twitter.com/RealTryHackMe/status/" + str(tweet.id))
                break

def setup(bot):
    bot.add_cog(Social(bot))
