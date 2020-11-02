import discord

from bot import send_embed, send_message
from general_util import remove_suffix, remove_prefix, get_bot_prefix, most_similar_string, list_to_string
from os import path

stand_list = []
stand_aliases = {
    "Stairway to Heaven": "Made in Heaven",
    "THE WORLD (Part 7)": "THE WORLD (Steel Ball Run)",
    "Death 13": "Death Thirteen",
    "Shining Diamond": "Crazy Diamond",
    "Reverb ACT1": "Echoes ACT1",
    "Reverb ACT2": "Echoes ACT2",
    "Reverb ACT3": "Echoes ACT3",
    "Show Off": "Surface",
    "Love Extra": "Love Deluxe",
    "Worse Company": "Bad Company",
    "Chili Pepper": "Red Hot Chili Pepper",
    "Opal Jam": "Pearl Jam",
    "Pole Jam": "Pearl Jam",
    "Heaven's Gate": "Heaven's Door",
    "Achtug Baby": "Achtung Baby",
    "Heart Father": "Atom Heart Father",
    "BoyManMan": "Boy II Man",
    "Boy to Man": "Boy II Man",
    "Boy 2 Man": "Boy II Man",
    "Terra Ventus": "Earth Wind and Fire",
    "Highway Go Go": "Highway Star",
    "Feral Cat": "Stray Cat",
    "Catgrass": "Stray Cat",
    "Misterioso": "Enigma",
    "Deadly Queen": "Killer Queen",
    "Heart Attack": "Sheer Heart Attack",
    "Bite the Dust": "Bites the Dust",
    "Killer Queen (Part 8)": "Killer Queen (Jojolion)",
    "Sheer Heart Attack (Jojolion)": "Killer Queen (Jojolion)",
    "Sheer Heart Attack (Part 8)": "Killer Queen (Jojolion)",
    "D4C": "Dirty Deeds Done Dirt Cheap",
    "D4C Love Train": "Dirty Deeds Done Dirt Cheap Love Train",
    "Love Train": "Dirty Deeds Done Dirt Cheap Love Train",
    "Golden Wind": "Gold Experience",
    "Golden Wind Requiem": "Gold Experience Requiem",
    "Zipper Man": "Sticky Fingers",
    "Moody Jazz": "Moody Blues",
    "Six Bullets": "Sex Pistols",
    "Li'l Bomber": "Aerosmith",
    "Purple Smoke": "Purple Haze",
    "Spicy Lady": "Spice Girl",
    "Shadow Sabbath": "Black Sabbath",
    "Tender Machine": "Soft Machine",
    "Kraftwerk": "Kraft Work",
    "Craft Work": "Kraft Work",
    "Arts & Crafts": "Kraft Work",
    "Tiny Feet": "Little Feet",
    "Mirror Man": "Man in the Mirror",
    "Thankful Dead": "The Grateful Dead",
    "The Thankful Death": "The Grateful Dead",
    "Grand Death": "The Grateful Dead",
    "Fisher Man": "Beach Boy",
    "Babyhead": "Baby Face",
    "White Ice": "White Album",
    "Gently Weeps": "White Album",
    "White Album Gently Weeps": "White Album",
    "White Ice Gently Weeps": "White Album",
    "Metallic": "Metallica",
    "Crush": "Clash",
    "Talking Mouth": "Talking Head",
    "Notorious Chase": "Notorious B.I.G",
    "Sanctuary": "Oasis",
    "Green Tea": "Green Day",
    "Emperor Crimson": "King Crimson",
    "Epitaph": "King Crimson",
    "Eulogy": "King Crimson",
    "Chariot Requiem": "Silver Chariot Requiem",
    "Prophecy Stones": "Rolling Stones",
    "Stone Ocean": "Stone Free",
    "Smack": "Kiss",
    "F.F.": "Foo Fighters",
    "Weather Forecast": "Weather Report",
    "Cry Cry Dolls": "Goo Goo Dolls",
    "Pale Snake": "Whitesnake",
    "Highway to Death": "Highway to Hell",
    "Burning Down": "Burning Down the House",
    "Diver Drive": "Diver Down",
    "Jail House Lock": "Jail House Rock",
    "Full Moon": "C-Moon",
    "Maiden Heaven": "Made in Heaven",
    "Tomb of the Noise": "Tomb of the Boom",
    "Listen to My Rhythm": "Boku no Rhythm wo Kiitekure",
    "Oh Lonesome Me": "Oh! Lonesome Me",
    "Frightening Monsters": "Scary Monsters",
    "Mando": "Mandom",
    "Snow Mountain": "Sugar Mountain",
    "Tubular": "Tubular Bells",
    "Filthy Acts at a Reasonable Price": "Dirty Deeds Done Dirt Cheap",
    "King Bed": "California King Bed",
    "Going Underground": "Born This Way",
    "Autumn Leaves": "Les Feuilles",
    "Nuts N. Bolts": "Nut King Call",
    "Nat King Cole": "Nut King Call",
    "Paper Moon": "Paper Moon King",
    "Flower Park": "Paisley Park",
    "King of Nothingness": "King Nothing",
    "I, Rock": "I Am a Rock",
    "Ozone Baby": "Ozon Baby",
    "DocToR Woo": "Doctor Wu",
    "Satoru Akefu": "Wonder of U"
}
parts = {"3": "*Stardust Crusaders*",
         "4": "*Diamond is Unbreakable*",
         "5": "*Vento Aureo*",
         "6": "*Stone Ocean*",
         "7": "*Steel Ball Run*",
         "8": "*Steel Ball Run*"}


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


def number_to_part(param):
    try:
        return parts[str(param)]
    except KeyError:
        return param


def update_stand_list():
    with open('stand_list.txt') as fp:
        line = fp.readline()
        count = 1
        while line:
            stand_list.append(remove_suffix(line, '\n'))
            line = fp.readline()
            count += 1


def stand_stats(message: discord.Message):
    update_stand_list()
    stand_query = remove_prefix(message.content, (get_bot_prefix(str(message.guild.id)) + "stand "))
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
                stand_stat_list[3:5], "\n") + "**First appears in:** " + number_to_part(stand_stat_list[0])
            embed = discord.Embed(
                title=stand_stat_list[2],
                description=description_text,
                color=part_color(stand_stat_list[0])
            )
            embed.set_thumbnail(url=stand_stat_list[1])
            embed.add_field(name='Stats', value=list_to_string(stand_stat_list[5:11], "\n"), inline=True)
            embed.add_field(name='Abilities', value=list_to_string(stand_stat_list[11:], "\n"), inline=True)
            send_embed(message.channel, embed)
    else:
        if stand == "Flaccid Pancake":
            send_message(message.channel, "Jesus fucking Christ, just search \"Limp Bizkit\"")
        else:
            send_message(message.channel, stand)
