import discord
from discord.ext import commands

inputFile = "token.txt"
workingFile = open(inputFile)
TOKEN = workingFile.readline()

prefix = "!"
bot = commands.Bot(command_prefix=prefix)

extensions = ["cogs.room", "cogs.social", "cogs.rank","cogs.userrank","cogs.rules"]
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
async def on_message(ctx):
    if "https://discord.gg/" in ctx.content:
        channel = ctx.channel
        await ctx.delete()
        await channel.send("{} has sent a invite link which is not permitted in this server as written on Rule No. 3".format(ctx.author.mention))

@bot.event
async def on_message(ctx):
    channel = ctx.channel
    bad_words = ["fuck","fucking","shit","bitch","asshole"]
    for i in bad_words:
        if i in (ctx.content).lower():
            await channel.send("**Language {}!**".format(ctx.author.mention))
            break

@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(521382216304033794)
    await channel.send(
        f"<@{member.id}> Welcome to the server!\nBe sure to review the !rules and if you have any questions fire way in #support"
    )


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)
