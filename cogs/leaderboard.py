import asyncio
import datetime
import io
import json
import random
from io import BytesIO

import discord
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps

import libs.config as config
from libs.thm_api import get_leaderboard_data


####################
# Config variables #
####################

c_monthly_data = config.get_config("data_files")["monthly_leaderboard"]
c_channels = config.get_config("channels")


#####################
# Strings variables #
#####################

s_leader = config.get_string("ranks")["leaderboard"]
s_monthly = config.get_string("ranks")["monthly"]


###################
# Other variables #
###################

# Channels ID.
id_announcement = c_channels["announcements"]

# Fonts and color.
font1 = ImageFont.truetype("fonts/Ubuntu-Light.ttf", 75)
font2 = ImageFont.truetype("fonts/Ubuntu-Light.ttf", 50)
font3 = ImageFont.truetype("fonts/Ubuntu-Bold.ttf", 30)
red = (162, 6, 6)
gray = (52, 60, 66)
green = (136, 204, 20)
white = (255, 255, 255)


############
# COG Body #
############

class Rank(commands.Cog, name="Leaderboard Commands"):
    def __init__(self, bot):
        self.bot = bot

    async def global_leaderboard(self, channel, page: int = 1):
        """Generates and sends the global leaderboard."""

        print("Generating global leaderboard...\n")

        # New image.
        img = Image.new('RGB', (1000, 1000), color=gray)

        # Adding logo.
        logo = Image.open("images/THMlogo.png")
        logo.thumbnail((logo.size[0]/4, logo.size[1]/4), Image.ANTIALIAS)
        img.paste(logo, (775, 15), logo)
        d = ImageDraw.Draw(img)

        # Adding texts. (leaderboard, mady with, invite link..)
        d.text((12, 20), "Leaderboard:", font=font1, fill=white)
        d.text((865-len(str(page))*25, 920),
               "Page {}".format(page), font=font2, fill=white)
        d.text((12, 925), s_leader["footer"],
               font=font3, fill=white)
        d.text((12, 955), config.get_config("url")["invite"], font=font3, fill=white)

        # Masking for the users.
        size = (128, 128)
        mask = Image.new("L", size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0) + size, fill=255)

        # Retrieving the global leaderboard data.
        leaderboard_data = get_leaderboard_data(page)

        base = 150
        index = 0
        pos = (8, base)
        edge = 975

        # Adding each user.
        for user in leaderboard_data:
            response = requests.get(user['avatar'])

            # Saving temp image, then adding it to the rest.
            temp_img = Image.open(BytesIO(response.content))
            temp_img.save('images/temp{}.png'.format(index))
            output = ImageOps.fit(temp_img, mask.size, centering=(0.5, 0.5))
            img.paste(output, (83, base), mask)

            # Adding the texts.
            d.text((222, base+32),
                   "{}".format(user['username']), font=font2, fill=white)
            d.text((8, base+32), "{}.".format(index+1 +
                                              (page-1)*5), font=font2, fill=white)

            d.text((970-(len(str(user['points']))*25), base+32),
                   str(user['points']), font=font2, fill=green)
            base += 160
            pos = (8, base)
            index += 1

        # Finalizing, and sending.
        large_img = img.resize((img.size[0]*4, img.size[1]*4))
        large_img.save('images/leaderboard_output.png')
        await channel.send(file=discord.File('images/leaderboard_output.png'))

    async def monthly_leaderboard(self, channel, page: int = 1):
        """Generates and sends the monthly leaderboard."""

        print("Generating monthly leaderboard...\n")

        # New image.
        img = Image.new('RGB', (1000, 1000), color=gray)

        # Adding logo.
        logo = Image.open("images/THMlogo.png")
        logo.thumbnail((logo.size[0]/4, logo.size[1]/4), Image.ANTIALIAS)
        img.paste(logo, (775, 15), logo)
        d = ImageDraw.Draw(img)

        # Adding texts. (leaderboard, mady with, invite link..)
        d.text((12, 20), "Monthly Leaderboard:", font=font1, fill=white)
        d.text((865-len(str(page))*25, 920),
               "Page {}".format(page), font=font2, fill=white)
        d.text((12, 925), s_monthly["footer"],
               font=font3, fill=white)
        d.text((12, 955), config.get_config("url")["invite"], font=font3, fill=white)

        # Masking for the users.
        size = (128, 128)
        mask = Image.new("L", size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0) + size, fill=255)

        # Retrieving the monthly leaderboard data.
        leaderboard_data = get_leaderboard_data(page, monthly=True)

        base = 150
        index = 0
        pos = (8, base)
        edge = 975

        # Adding each user.
        for user in leaderboard_data:
            response = requests.get(user['avatar'])

            # Saving temp image, then adding it to the rest.
            temp_img = Image.open(BytesIO(response.content))
            temp_img.save('images/temp{}.png'.format(index))
            output = ImageOps.fit(temp_img, mask.size, centering=(0.5, 0.5))
            img.paste(output, (83, base), mask)

            # Adding the texts.
            d.text((222, base+32),
                   "{}".format(user['username']), font=font2, fill=white)
            d.text((8, base+32), "{}.".format(index+1 +
                                              (page-1)*5), font=font2, fill=white)

            d.text((970-(len(str(user['monthlyPoints']))*25), base+32),
                   str(user['monthlyPoints']), font=font2, fill=green)
            base += 160
            pos = (8, base)
            index += 1

        # Finalizing, and sending.
        large_img = img.resize((img.size[0]*4, img.size[1]*4))
        large_img.save('images/leaderboard_output.png')
        await channel.send(file=discord.File('images/leaderboard_output.png'))

    async def monthly_announcement(self):
        """Sends the monthly leaderboard in the announcement channel."""

        date = datetime.datetime.today()
        month = date.month
        
        # If file doesn't exists, creates it with current month.
        try:
            file = open(c_monthly_data, "r+")
            data = file.read()
        except:
            file = open(c_monthly_data, "w")
            data = month
            file.write(str(data))

        file.close()

        if int(data) != month:
            channel = self.chan_announcement

            await self.monthly_leaderboard(channel)
            file = open(c_monthly_data, "w")
            file.write(str(month))
            file.close()

        await asyncio.sleep(config.get_config("sleep_time")["monthly_leaderboard"])

    @commands.command(description=s_leader["help_desc"], usage="[page]")
    async def leaderboard(self, ctx, *, page: int = 1):

        # The bot will appear as typing while executing the command.
        async with ctx.channel.typing():
            await self.global_leaderboard(ctx.channel, page)

    @commands.command(description=s_monthly["help_desc"], usage="[page]")
    async def monthly(self, ctx, *, page: int = 1):

        # The bot will appear as typing while executing the command.
        async with ctx.channel.typing():
            await self.monthly_leaderboard(ctx.channel, page)

    # Starts the monthly leaderboard announcement.
    @commands.Cog.listener()
    async def on_ready(self):
        self.chan_announcement = self.bot.get_channel(id_announcement)
        await self.monthly_announcement()


def setup(bot):
    bot.add_cog(Rank(bot))
