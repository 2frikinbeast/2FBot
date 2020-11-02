import datetime
import math
import os
import random
import re
from os import path

from birthday import *
from discord_util import *
from general_util import *
from hardcoded_values import *
from jojo import *
from mtg import *

TOKEN = os.environ.get('2FBOT_TOKEN')

client = discord.Client()

update_stand_list()


@client.event
async def on_message(message):
    global time_last_run
    if message.author == client.user:  # we do not want the bot to respond to itself
        return
    else:
        discord_input = message.content
        print(str(message.author) + " in " + str(message.guild) + ": " + str(discord_input))

    if "get_prefix" in discord_input.lower():
        msg = "`" + get_bot_prefix(message.guild.id) + "` is the current 2FBot prefix for " + str(message.guild)
        await message.channel.send(msg)

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "set_prefix "):
        message_len = 0
        while message_len < len(message.author.roles):
            if discord.Permissions(message.author.roles[message_len]._permissions).manage_guild:
                new_prefix = remove_prefix(discord_input.lower(), get_bot_prefix(str(message.guild.id)) + "set_prefix ")
                set_bot_prefix(str(message.guild.id), new_prefix)
                msg = "Prefix changed to `" + new_prefix + "` for server " + str(message.guild.id) + " (" + str(
                    message.guild) + ")"
                break
            else:
                message_len += 1
                msg = "You require \"Manage Server\" permissions to run this command"
        await message.channel.send(msg)

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
                await message.channel.send("User <@!" + str(lone_wolf) + "> does not have open DMs!")
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
                await message.channel.send("User <@!" + str(teams[k]["normal"]) + "> does not have open DMs!")
            try:
                await secret_teammate.send("You are on a team, but you don't know who your teammate is.")
            except discord.errors.HTTPException:
                await message.channel.send("User <@!" + str(teams[k]["secret"]) + "> does not have open DMs!")
            k += 1

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "random"):
        input = remove_prefix(discord_input.lower(), get_bot_prefix(str(message.guild.id)) + "random ")
        rand_list = input.split(" ")
        await message.channel.send(random.choice(rand_list))

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "birthday"):
        date = remove_prefix(discord_input.lower(), get_bot_prefix(str(message.guild.id)) + "birthday ")
        if discord_input.lower() == get_bot_prefix(str(message.guild.id)) + "birthday":
            try:
                birthdays_dict = load_dict_from_plk("server_config/birthday/" + str(message.guild.id) + ".pkl")
                user_birthday = string_to_ymd(str(birthdays_dict[str(message.author.id)]))
                if user_birthday["year"] is None:
                    await message.channel.send("Your birthday is " + str(user_birthday["month_name"]) + " " + str(
                        user_birthday["day"]) + " in unknown year")
                else:
                    await message.channel.send("Your birthday is " + str(user_birthday["month_name"]) + " " + str(
                        user_birthday["day"]) + " " + str(user_birthday["year"]))
            except (KeyError, FileNotFoundError):
                await message.channel.send("2FBot does not know your birthday. Use the command `" + get_bot_prefix(
                    message.guild.id) + "birthday yyyy-mm-dd` to enter your birthday. `mm-dd` is also accepted.")
        elif re.match(r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))", date):  # yyyy-mm-dd
            user_birthday = string_to_ymd(date)
            await message.channel.send(
                "Birthday parsed as " + user_birthday["month_name"] + " " + user_birthday["day"] + " " + user_birthday[
                    "year"])
            user_birthday = datetime.datetime(int(user_birthday["year"]), int(user_birthday["month"]),
                                              int(user_birthday["day"]))
            user_birthday_dict = {str(message.author.id): user_birthday}
            merge_to_pkl_dictionary(user_birthday_dict, "server_config/birthday/" + str(message.guild.id) + ".pkl")
        elif re.match(r"^(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$", date):  # mm-dd
            month = date[0:2]
            day = remove_prefix(date[3:5], "0")
            month_string = number_to_month(month)
            await message.channel.send("Birthday parsed as " + month_string + " " + day)
            user_birthday = datetime.datetime(6969, int(month), int(day))
            user_birthday_dict = {str(message.author.id): user_birthday}
            merge_to_pkl_dictionary(user_birthday_dict, "server_config/birthday/" + str(message.guild.id) + ".pkl")
        else:
            await message.channel.send("That date is not valid. Input it in format `yyyy-mm-dd` or `mm-dd`")

    if discord_input.lower() == (get_bot_prefix(str(message.guild.id)) + "help"):
        msg = "Command list:\n" + list_to_linebroken_string(command_list)
        await message.channel.send(msg)

    if discord_input.lower() == (get_bot_prefix(str(message.guild.id)) + "hello"):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if discord_input.lower() == (get_bot_prefix(str(message.guild.id)) + "invite"):
        await message.channel.send(
            " Use this link to invite 2FBot to a server: https://discord.com/oauth2/authorize?client_id=532326343753596938&scope=bot")

    if discord_input.lower().startswith(get_bot_prefix(str(message.guild.id)) + "mtgrule"):
        rule_query = remove_prefix(discord_input.lower(), (get_bot_prefix(str(message.guild.id)) + "mtgrule "))
        await message.channel.send(find_rule(rule_query))

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
                description_text = list_to_linebroken_string(
                    stand_stat_list[3:5]) + "**First appears in:** " + number_to_part(stand_stat_list[0])
                embed = discord.Embed(
                    title=stand_stat_list[2],
                    description=description_text,
                    color=part_color(stand_stat_list[0])
                )
                embed.set_thumbnail(url=stand_stat_list[1])
                embed.add_field(name='Stats', value=list_to_linebroken_string(stand_stat_list[5:11]), inline=True)
                embed.add_field(name='Abilities', value=list_to_linebroken_string(stand_stat_list[11:]), inline=True)
                await message.channel.send(embed=embed)
        else:
            if stand == "Flaccid Pancake":
                await message.channel.send("Jesus fucking Christ, just search \"Limp Bizkit\"")
            else:
                await message.channel.send(stand)

    if str(message.guild.id) == "501837363228704768":
        for i in cringe_words:
            if i in discord_input.lower() and not "based on" in discord_input.lower():
                try:
                    if (datetime.utcnow() - time_last_run).total_seconds() >= cringe_copypasta_cooldown:
                        time_last_run = datetime.utcnow()
                        msg = list_to_linebroken_string(cringe_copypasta)
                        await message.channel.send(msg)
                    else:
                        return
                except NameError:
                    time_last_run = datetime.utcnow()
                    msg = list_to_linebroken_string(cringe_copypasta)
                    await message.channel.send(msg)
        return


@client.event
async def on_ready():
    print('Logged in as')
    print(str(client.user.name) + " (" + str(client.user.id) + ")")
    print('Servers connected to:')
    for guild in client.guilds:
        print(str(guild.name) + " (" + str(guild.id) + ")")
    print('------')


client.run(TOKEN)
