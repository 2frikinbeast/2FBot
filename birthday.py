import datetime
import re

import discord

from bot import send_message
from general_util import remove_prefix, get_bot_prefix
from save import *


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

def birthday(message: discord.Message, args: list):
    date = args[0]
    if message.content.lower() == get_bot_prefix(str(message.guild.id)) + "birthday":
        try:
            birthdays_dict = load_dict_from_pkl("server_config/birthday/" + str(message.guild.id) + ".pkl")
            user_birthday = string_to_ymd(str(birthdays_dict[str(message.author.id)]))
            if user_birthday["year"] is None:
                send_message(message.channel, "Your birthday is " + str(user_birthday["month_name"]) + " " + str(user_birthday["day"]) + " in unknown year")
            else:
                send_message(message.channel, "Your birthday is " + str(user_birthday["month_name"]) + " " + str(
                    user_birthday["day"]) + " " + str(user_birthday["year"]))
        except (KeyError, FileNotFoundError):
            send_message(message.channel, "2FBot does not know your birthday. Use the command `" + get_bot_prefix(
                message.guild.id) + "birthday yyyy-mm-dd` to enter your birthday. `mm-dd` is also accepted.")
    elif re.match(r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))", date):  # yyyy-mm-dd
        user_birthday = string_to_ymd(date)
        send_message(message.channel, "Birthday parsed as " + user_birthday["month_name"] + " " + user_birthday["day"] + " " + user_birthday[
                "year"])
        user_birthday = datetime.datetime(int(user_birthday["year"]), int(user_birthday["month"]),
                                          int(user_birthday["day"]))
        user_birthday_dict = {str(message.author.id): user_birthday}
        merge_to_pkl_dictionary(user_birthday_dict, "server_config/birthday/" + str(message.guild.id) + ".pkl")
    elif re.match(r"^(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$", date):  # mm-dd
        month = date[0:2]
        day = remove_prefix(date[3:5], "0")
        month_string = number_to_month(month)
        send_message(message.channel, "Birthday parsed as " + month_string + " " + day)
        user_birthday = datetime.datetime(6969, int(month), int(day))
        user_birthday_dict = {str(message.author.id): user_birthday}
        merge_to_pkl_dictionary(user_birthday_dict, "server_config/birthday/" + str(message.guild.id) + ".pkl")
    else:
        send_message(message.channel, "That date is not valid. Input it in format `yyyy-mm-dd` or `mm-dd`")