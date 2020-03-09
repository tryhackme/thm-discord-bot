from discord.ext import commands
from requests.auth import HTTPBasicAuth
import discord 
import requests
import json
import time

from libs.embedmaker import officialEmbed

# Role IDs.
rolesF = json.loads(open("config/roles.json", "r").read())
adminID = rolesF["admin","Mod"]

# Issue's data.
creds = [cred.replace("\n","") for cred in open("jira_creds.txt","r")]
auth = HTTPBasicAuth(creds[0], creds[1])

issueName = "no_title"                      # The issue's title.
issueDesc = "no_description"                # The issue's desc.
issueProject = "BUG"                        # The issue's project.
issueType = "10021"                         # The issue's type. (10004 is task)
baseUrl = "https://tryhackme.atlassian.net" # The base URL.
issueUrl = baseUrl + "/rest/api/3/issue"    # The REST API url.

# The headers of the request.
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def hasRole(member, id):
        for role in member.roles:
                if id == role.id:
                        return True
        return False


class Jira(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    

    # Command to make a new issue to JIRA.
    @commands.command(description="Makes a new JIRA issue.", hidden=True)
    async def issue(self,ctx):

        # Remove the command.
        await ctx.message.delete()

        # Check for the user to be admin.
        if not hasRole(ctx.author, adminID):
            botMsg = await ctx.send("You do not have the permission to do that.")
            time.sleep(5)
            await botMsg.delete()
            return

        # Check for the author.
        def check(m):
            return m.author == ctx.author 

        # Retrieve the issue's name.
        botMsg = await ctx.send("Please provide a name for the new issue:")
        issueNameMsg = await self.bot.wait_for('message', check=check)
        issueName = issueNameMsg.content

        await botMsg.delete()
        await issueNameMsg.delete()


        # Retrieve the issue's desc.
        botMsg = await ctx.send("Now please provide a description:")

        issueDescMsg = await self.bot.wait_for('message', check=check)
        issueDesc = issueDescMsg.content + "\n -- Created by: " + ctx.author.display_name

        await botMsg.delete()
        await issueDescMsg.delete()

        # Confirmation embed.
        embed = officialEmbed("New issue", "This is the input you are about to create:")
        
        embed.add_field(name="Name", value=issueName)
        embed.add_field(name="Description", value=issueDesc)

        # Sends embed.
        botEmbed = await ctx.send(embed=embed)
        
        # Asks for validation.
        botMsg = await ctx.send("To confirm enter ***yes*** or anything else to cancel. (not case sensitive)")
        issueValid = await self.bot.wait_for('message', check=check)

        # Checks validation's answer.
        if issueValid.content.lower() == "yes":
            # Removes useless msg.
            await botMsg.delete()
            await issueValid.delete()

            # Creates the issue on JIRA.
            ## The payload made out of the issue's vars.
            payload = json.dumps( {
                "fields": {
                    "summary": issueName,
                    "issuetype": {
                        "id": issueType
                    },
                    "project": {
                        "key": issueProject
                    },
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                "text": issueDesc,
                                "type": "text"
                                }
                            ]
                            }
                        ]
                    }
                }
            } )

            ## Sends the the POST request.
            response = requests.request(
                "POST",
                issueUrl,
                data=payload,
                headers=headers,
                auth=auth
            )
            print("### JIRA issue creation report:")
            print(issueName + " : " + issueDesc)
            print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
            
            # Notifies the user.
            await ctx.send("Issue has been **created** by " + ctx.author.mention +  "!")
        else:
            # Removes useless msg.
            await botEmbed.delete()
            await botMsg.delete()
            await issueValid.delete()

            # Removes cancel msg.
            botMsg = await ctx.send("You have **cancelled** the issue!")
            time.sleep(5)
            await botMsg.delete()


def setup(bot):
    bot.add_cog(Jira(bot))
root@parabox:/home/paradox/THM-Bot/cogs# cat fun.py 
from discord.ext import commands
import discord
import json
import random
import aiohttp

from libs.embedmaker import officialEmbed


