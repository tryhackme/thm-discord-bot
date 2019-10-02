from discord.ext import commands
import discord, random, time, asyncio, requests, json,tweepy

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("twitter")
    async def twitter(self, ctx):
        response = discord.Embed(color=0x08a0e9)
        response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
        response.set_thumbnail(url="https://i.imgur.com/rImenvh.png")
        response.add_field(name="TryHackMe's Twitter Account:", value="https://twitter.com/realtryhackme")
        await ctx.send(embed=response)

    @commands.command()
    async def reddit(self, ctx):
        response = discord.Embed(color=0xff4500)
        response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
        response.set_thumbnail(url="https://i.imgur.com/rgK8YTD.png")
        response.add_field(name="TryHackMe's Subreddit:", value="https://www.reddit.com/r/tryhackme/")
        await ctx.send(embed=response)

    @commands.command()
    async def website(self, ctx):
        response = discord.Embed(color=0x000000)
        response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
        response.set_thumbnail(url="https://tryhackme.com/img/THMlogo.png")
        response.add_field(name="TryHackMe:", value="https://tryhackme.com/")
        await ctx.send(embed=response)

    @commands.command()
    async def social(self, ctx):
        response = discord.Embed(color=0x08a0e9)
        response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
        response.set_thumbnail(url="https://i.imgur.com/rImenvh.png")
        response.add_field(name="TryHackMe's Twitter Account:", value="https://twitter.com/realtryhackme")
        await ctx.send(embed=response)
        response = discord.Embed(color=0xff4500)
        response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
        response.set_thumbnail(url="https://i.imgur.com/rgK8YTD.png")
        response.add_field(name="TryHackMe's Subreddit:", value="https://www.reddit.com/r/tryhackme/")
        await ctx.send(embed=response)
        response = discord.Embed(color=0x000000)
        response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
        response.set_thumbnail(url="https://tryhackme.com/img/THMlogo.png")
        response.add_field(name="TryHackMe:", value="https://tryhackme.com/")
        await ctx.send(embed=response)
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
