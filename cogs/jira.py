import json
import time

import discord
import requests
from discord.ext import commands
from requests.auth import HTTPBasicAuth

import libs.config as config
from libs.embedmaker import officialEmbed
from libs.utils import has_role as has_role

####################
# Config variables #
####################

# Role IDs.
roles = config.get_config("roles")
id_admin = roles["admin"]
id_mod = roles["mod"]

# Strings.
s_no_perm = config.get_string("no_perm")
s_jira = config.get_string("jira")

# Config.
c_creds_jira = config.get_config("jira_creds")

# Creds.
creds = [cred.replace("\n", "") for cred in open(c_creds_jira, "r")]
auth = HTTPBasicAuth(creds[0], creds[1])

# Issue's data.
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


############
# COG Body #
############

class Jira(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to make a new issue to JIRA.
    @commands.command(description=s_jira["help_desc"] + " (Admin, Mod)", hidden=True)
    async def issue(self, ctx):

        # Remove the command.
        await ctx.message.delete()

        # Check for the user to be admin.
        if not (has_role(ctx.author, id_admin) or has_role(ctx.author, id_mod)):
            botMsg = await ctx.send(s_no_perm)
            time.sleep(5)
            await botMsg.delete()
            return

        # Check for the author.
        def check(m):
            return m.author == ctx.author

        # Retrieve the issue's name.
        botMsg = await ctx.send(s_jira["issue_name"])
        issueNameMsg = await self.bot.wait_for('message', check=check)
        issueName = issueNameMsg.content

        await botMsg.delete()
        await issueNameMsg.delete()

        # Retrieve the issue's desc.
        botMsg = await ctx.send(s_jira["issue_desc"])

        issueDescMsg = await self.bot.wait_for('message', check=check)
        issueDesc = issueDescMsg.content + "\n -- Created by: " + ctx.author.display_name

        await botMsg.delete()
        await issueDescMsg.delete()

        # Confirmation embed.
        embed = officialEmbed(
            "New issue", s_jira["confirm_title"])

        embed.add_field(name="Name", value=issueName)
        embed.add_field(name="Description", value=issueDesc)

        # Sends embed.
        botEmbed = await ctx.send(embed=embed)

        # Asks for validation.
        botMsg = await ctx.send(s_jira["confirm"])
        issueValid = await self.bot.wait_for('message', check=check)

        # Checks validation's answer.
        if issueValid.content.lower() == "yes":
            # Removes useless msg.
            await botMsg.delete()
            await issueValid.delete()

            # Creates the issue on JIRA.
            # The payload made out of the issue's vars.
            payload = json.dumps({
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
            })

            # Sends the the POST request.
            response = requests.request(
                "POST",
                issueUrl,
                data=payload,
                headers=headers,
                auth=auth
            )
            print("### JIRA issue creation report:")
            print(issueName + " : " + issueDesc)
            print(json.dumps(json.loads(response.text),
                             sort_keys=True, indent=4, separators=(",", ": ")) + "\n")

            # Notifies the user.
            await ctx.send(s_jira["confirmation"].format(ctx.author.mention))
        else:
            # Removes useless msg.
            await botEmbed.delete()
            await botMsg.delete()
            await issueValid.delete()

            # Removes cancel msg.
            botMsg = await ctx.send(s_jira["canceled"])
            time.sleep(5)
            await botMsg.delete()


def setup(bot):
    bot.add_cog(Jira(bot))
