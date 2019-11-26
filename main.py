import discord
from discord.ext import commands
import time
import datetime

import random


# Reading the token.
inputFile = "token.txt"
workingFile = open(inputFile)
token = workingFile.readline()

# Setting up the bot and prefix.
prefix = "!"
bot = commands.Bot(command_prefix=prefix)

# Saving the starting time.
start_time = time.time()

# Setting up extentions. (cogs)
extensions = ["cogs.room", "cogs.social", "cogs.rank","cogs.userrank","cogs.rolesync","cogs.rules","cogs.wiki","cogs.linkfetch","cogs.xkcd", "cogs.fun", "cogs.devrole"]

# Quotes for the welcoming messages.
quotes = [
    "C4n y0u pwn th4 m4chin3?",
    "Hacker man 0x1 0x0 0x1",
    "The quieter you become the more you are able to hear",
    "\*Morpheus\*: Red or Blue pill?",
    "Access security... Access security grid... YOU DIDN'T SAY THE MAGIC WORD!",
    "Just hack the mainframe.",
    "Z2VsdW5weHpyLnBieg==",
    "The Matrix is real",
    "No place like 127.0.0.1",
    "Hack the planet",
    "Just obfuscate it...",
    "Armitage + Hail Mary",
    "WEP, WPA, WAH?",
    "admin:password",
    "rockyou.txt",
    "tmux > screens",
    "tabs or spaces?",
    "Leeerrrroy Jeekinnnns...",
    "Enumeration is key",
    "Try harder..",
    "https://discord.gg/zGdzUad",
    "Satoshi Nakamoto",
    "Mining Bitcoin...",
    "Configuring neural network"
    ]

def getMoto():
    return quotes[random.randint(0, len(quotes) - 1)]

# Loading the cogs.
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"{extension} loaded successfully.\n")
        except Exception as e:
            print(f"Error occurred while loading {extension}")

# Logging the starting of the bot into the console.
@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))


# Welcoming messages to new users.
@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(521382216304033794)
    quip = getMoto()
    response = discord.Embed(title="Welcome!", description=quip, color=0xa20606)
    response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
    response.set_thumbnail(url="https://cdn.discordapp.com/icons/521382216299839518/c0c7e9f1e258dd6d030fde8823bf8657.webp")
    response.add_field(name="Hey there!", value=f"<@{member.id}> , Welcome to the server!\n Be sure to review the !rules in #bot-commands. If you need help with a room, ask in #rooms-help.\n\n You can also sync your THM rank on the discord! Use !verify in #bot-commands for more information!")
    await channel.send(embed=response)


## Other commands.
# Uptime command.
@bot.command()
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    
    embed = discord.Embed(colour=0x3289a8)
    embed.add_field(name="Uptime", value=text)
    embed.set_footer(text="TryHackMe")

    await ctx.channel.send(embed=embed)

# Ping command.
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")
    ping = await ctx.send("**__Calculating Elapsed Time__**")
    await ping.edit(content="**Calculated:\nPing rate:** {}ms".format(round(bot.latency, 3)))


# Starting the bot.
bot.run(token)
