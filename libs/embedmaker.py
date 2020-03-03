import discord

configAuthor = "TryHackMe"
configAuthor_img = "https://tryhackme.com/img/THMlogo.png"
configFooter = "From TryHackMe with \u2764!"
configColor = 0x000000

def officialEmbed(title="", desc="", color=configColor, author=configAuthor, author_img=configAuthor_img, footer=configFooter, url=""):
    response = discord.Embed(title=title, description=desc, color=color, url="")
    response.set_author(name=author, icon_url=author_img)
    response.set_footer(text=footer)

    return response

# def officialEmbed(title, desc, footer):
#     return officialEmbed(title, desc, configColor, configAuthor, configAuthor_img, footer)

# def officialEmbed(title, desc, color):
#     return officialEmbed(title, desc, color, configAuthor, configAuthor_img, configFooter)

# def officialEmbed(title, desc):
#     return officialEmbed(title=title, desc=desc)