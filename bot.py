import discord
import os

TOKEN = os.environ.get('2FBOT_TOKEN')

client = discord.Client()

cringe_words = ["cringe", "based"]

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    discord_input = message.content
    print(discord_input)

    if discord_input.lower() == "!hello":
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    for i in cringe_words:
        if i in discord_input.lower():
            msg = "\"Hurr, Cringe! Durr, Cringe! Cringe!\" \nIs that all you shitposting fucks can say?! \n\"ugh, based based based cringe cringe cringe based based cringe cringe\" \nI feel like I'm in a fucking asylum full of dementering old people, that can do nothing but repeat the same fucking words and look like a fucking broken record! \n\"Cringe cringe cringe cringe! cringe based based! onions onions soy! onions LOL onions! Cringe boomer Le zoomer! I am boomer?! No zoom zoom zoomies, zoomer going zoomies!\" \nAGH I FUCKING HATE THE INTERNET SO GOD DAMN MUCH!! FUCK SHITPOSTING HONEST GOD-FUCKING I HOPE YOUR MOTHER CHOKES ON HER OWN FECES IN HELL! YOU COCKSUCKER! \nOH BUT I KNOW MY POST IS CRINGED ISN'T IT? CRINGE CRINGE CRINGEY-CRINGE BASED CRINGE REDDIT CRINGE BASED REDDIT ONIONS BASED ONIONS CRINGE REDDIT CRINGE"
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
