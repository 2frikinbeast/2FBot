import math
import random
import re

import discord

from bot import client, direct_message, send_message
from general_util import remove_prefix, get_bot_prefix, remove_suffix


def find_rule(rule):
    file = open("MagicCompRules.txt", encoding="utf8")
    if rule.lower() == "random":
        lines = file.read().splitlines()
        random_rule = ""
        while not re.match(r"[0-9][0-9][0-9][.][0-9]+[a-z]+", random_rule):
            random_rule = random.choice(lines)
        return random_rule
    else:
        line = str(file.readline())
        count = 1
        while line:
            if line.startswith(rule):
                return line
            line = file.readline()
            count += 1
    return "Rule " + rule + " could not be found"


def secret_partners(message: discord.Message, args: list):
    discord_input = message.content
    player_list_string = remove_prefix(discord_input.lower(),
                                       get_bot_prefix(str(message.guild.id)) + "secret_partners ")
    player_list = []
    lone_wolf = ""
    for player in args:
        cleaned_user = remove_prefix(player, "<@!")
        cleaned_user = remove_suffix(cleaned_user, ">")
        player_list.append(cleaned_user)
    num_teams = math.floor(len(player_list) / 2)
    need_lone_wolf = not (len(player_list) % 2 == 0)
    if need_lone_wolf:
        await message.channel.send("Splitting " + player_list_string + " into " + str(
            num_teams) + " teams with one lone wolf. Please ensure your DMs are open.")
    else:
        await message.channel.send("Splitting " + player_list_string + " into " + str(
            num_teams) + " teams. Please ensure your DMs are open.")
    teams = {}
    chosen_players = []
    i = 1
    while i <= num_teams:
        teams[i] = {"normal": "", "secret": ""}
        i += 1
    j = 1
    while j <= len(player_list):
        random_player = random.choice(player_list)
        if random_player not in chosen_players:
            try:
                if teams[math.ceil(j / 2)]["normal"] == "":
                    teams[math.ceil(j / 2)]["normal"] = random_player
                    chosen_players.append(random_player)
                else:
                    teams[math.ceil(j / 2)]["secret"] = random_player
                    chosen_players.append(random_player)
            except KeyError:
                lone_wolf = random_player
                chosen_players.append(random_player)
            j += 1
    if not lone_wolf == "":
        if not direct_message(lone_wolf, "You are the lone wolf. Try to win the game by yourself!"):
            send_message(message.channel, "User <@!" + str(lone_wolf) + "> does not have open DMs!")
    k = 1
    while k <= len(teams):
        normal_teammate = int(teams[k]["normal"])
        secret_teammate = int(teams[k]["secret"])
        secret_teammate_name = client.get_user(secret_teammate).name
        if not direct_message(normal_teammate, "You are on a team with " + secret_teammate_name + ". Don't tell anyone!"):
            send_message(message.channel, "User <@!" + normal_teammate + "> does not have open DMs!")
        if not direct_message(secret_teammate, "You are on a team, but you don't know who your teammate is."):
            send_message(message.channel, "User <@!" + secret_teammate + "> does not have open DMs!")
        k += 1
