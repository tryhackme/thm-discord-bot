import asyncio
import json
import time

import aiohttp
import discord
from discord.ext import commands

import libs.config as config
from libs.embedmaker import officialEmbed
from libs.utils import api_fetch


####################
# Config variables #
####################

c_api_stats = config.get_config("url")["api"]["stats"]
c_channels = config.get_config("channels")
c_milestone_offset = config.get_config("milestone_offset")
c_milestone_picture = config.get_config("images")["milestone"]
c_sleep_time = config.get_config("sleep_time")["stats_listener"]
c_stats_data = config.get_config("data_files")["stats"]


#####################
# Strings variables #
#####################

s_stats = config.get_string("stats")


###################
# Other variables #
###################

# Channels ID.
user_count_chann = c_channels["stats_users"]
room_count_chann = c_channels["stats_rooms"]
announcement_chann = c_channels["announcements"]


#############
# Functions #
#############

def round_number(x, base):
    """Rounds a number."""

    return base * round(x/base)

# Fetching data from the API.
async def fetch_stats():
    """Retrives the stats from THM API."""

    data = await api_fetch(c_api_stats)
    return data

# Saving JSON to local file.
def save_json(data):
    """Saves the data into the JSON file."""

    with open(c_stats_data, "w") as file:
        json.dump(data, file)

# Sending announcement function.
async def send_milestone(channel, milestone):
    """Announces a new milestone."""

    # Set up embed.
    embed = officialEmbed(s_stats["title"], s_stats["desc"].format(str(milestone)))
    embed.set_image(url=c_milestone_picture)

    # Send messages.
    await channel.send(embed=embed)


############
# COG Body #
############

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Updates the stats tracking channels with the given data.
    async def update_stat_channels(self, data):
        """Updates the numbers in the channels used to display stats."""

        userChann = self.bot.get_channel(user_count_chann)
        roomChann = self.bot.get_channel(room_count_chann)

        await userChann.edit(name="Users: "+str(data["totalUsers"]))
        await roomChann.edit(name="Rooms: "+str(data["publicRooms"]))

    # Checks if a new user milestone has been reached and sends an announcement.
    async def check_user_milestone(self, data):
        """Checks if a new registered user milestone has been reached."""

        # If there is no file (or it's corrupted), make (a new) one.
        try:
            raw_data = open(c_stats_data, "r").read()
            stored_data = json.loads(raw_data)

            new_milestone = stored_data["totalUsers"] + c_milestone_offset

            if data["totalUsers"] >= new_milestone:
                channel = self.bot.get_channel(announcement_chann)

                save_json(data)

                await send_milestone(channel, round_number(new_milestone, c_milestone_offset))
        except:
            raw_data = await fetch_stats()
            save_json(raw_data)

    async def listener(self):
        """Listener for the stats."""

        # We retrieve data from the API.
        data = await fetch_stats()

        # Compares the localy saved data to the one just fetched for a milestone.
        await self.check_user_milestone(data)

        # Updates the live stats.
        await self.update_stat_channels(data)


        await asyncio.sleep(c_sleep_time)
        await self.listener()


    # Starts the listener.
    @commands.Cog.listener()
    async def on_ready(self):
        await self.listener()

def setup(bot):
    bot.add_cog(Stats(bot))
