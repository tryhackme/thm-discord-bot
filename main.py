import discord
from discord.ext import commands
import time
import datetime

START_TIME = time.time()

inputFile = "token.txt"
workingFile = open(inputFile)
TOKEN = workingFile.readline()


prefix = "!"
bot = commands.Bot(command_prefix=prefix)

extensions = ["cogs.room", "cogs.social", "cogs.rank","cogs.userrank","cogs.rules","cogs.wiki","cogs.linkfetch","cogs.xkcd","cogs.partner", "cogs.fun"]

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"{extension} loaded successfully.\n")
        except Exception as e:
            print(f"Error occurred while loading {extension}")

@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))


@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(521382216304033794)
    await channel.send(
        f"<@{member.id}>Welcome to the server!\nBe sure to review the **!rules** and if you have any questions fire way in #support"
    )

@bot.command()
async def uptime(self, ctx):
    current_time = time.time()
    difference = int(round(current_time - START_TIME))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(colour=0x3289a8)
    embed.add_field(name="Uptime", value=text)
    embed.set_footer(text="TryHackMe")
    await self.bot.say("Current uptime: " + text)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")
    ping = await ctx.send("**__Calculating Elapsed Time__**")
    await ping.edit(content="**Calculated:\nPing rate:** {}ms".format(round(bot.latency, 3)))

bot.run(TOKEN)
