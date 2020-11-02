import discord
from save import *

DEFAULT_PREFIX = "!!"


def get_bot_prefix(server_id):
    config_file_path = "server_config/" + str(server_id) + ".pkl"
    try:
        config = load_dict_from_plk(config_file_path)
        return config["prefix"]
    except FileNotFoundError:
        return DEFAULT_PREFIX


def set_bot_prefix(server_id, new_prefix):
    config_file_path = "server_config/" + str(server_id) + ".pkl"
    try:
        prefix_dict = {"prefix": new_prefix}
        merge_to_pkl_dictionary(prefix_dict, config_file_path)
    except FileNotFoundError:
        config = {"prefix": new_prefix}
        save_dict_to_pkl(config, config_file_path)

async def send_message(send_channel: discord.TextChannel, message_to_send: str):
    await send_channel.send(message_to_send)
