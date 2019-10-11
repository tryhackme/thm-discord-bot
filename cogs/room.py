from discord.ext import commands
import discord, random, time, asyncio, aiohttp, json
import ast

class Room(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def new_room(self):
        while True:
            channel = self.bot.get_channel(546650767495397376)
            json_file = open("storage.json", "r").read()
            stored_data = json.loads(ast.literal_eval(json_file))
            async with aiohttp.ClientSession() as session:
                async with session.get("https://tryhackme.com/api/newrooms") as new_data:
                    text = await new_data.read()
                    json_data = json.loads(text)
                    # check for new data
                    if json_data[0]["title"] != stored_data[0]["title"]:
                        # set up embed
                        img = "http://tryhackme.com/" + json_data[0]["image"]
                        title = json_data[0]["title"]
                        code = "http://tryhackme.com/room/" + json_data[0]["code"]
                        description = json_data[0]["description"]
                        embed = discord.Embed(title=title, description=description, url=code)
                        embed.set_image(url=img)
                        embed.set_author(name="TryHackMe",icon_url="https://tryhackme.com/img/THMlogo.png")
                        embed.set_footer(text="From the TryHackMe Official API!")
                        await channel.send("NEW ROOM")
                        await channel.send(embed=embed)
                        with open("storage.json", "w") as file:
                            file.write(text)
                            file.close()
            await asyncio.sleep(60)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.new_room()


def setup(bot):
    bot.add_cog(Room(bot))



