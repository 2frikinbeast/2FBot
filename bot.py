import os
import discord
import Levenshtein
from os import path

TOKEN = os.environ.get('2FBOT_TOKEN')

client = discord.Client()

command_prefix = "!!"
cringe_words = ["cringe", "based"]
cringe_copypasta = ["\"Hurr, Cringe! Durr, Cringe! Cringe!\"",
                    "Is that all you shitposting fucks can say?!",
                    "\"ugh, based based based cringe cringe cringe based based cringe cringe\"",
                    "I feel like I'm in a fucking asylum full of dementering old people, that can do nothing but "
                    "repeat the same fucking words and look like a fucking broken record!",
                    "\"Cringe cringe cringe cringe! cringe based based! onions onions snoy! onions LOL onions! Cringe "
                    "boomer Le zoomer! I am boomer?! No zoom zoom zoomies, zoomer going zoomies!\"",
                    "AGH I FUCKING HATE THE INTERNET SO GOD DAMN MUCH!! FUCK SHITPOSTING HONEST GOD-FUCKING I HOPE "
                    "YOUR MOTHER CHOKES ON HER OWN FECES IN HELL! YOU COCKSUCKER!",
                    "OH BUT I KNOW MY POST IS CRINGED ISN'T IT? CRINGE CRINGE CRINGEY-CRINGE BASED CRINGE REDDIT "
                    "CRINGE BASED REDDIT ONIONS BASED ONIONS CRINGE REDDIT CRINGE"]
command_list = ["help", "hello"]
stand_list = []


def list_to_linebroken_string(string_list):
    output = ""
    for item in string_list:
        output += (item + "\n")
    return output


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def remove_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:(-1 * len(suffix))]
    return text


def most_similar_string(query, list):
    similarity_min = 10000
    output = ""
    for item in list:
        if Levenshtein.distance(query, item) < similarity_min:
            similarity_min = Levenshtein.distance(query, item)
            output = item
    return output


def part_color(part):
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


with open('stand_list.txt') as fp:
    line = fp.readline()
    count = 1
    while line:
        stand_list.append(remove_suffix(line, '\n'))
        line = fp.readline()
        count += 1


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    else:
        discord_input = message.content
        print(discord_input)

    if discord_input.lower() == (command_prefix + "help"):
        msg = "Command list" + list_to_linebroken_string(command_list)

    if discord_input.lower() == (command_prefix + "hello"):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if discord_input.lower().startswith(command_prefix + "stand"):
        stand_query = remove_prefix(discord_input, (command_prefix + "stand "))
        stand = most_similar_string(stand_query, stand_list)
        if stand == "Stairway to Heaven":
            stand = "Made in Heaven"
        elif stand == "THE WORLD (Part 7)" or stand == "THE WORLD (Diego)":
            stand == "THE WORLD (Steel Ball Run)"
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
                embed = discord.Embed(
                    title=stand_stat_list[2],
                    description=list_to_linebroken_string(stand_stat_list[3:5]),
                    color=part_color(int(stand_stat_list[0]))
                )
                embed.set_thumbnail(url=stand_stat_list[1])
                embed.add_field(name='Stats', value=list_to_linebroken_string(stand_stat_list[5:11]), inline=True)
                embed.add_field(name='Abilities', value=list_to_linebroken_string(stand_stat_list[11:]), inline=True)
                await message.channel.send(embed=embed)
        else:
            await message.channel.send(stand)

    if 'based on' in discord_input.lower():
        return
    else:
        for i in cringe_words:
            if i in discord_input.lower():
                msg = list_to_linebroken_string(cringe_copypasta)
                await message.channel.send(msg)
                return
        return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
