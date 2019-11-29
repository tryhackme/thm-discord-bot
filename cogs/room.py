from discord.ext import commands
import discord, random, time, asyncio, aiohttp, json
import ast

class Room(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def new_room(self):
        while True:
            channelJson = open("config/channels.json", "r").read()
            channelID = json.loads(channelJson)["announcements"]
            channel = self.bot.get_channel(channelID)

            roomJson = open("config/storage.json", "r").read()
            stored_data = json.loads(roomJson)

            async with aiohttp.ClientSession() as session:
                async with session.get("https://tryhackme.com/api/newrooms") as new_data:

                    text = await new_data.read()
                    json_data = json.loads(text)

                    # check for new data
                    if json_data[0]["title"] != stored_data[0]["title"]:
                       
                        # set up embed
                        img = json_data[0]["image"]
                        title = json_data[0]["title"]
                        code = "http://tryhackme.com/room/" + json_data[0]["code"]
                        description = json_data[0]["description"]

                        embed = discord.Embed(title=title, description=description, url=code)
                        embed.set_image(url=img)
                        embed.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
                        embed.set_footer(text="From the TryHackMe Official API!")

                        await channel.send("A new room is available!  |  Check it out: https://tryhackme.com/room/"+code)
                        await channel.send(embed=embed)

                        with open("config/storage.json", "w") as file:
                            json.dump(json_data, file)
                            #file.write(str(json_data))
                            #file.close()
                            
            await asyncio.sleep(60)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.new_room()


def setup(bot):
    bot.add_cog(Room(bot))



