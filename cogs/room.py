from discord.ext import commands
import discord, random, time, asyncio, requests, json


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def new_room(self):
        while True:
            channel = self.bot.get_channel(546650767495397376)
            json_file = open("storage.json", "r+")
            stored_data = json.load(json_file)
            new_data = requests.get("https://www.tryhackme.com/api/newrooms")
            text = new_data.text
            json_data = new_data.json()
            # check for new data
            if json_data[0]["title"] != stored_data[0]["title"]:
                # set up embed
                img = "https://tryhackme.com/" + json_data[0]["image"]
                title = json_data[0]["title"]
                code = "https://tryhackme.com/room/" + json_data[0]["code"]
                description = json_data[0]["description"]
                embed = discord.Embed(title=title, description=description, url=code)
                embed.set_image(url=img)
                await channel.send("NEW ROOM")
                await channel.send(embed=embed)
                with open("storage.json", "w") as file:
                    file.write(text)
            await asyncio.sleep(60)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.new_room()


def setup(bot):
    bot.add_cog(Test(bot))



