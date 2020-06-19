import discord
import libs.config as config
from discord.ext import commands

####################
# Config variables #
####################

s_help = config.get_string("help")


#############
# Functions #
#############

def get_msg(bot, isStaff):
    """Fabricates the output message by loading COGs and commands informations."""

    msg = "```markdown\n#####\tHELP\t#####\n{required args} | [optional args]\n"

    # Loops through cogs.
    for cog_name in bot.cogs:
        cog = f"\n> {cog_name}\n"

        # Command number.
        i = 0

        # Loops all commands in cog.
        commands = bot.get_cog(cog_name).get_commands()
        for command in commands:

            # User and command isn't hidden, or staff and command is hidden.
            if (not command.hidden and not isStaff) or (command.hidden and isStaff):
                i = i+1
                cog += command.name

                # Display only stuff that exists.
                if not command.usage == None:
                    cog += f" {command.usage}"
                if not command.description == "":
                    cog += f" | {command.description}"

                cog += "\n"

        # If all commands in cog are hidden, don't print its name.
        if i > 0:
            msg += cog

    msg += "```"
    return msg


############
# COG Body #
############

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="staff", description=s_help["staff_help"])
    async def help_staff(self, ctx):
        await ctx.send(get_msg(self.bot, True))

    @commands.command(name="help", description=s_help["user_help"])
    async def help_user(self, ctx):
        await ctx.send(get_msg(self.bot, False))


def setup(bot):
    bot.add_cog(Help(bot))
