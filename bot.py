import datetime
import os
import random
import re
from os import path
import math

import Levenshtein
import discord

from data_management import *
from hardcoded_values import *

TOKEN = os.environ.get('2FBOT_TOKEN')

client = discord.Client()


def get_bot_prefix(server_id):
    config_file_path = "server_config/" + str(server_id) + ".pkl"
    try:
        config = load_dict_from_pkl(config_file_path)
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


def current_time():
    return datetime.utcnow()


def list_to_string(string_list, separator="\n"):
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


def part_color(part_number):
    part = int(part_number)
    if part == 3:
        return discord.Color(0x49408B)  # purple
    elif part == 4:
        return discord.Color(0xC5EDEF)  # blue
    elif part == 5:
        return discord.Color(0xDEA143)  # gold
    elif part == 6:
        return discord.Color(0x4A7D52)  # green
    elif part == 7:
        return discord.Color(0xF8A6F3)  # pink
    elif part == 8:
        return discord.Color(0xF3FCFD)  # white
    else:
        return discord.Color.dark_gray()


def check_stand_alias(alias):
    try:
        return stand_aliases[alias]
    except:
        return alias


with open('stand_list.txt') as fp:
    line = fp.readline()
    count = 1
    while line:
        stand_list.append(remove_suffix(line, '\n'))
        line = fp.readline()
        count += 1


def number_to_part(param):
    try:
        return parts[str(param)]
    except KeyError:
        return param


def pull_from_hardcoded_list(key, args):
    reminder_text = keywords_without_multiple_arguments[key].replace("arg1", list_to_string(args, " "))
    return reminder_text


def find_keyword(keyword_query):
    query_list = keyword_query.split()
    if query_list[0] == "equip":
        if len(query_list) > 1:  # if there is additional arguments
            reminder_text = "[Cost]: Attach this permanent to target (arg1) you control. Activate this ability only any time you could cast a sorcery."
            reminder_text = reminder_text.replace("(arg1)", list_to_string(query_list[1:], " "))
        else:
            reminder_text = keywords_without_multiple_arguments["equip"]
    elif query_list[0] == "hexproof" and query_list[1] == "from":
        reminder_text = pull_from_hardcoded_list("hexprooffrom", query_list[2:])
    elif query_list[0].endswith("walk"):
        reminder_text = "This creature can't be blocked as long as defending player controls a " + remove_suffix(
            query_list[0], "walk") + "."
    else:
        try:
            reminder_text = pull_from_hardcoded_list(query_list[0], query_list[1:])
        except KeyError:
            reminder_text = "Keyword not recognized. If you believe this to be an error, please submit an issue here: <https://github.com/2frikinbeast/2FBot/issues> (Please note that this feature is very much in beta.)"

    return reminder_text.replace("  ", " ")


def find_rule(rule):
    file = open("MagicCompRules.txt", encoding="utf8")
    if rule.lower() == "random":
        lines = file.read().splitlines()
        random_rule = ""
        while not re.match(r"[0-9][0-9][0-9][.][0-9]+[a-z]+", random_rule):
            random_rule = random.choice(lines)
        return random_rule
    else:
        rule_line = str(file.readline())
        rule_count = 1
        while rule_line:
            if rule_line.startswith(rule):
                return rule_line
            rule_line = file.readline()
            rule_count += 1
    return "Rule " + rule + " could not be found"


def number_to_month(month):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return switcher.get(int(month), "Invalid month")
    pass


def string_to_ymd(date_string):
    if date_string[0:4] == "6969":
        year = None
    else:
        year = date_string[0:4]
    month = date_string[5:7]
    day = remove_prefix(date_string[8:10], "0")
    date_dictionary = {
        "year": year,
        "month": month,
        "month_name": number_to_month(month),
        "day": day
    }
    return date_dictionary


class Error(Exception):
    pass

class CouldNotOpenDM(Error):
    pass


