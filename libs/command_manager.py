import libs.config as config
from discord.channel import DMChannel
import libs.utils as utils
from enum import Enum

class Context(Enum):
    PUBLIC = 1
    DM = 2
    BOTH = 3

class _Roles():
    def __load_ranks(self):
        RANKS = []

        for rank in self._roles_id:
            RANKS.append(rank)

        return RANKS

    def __init__(self):
        self._roles_id = config.get_config("roles")

        self.ADMIN = self._roles_id["admin"]
        self.MOD = self._roles_id["mod"]

        self.DEVLEAD = self._roles_id["devLead"]
        self.DEV = self._roles_id["dev"]

        self.VERIFIED = self._roles_id["verified"]
        self.SUB = self._roles_id["sub"]
        self.CONTRIB = self._roles_id["contrib"]

        self.ANNOUNCEMENT = self._roles_id["announcementrole"]

        self.RANKS = self.__load_ranks()

roles = _Roles()

s_sanitized = config.get_string("not_sanitized")
s_no_perm = config.get_string("no_perm")
s_context_dm = config.get_string("context_dm_only")
s_context_public = config.get_string("context_public_only")

def __has_role__(member, id):
    """Check if the member has the roles."""

    for role in member.roles:
        if id == role.id:
            return True
    return False

def __check_context__(ctx, context):
    """Checks that the current context fits the desired one."""

    if context == Context.DM and (not isinstance(ctx.channel, DMChannel)):
        raise Exception(s_context_dm)
    elif context == Context.PUBLIC and isinstance(ctx.channel, DMChannel):
        raise Exception(s_context_public)

def __check_sanitized__(args):
    """Checks that every arg in args is sanitized correctly."""

    for arg in args:
        print("Doing: "+str(arg))
        if isinstance(arg, tuple) or isinstance(arg, list):
            __check_sanitized__(arg)
        else:
            if not utils.sanitize_check(arg):
                raise Exception(s_sanitized)

def __check_roles__(ctx, roles):
    """Checks that the user has all the required roles."""

    user = ctx.author
    has_perm = False

    # We want to know if the user has specific roles.
    for role in roles:
        if __has_role__(user, role):
            has_perm = True

    if not has_perm:
        raise Exception(s_no_perm)


async def command(ctx, args=None, roles=None, context=Context.BOTH):
    """Roles is an array (of roles) of required roles to execute the command. Args is an array (of string, or tuple of str, or array of str) of the arguments of the command."""

    # Checking for the context.
    try:
        __check_context__(ctx, context)
    except Exception as e:
        await ctx.send(e)
        return False

    # Checking if all the args are sanitized.
    if args != None:
        try:
            __check_sanitized__(args)
        except Exception as e:
            await ctx.send(e)
            return False

    # Checking if the user has permission.
    if roles != None:
        try:
            __check_roles__(ctx, roles)
        except Exception as e:
            await ctx.send(e)
            return False

    return True