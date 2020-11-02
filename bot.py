import datetime
import os

import discord

from bot_functions import run_function
from general_util import list_to_string
from hardcoded_values import cringe_words, cringe_copypasta, cringe_copypasta_cooldown

TOKEN = os.environ.get('2FBOT_TOKEN')

client = discord.Client()


async def send_message(send_channel: discord.TextChannel,
                       message_to_send: str):  # returns boolean False if message failed to send
    try:
        await send_channel.send(message_to_send)
        return True
    except:
        return False


async def send_embed(send_channel: discord.TextChannel, embed_to_send: discord.Embed):
    try:
        await send_channel.send(embed=embed_to_send)
        return True
    except:
        return False


async def direct_message(user_id: int, message_to_send: str):  # returns boolean False if direct message failed to send
    user = client.get_user(user_id)
    try:
        await user.send(message_to_send)
        return True
    except discord.errors.HTTPException:
        return False


@client.event
async def on_message(message):
    global time_last_run
    if str(message.guild.id) == "501837363228704768":
        for i in cringe_words:
            if i in message.content.lower() and "based on" not in message.content.lower():
                try:
                    if (datetime.utcnow() - time_last_run).total_seconds() >= cringe_copypasta_cooldown:
                        time_last_run = datetime.utcnow()
                        msg = list_to_string(cringe_copypasta, "\n")
                        await message.channel.send(msg)
                    else:
                        return
                except NameError:
                    time_last_run = datetime.utcnow()
                    msg = list_to_string(cringe_copypasta, "\n")
                    await message.channel.send(msg)
        return
    if not message.author == client.user:  # we do not want the bot to respond to itself
        run_function(message)
        print(str(message.author) + " in " + str(message.guild) + ": " + str(message.content))


@client.event
async def on_ready():
    if not direct_message(83327063448092672, "Bot is starting."):
        print("Failed to send startup DM to @2frikinbeast#2222")
    print('Logged in as')
    print(str(client.user.name) + " (" + str(client.user.id) + ")")
    print('Servers connected to:')
    for guild in client.guilds:
        print(str(guild.name) + " (" + str(guild.id) + ")")
    print('------')


client.run(TOKEN)
