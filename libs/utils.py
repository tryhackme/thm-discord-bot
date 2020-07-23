import aiohttp, json
from discord.utils import get

def sanitize_check(data, banned_char=None):
    """Checks if the input is sanitized."""

    default_chars = ["/", ";", "-", ">", "<", ":", "`", "\"", "|"]

    if banned_char == None:
        banned_char = default_chars

    if any((c in banned_char) for c in data):
        return False
    else:
        return True

async def add_role(member, id):
    """Add the role to the member."""

    await member.add_roles(get(member.guild.roles, id=id))

def has_role(member, id):
    """Check if the member has the roles. DO NOT USE, USE THE COMMAND MANAGER INSTEAD."""

    for role in member.roles:
        if id == role.id:
            return True
    return False

async def api_fetch(base_url, *args):
    """Fetch JSON from the URL."""

    async with aiohttp.ClientSession() as session:
        url = base_url

        for e in args:
            url += str(e)

        async with session.get(url) as new_data:
            data = await new_data.read()
            json_data = json.loads(data)

            return json_data


def bool_to_yesno(value: bool) -> str:
    return 'Yes' if value else 'No'
