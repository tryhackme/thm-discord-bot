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


####################
# Config variables #
####################

c_api_leaderboard = config.get_config("url")["api"]["leaderboard"]
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

pages = {1: 5, 2: 10, 3: 15, 4: 20, 5: 25, 6: 30, 7: 35, 8: 40, 9: 45, 10: 50}


#############
# Functions #
#############

def getUsernames(page, style):
    response = requests.get(c_api_leaderboard)
    data = response.text
    data = json.loads(data)[style]
    num = pages[page]-5
    r_num = num+1
    usernames = []
    for e, i in enumerate(data[num:pages[page]]):
        usernames.append(i["username"])
    return usernames

def getAvatars(page, style):
    response = requests.get(c_api_leaderboard)
    data = response.text
    data = json.loads(data)[style]
    num = pages[page]-5
    r_num = num+1
    avatars = []
    for e, i in enumerate(data[num:pages[page]]):
        avatars.append(i["avatar"])
    return avatars

def getPoints(page, style):
    response = requests.get(c_api_leaderboard)
    data = response.text
    data = json.loads(data)[style]
    num = pages[page]-5
    r_num = num+1
    points = []
    pointsType = 0
    if style == "topUsersMonthly":
        pointsType = "monthlyPoints"
    else:
        pointsType = "points"
    for e, i in enumerate(data[num:pages[page]]):
        points.append(i[pointsType])
    return points


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

        # Retrieving the users, points and avatar.
        avatars = getAvatars(page, "topUsers")
        usernames = getUsernames(page, "topUsers")
        points = getPoints(page, "topUsers")

        base = 150
        index = 0
        pos = (8, base)
        edge = 975

        # Adding each user.
        for x in usernames:
            response = requests.get(avatars[index])

            # Saving temp image, then adding it to the rest.
            temp_img = Image.open(BytesIO(response.content))
            temp_img.save('images/temp{}.png'.format(index))
            output = ImageOps.fit(temp_img, mask.size, centering=(0.5, 0.5))
            img.paste(output, (83, base), mask)

            # Adding the texts.
            d.text((222, base+32),
                   "{}".format(usernames[index]), font=font2, fill=white)
            d.text((8, base+32), "{}.".format(index+1 +
                                              (page-1)*5), font=font2, fill=white)

            d.text((970-(len(str(points[index]))*25), base+32),
                   str(points[index]), font=font2, fill=green)
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

        # Retrieving the users, points and avatar.
        avatars = getAvatars(page, "topUsersMonthly")
        usernames = getUsernames(page, "topUsersMonthly")
        points = getPoints(page, "topUsersMonthly")

        base = 150
        index = 0
        pos = (8, base)
        edge = 975

        # Adding each user.
        for x in usernames:
            response = requests.get(avatars[index])

            # Saving temp image, then adding it to the rest.
            temp_img = Image.open(BytesIO(response.content))
            temp_img.save('images/temp{}.png'.format(index))
            output = ImageOps.fit(temp_img, mask.size, centering=(0.5, 0.5))
            img.paste(output, (83, base), mask)

            # Adding the texts.
            d.text((222, base+32),
                   "{}".format(usernames[index]), font=font2, fill=white)
            d.text((8, base+32), "{}.".format(index+1 +
                                              (page-1)*5), font=font2, fill=white)

            d.text((970-(len(str(points[index]))*25), base+32),
                   str(points[index]), font=font2, fill=green)
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

    @commands.command(description=s_leader["help_desc"])
    async def leaderboard(self, ctx, *, page: int = 1):
        # Adds a white flag reaction to the user's command.
        emoji = "\N{Waving White Flag}"
        await ctx.message.add_reaction(emoji)

        await self.global_leaderboard(ctx.channel, page)

    @commands.command(description=s_monthly["help_desc"])
    async def monthly(self, ctx, *, page: int = 1):
        # Adds a white flag reaction to the user's command.
        emoji = "\N{Waving White Flag}"
        await ctx.message.add_reaction(emoji)

        await self.monthly_leaderboard(ctx.channel, page)

    # Starts the montly leaderboard announcement.
    @commands.Cog.listener()
    async def on_ready(self):
        self.chan_announcement = self.bot.get_channel(id_announcement)
        await self.monthly_announcement()


def setup(bot):
    bot.add_cog(Rank(bot))
