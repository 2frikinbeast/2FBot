from datetime import datetime

import Levenshtein

from save import *

DEFAULT_PREFIX = "!!"


def get_bot_prefix(server_id: str):
    config_file_path = "server_config/" + str(server_id) + ".pkl"
    try:
        config = load_dict_from_pkl(config_file_path)
        return config["prefix"]
    except FileNotFoundError:
        return DEFAULT_PREFIX


def set_bot_prefix(server_id: str, new_prefix: str):
    config_file_path = "server_config/" + str(server_id) + ".pkl"
    try:
        prefix_dict = {"prefix": new_prefix}
        merge_to_pkl_dictionary(prefix_dict, config_file_path)
    except FileNotFoundError:
        config = {"prefix": new_prefix}
        save_dict_to_pkl(config, config_file_path)


def current_time():
    return datetime.utcnow()


def list_to_string(string_list: list, separator: str):
    output = ""
    for item in string_list:
        output += (item + separator)
    return output


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def remove_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:(-1 * len(suffix))]
    return text


def most_similar_string(query, search_list):
    similarity_min = 10000
    output = ""
    for item in search_list:
        if Levenshtein.distance(query, item) < similarity_min:
            similarity_min = Levenshtein.distance(query, item)
            output = item
    return output
