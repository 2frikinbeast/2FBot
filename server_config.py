import discord

from bot import send_message
from general_util import set_bot_prefix, get_bot_prefix


def get_server_prefix(message: discord.Message):
    msg = "`" + get_bot_prefix(message.guild.id) + "` is the current 2FBot prefix for " + str(message.guild)
    send_message(message.channel, msg)

def set_server_prefix(message: discord.Message, args):
    message_len = 0
    while message_len < len(message.author.roles):
        if discord.Permissions(message.author.roles[message_len]._permissions).manage_guild:
            new_prefix = args[0]
            set_bot_prefix(str(message.guild.id), new_prefix)
            msg = "Prefix changed to `" + new_prefix + "` for server " + str(message.guild.id) + " (" + str(
                message.guild) + ")"
            break
        else:
            message_len += 1
            msg = "You require \"Manage Server\" permissions to run this command"
    send_message(message.channel, msg)