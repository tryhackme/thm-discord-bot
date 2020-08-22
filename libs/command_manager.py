"""Command Manager
Manages checking conditions for commands that need certain roles to be executed.

Use decorator function @check() to do proper permissions and input sanitation for your command.
i.e.

@command_manager.check(roles=["admin",
                              "mod",]
                       channels=["staff_channel"])
async fun_command(self, ctx):
    ...

There is also .sanitize_check(ctx, msg) for input sanitation. Will return false if msg contains
a forbidden character.

Names of roles and channels are derived from libs.config.get_config() (which comes from config/config.json)
"""

import libs.config as config
from discord.channel import DMChannel
from discord.ext import commands as error
import functools
import asyncio


# GLOBAL VARIABLES
ERROR_STRING = config.get_string("commands")
ROLE_IDS = config.get_config("roles")
CHANNEL_IDS = config.get_config("channels")
DEFAULT_BANNED = ["/", ";", "-", ">", "<", ":", "`", "\"", "|"]


def check(roles=None,
          channels=None,
          dm_flag=None):
    """Decorator for sanitizing arguments and checking permissions."""
    # Call this decorator function before a command in order to check the specific perms passed into it.
    # 'msg' is an array (of string, or nestable string array/tuples) of the arguments of the command.
    # 'roles' is an array (of str) of required role names user must have to execute the command.
    # 'channels' is an array (of str) of valid channel names that command can be executed in
    # 'dm_flag' is a bool for three allowed context types
    #   1.dm_flag is None  - Command can be executed in DMs and any channel
    #   2.dm_flag is True  - Command can only be executed in DMs
    #   3.dm_flag is False - Command can only be executed in a discord channel (no DM)

    # Turn arg roles into a list if it is a string for one-role commands.
    if type(roles) is str:
        roles = [roles]
    # Same as above but for channels.
    if type(channels) is str:
        channels = [channels]

    # Decorator magic. wrapper() is where the perm checking happens
    def perm_check(cmd):
        # Checking for the context.
        @functools.wraps(cmd)
        async def wrapper(*args, **kwargs):
            """Checks permissions of the message before executing command"""
            # wrapper args is the original args passed to the command being checked
            # second element of args will always be the discord message (Context object)
            ctx = args[1]

            # 1. Checking if dm_flag is set and if message is in DMs
            if dm_flag is not None:
                try:
                    check_context(ctx, dm_flag)
                # Error if message does not fit in DM or public channels.
                # TODO: log exceptions to debug
                except error.PrivateMessageOnly as e:
                    await error_response(ctx, "context_dm_only",
                                         delete_ctx=True)
                    return False
                except error.NoPrivateMessage as e:
                    await error_response(ctx, "context_public_only",
                                         delete_msg=False)
                    return False

            # 2. Checking for if message is in the list of channels provided. dm_flag = False for no DM
            if channels:
                try:
                    dm_allowed = dm_flag is not False
                    check_channel(ctx, channels, dm_allowed)
                # Error if channel is not in the listed channels
                except error.CommandInvokeError as e:
                    # TODO: log exception to debug
                    await error_response(ctx, "channel_not_allowed")
                    return False

            # 3. Checking if the user has permission.
            if roles:
                try:
                    check_roles(ctx, roles)
                # Error if user does not have any role in list of roles
                except error.MissingAnyRole as e:
                    # TODO: log exception to debug
                    await error_response(ctx, "no_perm")
                    return False

            # 4. If all checks succeeded, then execute original command.
            return await cmd(*args, **kwargs)

        return wrapper

    return perm_check


async def is_sanitized(ctx, msg, err_msg="not_sanitized", banned_chars=None):
    """Checks user input for any forbidden characters.
    Returns True if sanitary, otherwise throws the discord.ext.commands.BadArgument exception.
    """
    # Default banned characters are "/", ";", "-", ">", "<", ":", "`", "\"", "|"
    # err_msg flag will cause bot to respond with generic error message to ctx.channel if True

    # Use banned_chars if assigned, otherwise just use the default ban list. (RECOMMENDED)
    if banned_chars:
        banned = banned_chars
    else:
        banned = DEFAULT_BANNED

    for text in msg:
        # Check to see if arg is a list to also recursively sanitize anything in it
        if type(text) is tuple or \
           type(text) is list:
            await is_sanitized(ctx, text)
        else:
            # Otherwise, check text for sanitation.
            has_banned_chars = [char for char in text if char in banned]

            if has_banned_chars:
                if err_msg:
                    await error_response(ctx, err_msg)
                # TODO: log exception to debug/tracking channel
                raise error.BadArgument(message=msg)
    # If all text is sanitary, then return bool True
    return True


async def error_response(ctx, err_msg,
                         delete_msg=True,
                         delete_ctx=False):
    """Sends a bot err_msg to the channel in context, then deletes the error message after 5 seconds.
    delete flags will determine what gets deleted after 5 seconds.
    """
    # Tries to retrieve ERROR_STRING[err_msg], but if not found, then defaults to err_msg
    error_output = ERROR_STRING.get(err_msg, err_msg)

    bot_message = await ctx.send(error_output)

    if delete_msg or delete_ctx:
        await asyncio.sleep(5)
        if delete_msg:
            await bot_message.delete()
        if delete_ctx and type(ctx.channel) is not DMChannel:
            await ctx.message.delete()


def check_context(ctx, dm_flag):
    """Checks if the context is correct (DMs or public channel)"""
    dm_message = type(ctx.channel) is DMChannel

    # If message is not a DM and the command is DM only (dm_flag True)
    if not dm_message and dm_flag:
        raise error.PrivateMessageOnly
    # If message is a DM but the command is not allowed in DMs (dm_flag False)
    elif dm_message and not dm_flag:
        raise error.NoPrivateMessage

    return dm_message


def check_channel(ctx, channels, dm_allowed):
    """Checks the current channel is valid for the command with arg channels"""

    # Converts arg channels into corresponding channel IDs
    valid_channels = [CHANNEL_IDS[channel] for channel in channels]

    dm_appropriate = type(ctx.channel) is DMChannel and dm_allowed

    # Check if channel is in the list of channels
    if ctx.channel.id not in valid_channels and not dm_appropriate:
        raise error.CommandInvokeError(ctx)

    return True


def check_roles(ctx, roles):
    """Checks that the user has all the required roles."""
    user = ctx.author
    # Get the list of IDs from user.roles
    user_roles = [role.id for role in user.roles]

    # Get the list of required role IDs from roles arg
    req_roles = [ROLE_IDS[req_role] for req_role in roles]

    # Magic python sentence that checks if there's any roles in user_roles that
    # is also in the list of req_roles.
    if not [role for role in user_roles if role in req_roles]:
        raise error.MissingAnyRole(roles)

    return True
