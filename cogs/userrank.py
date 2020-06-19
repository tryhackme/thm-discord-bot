import asyncio
import json
import random

import aiohttp
import discord
import requests
from discord.ext import commands
from requests.exceptions import HTTPError

import libs.config as config
import libs.database as database
from libs.embedmaker import officialEmbed
from libs.utils import sanitize_check
from libs.utils import api_fetch


####################
# Config variables #
####################

c_api_rank = config.get_config("url")["api"]["user"]
c_api_token = config.get_config("url")["api"]["token"]
c_url_userprofile = config.get_config("url")["user_profile"]

#####################
# Strings variables #
#####################

s_userrank = config.get_string("ranks")["userrank"]
s_quotes = config.get_string("quotes")["regular_quotes"]

#############
# Functions #
#############

def get_moto():
    """Returns a random quote from the list."""

    return s_quotes[random.randint(0, len(s_quotes) - 1)]

# Getting infos.
def get_avatar(username):
    """Fetches the user's avatar."""

    response = requests.get(
        c_api_rank.format(username))
    data = response.text
    data = json.loads(data)
    return data['avatar']

def get_points(username):
    """Fetches the user's points."""

    response = requests.get(
        c_api_rank.format(username))
    data = response.text
    data = json.loads(data)
    return data['points']

def get_rank(username):
    """Fetches the user's rank."""

    response = requests.get(
        c_api_rank.format(username))
    data = response.text
    data = json.loads(data)
    return data['userRank']

def get_sub_status(username):
    """Fetches the user's sub status."""

    url = c_url_userprofile.format(username)
    check = "No!"
    try:
        response = requests.get(url)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        if "<span>Subscribed</span>" in response.text:
            check = "Yes!"
        else:
            check = "No!"
    return check


############
# COG Body #
############

class Userrank(commands.Cog, name="Rank Commands"):
    def __init__(self, bot):
        self.bot = bot

    async def send_rank(self, ctx, user):
        """Sends the message containing the user's rank."""

        try:
            if get_rank(user) != 0:
                quip = get_moto()
                quip = "*{}*".format(quip)

                userImg = get_avatar(user)
                Points = get_points(user)
                rank = get_rank(user)

                response = officialEmbed("Rank", quip, 0x148f77)

                response.set_thumbnail(url=userImg)
                response.add_field(
                    name="Username:", value=user, inline=True)
                response.add_field(name="Rank:", value=rank, inline=True)
                response.add_field(
                    name="Points:", value=Points, inline=True)

                sub = get_sub_status(user)

                response.add_field(name="Subscribed?",
                                    value=sub, inline=True)
            else:
                response = officialEmbed("Rank", s_userrank["user_not_found"], color=0xdc143c)

                userImg = config.get_config("info")["icon"]
                response.set_thumbnail(url=userImg)


            await ctx.send(embed=response)
        except:
            await ctx.send(s_userrank["error"])

    async def rank_from_id(self, ctx, id):
        """Retrieve a user's rank from his ID."""

        db = database.connect_to_db()
        request = database.get_user_by_discord_uid(db, id)

        if len(request) == 0:
            response = officialEmbed("Rank", s_userrank["user_not_found"], color=0xdc143c)

            userImg = config.get_config("info")["icon"]
            response.set_thumbnail(url=userImg)

            await ctx.send(embed=response)
        else:
            user_token = request[0][1]

            data = await api_fetch(c_api_token, user_token)
            user = data["username"]

            await self.send_rank(ctx, user)

    @commands.command(description=s_userrank["help_desc"], usage="[@mention/username]")
    async def rank(self, ctx, user=None):
        is_id = False

        # Empty arg, so we retrieve sender's id.
        if user == None:
            await self.rank_from_id(ctx, ctx.author.id)
            return

        # Contains a user.
        ## Is it a mention or THM username?
        ### Mentions.
        if "<@!" in user:
            is_id = True
            user = user[3:len(user)-1]
        elif "<@" in user:
            is_id = True
            user = user[2:len(user)-1]

        # THM Username.
        if sanitize_check(user) == False:
            await ctx.send(config.get_string("not_sanitized"))
            return
        
        if is_id:
            await self.rank_from_id(ctx, user)
        else:
            await self.send_rank(ctx, user)


def setup(bot):
    bot.add_cog(Userrank(bot))
