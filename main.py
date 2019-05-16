# TryHackMe Discord Bot
# Created by DarkStar7471 aka J0n
import discord
from discord.ext import commands

inputFile = "token.txt"
workingFile = open(inputFile)
TOKEN = workingFile.readline()

prefix = "!"
bot = commands.Bot(command_prefix=prefix)
extensions = ["cogs.room", "cogs.social"]
if __name__ == "__main__":
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))


@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(521382216304033794)
    await channel.send(
        f"<@{member.id}> welcome to the server! Be sure to review the !rules and if you have any questions fire way in #support"
    )


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


bot.run(TOKEN)
