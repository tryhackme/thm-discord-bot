import libs.config as config
import discord

configAuthor = config.get_config("info")["name"]
configAuthor_img = config.get_config("info")["logo"]
configFooter = config.get_config("info")["footer"]
configColor = config.get_config("colors")["site"]


def officialEmbed(title="", desc="", color=configColor, author=configAuthor, author_img=configAuthor_img, footer=configFooter, url=""):
    response = discord.Embed(
        title=title, description=desc, color=color, url="")
    response.set_author(name=author, icon_url=author_img)
    response.set_footer(text=footer)

    return response