async def delete_message(offending_message, give_reason=False,
                         reason: str = "No reason given."):
    embed = discord.Embed(title="Your message in " + str(offending_message.guild) + " was deleted.")
    embed.add_field(name="Your message", value=offending_message.content)
    embed.set_thumbnail(url=offending_message.guild.icon_url)
    if give_reason:
        embed.add_field(name='Deletion reason', value=reason)
    try:
        await offending_message.author.send(embed=embed)
    except AttributeError:
        raise CouldNotOpenDM
    await offending_message.delete()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself

    global time_last_run
    if message.author == client.user:
        return
    else:
        discord_input = message.content
        print(str(message.author) + " in " + str(message.guild) + ": " + str(
            discord_input) + " https://discord.com/channels/" + str(message.guild.id) + "/" + str(
            message.channel.id) + "/" + str(message.id))

    if "get_prefix" in discord_input.lower():
        msg = "`" + get_bot_prefix(message.guild.id) + "` is the current 2FBot prefix for " + str(message.guild)
        await message.reply(msg, mention_author=False)

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "delete "):
        args = remove_prefix(discord_input, get_bot_prefix(str(message.guild.id)) + "delete ").split(" ")
        try:
            reason = list_to_string(args[1:], " ")
            message_url_args = args[0].split("/")
            message_id = message_url_args[-1]
            message_channel = client.get_channel(int(message_url_args[-2]))
            offending_message = await message_channel.fetch_message(int(message_id))
            if str(offending_message.guild.id) != str(message.guild.id):
                await message.reply("You must run this command in " + str(offending_message.guild) + " in order to delete that message.", mention_author=False)
            else:
                if message.author.guild_permissions.manage_messages:
                    if reason:
                        try:
                            await delete_message(offending_message, True, reason)
                            await message.reply("Message successfully deleted.", mention_author=False)
                        except discord.errors.Forbidden:
                            await message.reply("This bot does not have permission to Manage Messages.", mention_author=False)
                        except CouldNotOpenDM:
                            await message.reply("Failed to DM user deletion reason.\nMessage successfully deleted.", mention_author=False)
                    else:
                        try:
                            await delete_message(offending_message, True)
                            await message.reply("Message successfully deleted.", mention_author=False)
                        except discord.errors.Forbidden:
                            await message.reply("This bot does not have permission to Manage Messages.", mention_author=False)
                        except CouldNotOpenDM:
                            await message.reply("Failed to DM user deletion reason.\nMessage successfully deleted.", mention_author=False)
                else:
                    await message.reply("You do not have permissions to use `!!delete`. Manage Messages permission required.", mention_author=False)
        except IndexError:
            await message.reply("Invalid arguments. Command must be structured like this: `" + str(get_bot_prefix(str(message.guild.id))) + "delete <link to offending message> <deletion reason (optional)>`", mention_author=False)

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "set_prefix "):
        if message.author.guild_permissions.manage_guild:
            new_prefix = remove_prefix(discord_input.lower(), get_bot_prefix(str(message.guild.id)) + "set_prefix ")
            set_bot_prefix(str(message.guild.id), new_prefix)
            msg = "Prefix changed to `" + new_prefix + "` for server " + str(message.guild.id) + " (" + str(
                message.guild) + ")"
        else:
            msg = "You require \"Manage Server\" permissions to run this command"
        await message.reply(msg, mention_author=False)

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "secret_partners") and str(
            message.guild.id) == "706275564104843384":
        player_list_string = remove_prefix(discord_input.lower(),
                                           get_bot_prefix(str(message.guild.id)) + "secret_partners ")
        player_list_uncleaned = player_list_string.split(" ")
        player_list = []
        lone_wolf = ""
        for player in player_list_uncleaned:
            cleaned_user = remove_prefix(player, "<@!")
            cleaned_user = remove_suffix(cleaned_user, ">")
            player_list.append(cleaned_user)
        num_teams = math.floor(len(player_list) / 2)
        need_lone_wolf = not (len(player_list) % 2 == 0)
        if need_lone_wolf:
            await message.reply("Splitting " + player_list_string + " into " + str(
                num_teams) + " teams with one lone wolf. Please ensure your DMs are open.", mention_author=False)
        else:
            await message.reply("Splitting " + player_list_string + " into " + str(
                num_teams) + " teams. Please ensure your DMs are open.", mention_author=False)
        teams = {}
        chosen_players = []
        i = 1
        while i <= num_teams:
            teams[i] = {"normal": "", "secret": ""}
            i += 1
        j = 1
        while j <= len(player_list):
            random_player = random.choice(player_list)
            if not random_player in chosen_players:
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
        print(teams)
        if not lone_wolf == "":
            lone_wolf_user = client.get_user(int(lone_wolf))
            try:
                await lone_wolf_user.send("You are the lone wolf. Try to win the game by yourself!")
            except discord.errors.HTTPException:
                await message.reply("User <@!" + str(lone_wolf) + "> does not have open DMs!", mention_author=False)
        else:
            print("There is no lone wolf.")
        k = 1
        while k <= len(teams):
            normal_teammate = client.get_user(int(teams[k]["normal"]))
            secret_teammate = client.get_user(int(teams[k]["secret"]))
            secret_teammate_name = secret_teammate.name
            try:
                await normal_teammate.send("You are on a team with " + secret_teammate_name + ". Don't tell anyone!")
            except discord.errors.HTTPException:
                await message.reply("User <@!" + str(teams[k]["normal"]) + "> does not have open DMs!", mention_author=False)
            try:
                await secret_teammate.send("You are on a team, but you don't know who your teammate is.")
            except discord.errors.HTTPException:
                await message.reply("User <@!" + str(teams[k]["secret"]) + "> does not have open DMs!", mention_author=False)
            k += 1

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "random"):
        input = remove_prefix(discord_input.lower(), get_bot_prefix(str(message.guild.id)) + "random ")
        rand_list = input.split(" ")
        await message.reply(random.choice(rand_list), mention_author=False)

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "birthday"):
        date = remove_prefix(discord_input.lower(), get_bot_prefix(str(message.guild.id)) + "birthday ")
        if discord_input.lower() == get_bot_prefix(str(message.guild.id)) + "birthday":
            try:
                birthdays_dict = load_dict_from_pkl("server_config/birthday/" + str(message.guild.id) + ".pkl")
                user_birthday = string_to_ymd(str(birthdays_dict[str(message.author.id)]))
                if user_birthday["year"] is None:
                    await message.reply("Your birthday is " + str(user_birthday["month_name"]) + " " + str(
                        user_birthday["day"]) + " in unknown year.", mention_author=False)
                else:
                    await message.reply("Your birthday is " + str(user_birthday["month_name"]) + " " + str(
                        user_birthday["day"]) + " " + str(user_birthday["year"]) + ".", mention_author=False)
            except (KeyError, FileNotFoundError):
                await message.reply("2FBot does not know your birthday. Use the command `" + get_bot_prefix(
                    message.guild.id) + "birthday yyyy-mm-dd` to enter your birthday. `mm-dd` is also accepted.", mention_author=False)
        elif re.match(r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))", date):  # yyyy-mm-dd
            user_birthday = string_to_ymd(date)
            await message.reply(
                "Birthday parsed as " + user_birthday["month_name"] + " " + user_birthday["day"] + " " + user_birthday[
                    "year"], mention_author=False)
            user_birthday = datetime.datetime(int(user_birthday["year"]), int(user_birthday["month"]),
                                              int(user_birthday["day"]))
            user_birthday_dict = {str(message.author.id): user_birthday}
            merge_to_pkl_dictionary(user_birthday_dict, "server_config/birthday/" + str(message.guild.id) + ".pkl")
        elif re.match(r"^(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$", date):  # mm-dd
            month = date[0:2]
            day = remove_prefix(date[3:5], "0")
            month_string = number_to_month(month)
            await message.reply("Birthday parsed as " + month_string + " " + day, mention_author=False)
            user_birthday = datetime.datetime(6969, int(month), int(day))
            user_birthday_dict = {str(message.author.id): user_birthday}
            merge_to_pkl_dictionary(user_birthday_dict, "server_config/birthday/" + str(message.guild.id) + ".pkl")
        else:
            await message.reply("That date is not valid. Input it in format `yyyy-mm-dd` or `mm-dd`", mention_author=False)

    if discord_input.lower() == (get_bot_prefix(str(message.guild.id)) + "help"):
        msg = "Command list:\n" + list_to_string(command_list)
        await message.reply(msg, mention_author=False)

    if discord_input.lower() == (get_bot_prefix(str(message.guild.id)) + "hello"):
        await message.reply("Hello!")

    if discord_input.lower() == (get_bot_prefix(str(message.guild.id)) + "invite"):
        await message.reply(
            " Use this link to invite 2FBot to a server: https://discord.com/oauth2/authorize?client_id=532326343753596938&scope=bot&permissions=337984", mention_author=False)

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "coolness"):
        args = discord_input.lower().split(" ")
        if len(args) == 1:
            user_id = int(message.author.id)
        elif len(args) == 2:
            user_id = int(remove_suffix(remove_prefix(str(args[1]), "<@!"), ">"))
        if user_id == 83327063448092672:
            coolness = 200 #i am always cool 😎
        else:
            random.seed(user_id)
            coolness = random.randint(0, 100)
        if user_id == int(message.author.id):
            await message.reply("You are " + str(coolness) + "% cool.", mention_author=False)
        else:
            cool_user = await client.fetch_user(user_id)
            cool_username = cool_user.display_name
            await message.reply(cool_username + " is " + str(coolness) + "% cool.", mention_author=False)
        random.seed(a=None) #resets random seed

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "mtg_rule"):
        rule_query = remove_prefix(discord_input.lower(), (get_bot_prefix(str(message.guild.id)) + "mtg_rule "))
        await message.reply(find_rule(rule_query), mention_author=False)

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "mtg_keyword"):
        keyword_query = remove_prefix(discord_input.lower(), (get_bot_prefix(str(message.guild.id)) + "mtg_keyword "))
        await message.reply(find_keyword(keyword_query), mention_author=False)

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "stand"):
        stand_query = remove_prefix(discord_input, (get_bot_prefix(str(message.guild.id)) + "stand "))
        stand = check_stand_alias(most_similar_string(stand_query, stand_list))
        stand_file = 'stand_stats/' + stand + '.txt'
        if path.exists(stand_file):
            with open(stand_file) as fp:
                stand_stat_list = []
                line = fp.readline()
                count = 1
                while line:
                    stand_stat_list.append(remove_suffix(line, '\n'))
                    line = fp.readline()
                    count += 1
                description_text = list_to_string(
                    stand_stat_list[3:5]) + "**First appears in:** " + number_to_part(stand_stat_list[0])
                embed = discord.Embed(
                    title=stand_stat_list[2],
                    description=description_text,
                    color=part_color(stand_stat_list[0])
                )
                embed.set_thumbnail(url=stand_stat_list[1])
                embed.add_field(name='Stats', value=list_to_string(stand_stat_list[5:11]), inline=True)
                embed.add_field(name='Abilities', value=list_to_string(stand_stat_list[11:]), inline=True)
                await message.reply(embed=embed,mention_author=False)
        else:
            if stand == "Flaccid Pancake":
                await message.reply("Jesus fucking Christ, just search \"Limp Bizkit\"", mention_author=False)
            else:
                await message.reply(stand, mention_author=False)

    if str(message.guild.id) == "501837363228704768":
        for i in cringe_words:
            if i in discord_input.lower() and not "based on" in discord_input.lower():
                try:
                    if (datetime.utcnow() - time_last_run).total_seconds() >= cringe_copypasta_cooldown:
                        time_last_run = datetime.utcnow()
                        msg = list_to_string(cringe_copypasta)
                        await message.reply(msg, mention_author=False)
                    else:
                        return
                except NameError:
                    time_last_run = datetime.utcnow()
                    msg = list_to_string(cringe_copypasta)
                    await message.reply(msg, mention_author=False)
        return

    if str(message.guild.id) == "706275564104843384":
        if re.search(r"\b" + re.escape("tron") + r"\b", discord_input.lower()):
            msg = "**WOW\nFUCK\nTRON**"
            await message.reply(msg, mention_author=False)


@client.event
async def on_ready():
    print('Logged in as')
    print(str(client.user.name) + " (" + str(client.user.id) + ")")
    print('Servers connected to:')
    for guild in client.guilds:
        print(str(guild.name) + " (" + str(guild.id) + ")")
    print('------')


client.run(TOKEN)
