import json
import random

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument

import libs.config as config
from cogs.rules import send_rules

####################
# Config variables #
####################

c_token_file = config.get_config("token_file")
c_prefix = config.get_config("prefix")

c_extensions = config.get_config("cogs")
c_disabled_extensions = config.get_config("disabled_cogs")


####################
# String variables #
####################

# Loads the bot's activity status
s_status = config.get_string("status")

# Token and prefix.

token = open(c_token_file).readline()
bot = commands.Bot(command_prefix=c_prefix)


# Loading the cogs.
if __name__ == "__main__":
    # Removes default help command.
    bot.remove_command("help")

    # Logging the unlodead cogs.
    if len(c_disabled_extensions) != 0:
        print("\nFollowing cogs are disabled:")
        for extension in c_disabled_extensions:
            print(f"[Disabled]\t{extension} has been disabled.")

    # Logging the loaded cogs.
    if len(c_extensions) != 0:
        print("\nLoading the COGS:")
        for extension in c_extensions:
            try:
                bot.load_extension(extension)
                print(f"[Success]\t{extension} loaded successfully.")
            except Exception as e:
                print(f"[ERROR]\tAn error occurred while loading {extension}\n" + str(e) + "\n")


# Logging the starting of the bot into the console.
@bot.event
async def on_ready():
    # Sets activity message.
    if s_status != "":
        await bot.change_presence(activity=discord.Game(s_status))

    # Removes default help command.
    print("\n#- Logged in as {0.user}".format(bot)+"\n")


# Removes the "command not found" error from the console.
@bot.event
async def on_command_error(ctx, error):
    error_to_skip = [CommandNotFound, MissingRequiredArgument]

    for error_type in error_to_skip:
        if isinstance(error, error_type):
            return

    raise error

# Starting the bot.
bot.run(token)
