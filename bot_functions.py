import random
import discord
from general_util import *
from hardcoded_values import command_list



def run_function(message: discord.Message):
    bot_prefix = get_bot_prefix(message.guild.id)
    discord_input = message.content
    command = remove_prefix(discord_input.split()[0], bot_prefix).lower()  # get everything before the first space, if any
    args = remove_prefix(remove_prefix(discord_input, command),
                         " ").split()  # split everything after the command into a list of arguments
    if "get_prefix" in discord_input.lower():
        from server_config import get_server_prefix
        get_server_prefix(message)
    elif command == "set_prefix":
        from server_config import set_server_prefix
        set_server_prefix(message, args)
    elif command == "hello":
        from bot import send_message
        send_message(message.channel, 'Hello {0.author.mention}'.format(message))
    elif command == "help":
        from bot import send_message
        send_message(message.channel, "Command list:\n" + list_to_string(command_list))
    elif command == "invite":
        from bot import send_message
        send_message(message.channel, "Use this link to invite 2FBot to a server: https://discord.com/oauth2/authorize?client_id=532326343753596938&scope=bot")
    elif command == "random":
        from bot import send_message
        send_message(message.channel, str(random.choice(args)))
    elif command == "birthday":
        from birthday import birthday
        birthday(message, args)
    elif command == "mtgrule":
        from bot import send_message
        from mtg import find_rule
        send_message(message.channel, find_rule(args[0]))
    elif command == "secret_partners":
        from mtg import secret_partners
        secret_partners(message, args)
    elif command == "stand":
        from jojo import stand_stats
        stand_stats(message)