class Fun(commands.Cog, name="Fun Commands"):
    def __init__(self, bot):
        self.bot = bot


    ###################################
    ### Skidy, Ashu, Dark's quotes. ###
    ###################################

    @commands.command(description="Sends Skidy's emote.")
    async def skidy(self, ctx):
        response = officialEmbed(title=":slight_smile:", color=0x225999, author="Skidy", author_img="https://i.imgur.com/fSMnXPt.png", footer="")
        await ctx.send(embed=response)

    @commands.command(description="Send Ashu's emote.")
    async def ashu(self, ctx):
        response = officialEmbed(title=":slight_smile:", color=0x225999, author="Ashu", author_img="https://i.imgur.com/ojiqdem.png", footer="")
        await ctx.send(embed=response)

    @commands.command(description="Send a random Darkstar quote.")
    async def dark(self, ctx):
        darkF = json.loads(open("config/dark.json", "r").read())
        darkQuotes = darkF["quotes"]
        quote = darkQuotes[random.randint(0, len(darkQuotes)-1)]

        response = officialEmbed(title=quote, color=0xff4500, author="DarkStar7471", author_img="https://i.imgur.com/jZ908d1.png", footer="")
        await ctx.send(embed=response)


    ##############################
    ### HONK and BOOP and NOOT ###
    ##############################

    @commands.command(description="HOOONK!")
    async def honk(self, ctx):
        response = officialEmbed("!honk", "***HONK HONK HONK***", 0xff4500)
        response.set_image(url="https://cdn.discordapp.com/attachments/433685563674198016/630100135623524363/JPEG_20191003_021216.jpg")
        await ctx.send(embed=response)
    @commands.command(description="NOOT NOOT")
    async def noot(self,ctx):
        response = officialEmbed("!noot","NOOT NOOT",0xffffff)
        response.set_image(url="https://ichef.bbci.co.uk/images/ic/640x360/p01lc1vw.jpg")
        await ctx.send(embed=response)

    @commands.command(description="Boop someone!", usage="{@user}")
    async def boop(self, ctx, member: discord.Member=None):
        if ctx.message.channel.name == "bot-commands" and member is not None:
                if member.id == 572908911749890053: #Yume - Asphodel#8097 572908911749890053
                    desc = "<@{}>, you can't boop <@{}>!".format(ctx.author.id, member.id)
                    response = officialEmbed("!boop", desc, color=0xFFFFFF)
                else:
                    desc = "<@{}> was booped by <@{}>!".format(member.id, ctx.author.id)
                    response = officialEmbed("!boop", desc, color=0xFFFFFF)
                    response.set_image(url="http://giphygifs.s3.amazonaws.com/media/99LhY1qc6jG8w/giphy.gif")
                await ctx.send(embed=response)
        else:
            return


    ############
    ### XKCD ###
    ############

    @commands.command(description="Send a random XKCD comic.")
    async def xkcd(self,ctx):
        comic_no = random.randint(1,1900)
        url = f"http://xkcd.com/{comic_no}/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                new_data = await data.read()
                json_data = json.loads(new_data)
                img = json_data.get("img")
                title = json_data.get("title")
                alt = json_data.get("alt")

                response = officialEmbed(color=0xffb6b9, footer="From the XKCD Official API!")
                response.add_field(name=title,value=alt)
                response.set_image(url=img)
        await ctx.send(embed=response)
            
    ########################
    ### Shiba And Spaniel###
    ########################                  
    """
    todo:  Make it so it picks a random shiba pic from a directory on the server
    """
    @commands.command(description="NOOT NOOT")
    async def shibe(self,ctx):
        response = officialEmbed("!shibe","Shiba Inu",0xff4500)
        response.set_image(url="https://justsomething.co/wp-content/uploads/2017/12/ryujii-handsome-ridiculously-cute-shiba-japan-758x397.jpg")
        await ctx.send(embed=response)
    async def spaniel(self,ctx):
        response = officialEmbed("!spaniel","Spaniel",0xff4500)
        response.set_image(url="https://www.about-cocker-spaniels.com/images/cute-puppy-names-boys-1.jpg")
        await ctx.send(embed=response)
    

def setup(bot):
    bot.add_cog(Fun(bot))        
