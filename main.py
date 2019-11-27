import discord
from discord.ext import commands
import time
import datetime
import json
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
quotesF = json.loads(open("config/quotes.json", "r").read())
channelsF = json.loads(open("config/channels.json", "r").read())

specialQuotes = quotesF["specialQuotes"]
regularQuotes = quotesF["regularQuotes"]
welcomeChanID = channelsF["welcome"]


def getMoto():
    #About 10% chance to have a special quote.
    isSpecial = random.randint(0,100)

    if isSpecial <= 10:
        return specialQuotes[random.randint(0, len(specialQuotes)-1)]
    else:
        return regularQuotes[random.randint(0, len(regularQuotes) - 1)]

async def send_rules(member):
    response = discord.Embed(title="!rules", color=0xffff00)
    response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
    response.set_thumbnail(url="https://tryhackme.com/img/THMlogo.png")
            
    response.add_field(name="1.", value="No unsolicited direct messages (DMs) to other members of the discord. This includes staff. Verify that the member you are messaging is ok with you sending them DMs.")
    response.add_field(name="2.", value="No personal drama or drama from any other discord community is allowed to be brought into this discord. This is a space for infosec discussions and learning, keep it that way.")
    response.add_field(name="3.", value="No excessive self promotion. Linking to another discord server is strictly prohibited, just don't turn it into advertising.")
    response.add_field(name="4.", value="Keep it civil. If action is necessary in a dispute or any other sort of disruption on this discord punishment will be doled out evenly both to the individual(s) who started the issue and to those who reacted inappropriately in their response.")
    response.add_field(name="5.", value="No cheating is allowed whatsoever within this discord. Any cheating (other than specifically within a developmental environment where it has been preapproved by staff) will result in an immediate and permanent ban.")
    response.add_field(name="6.", value="Racism is not tolerated and will result in a permanent ban.")
    response.add_field(name="7.", value="Administrators reserve the right to modify the rules at any time and extend them accordingly to cover infractions which may not be currently included in these rules.")
    response.set_footer(text="From the TryHackMe Official API!")
    
    channel = await member.create_dm()
    await channel.send(embed=response)

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
    channel = bot.get_channel(welcomeChanID)

    quip = getMoto()
    response = discord.Embed(title="Welcome!", description=quip, color=0xa20606)
    response.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
    response.set_thumbnail(url="https://cdn.discordapp.com/icons/521382216299839518/c0c7e9f1e258dd6d030fde8823bf8657.webp")
    response.add_field(name="Hey there!", value=member.mention + ", Welcome to the server!\nIf you need help with a room, ask in #rooms-help.\n\n You can also sync your THM rank on the discord! Use !verify in #bot-commands for more information!")

    await send_rules(member)
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
