#Custom Emojis:
#
# <a:python3:232720527448342530>
# 01233333333456789ABCDEFGHIJKLM   #m=22  #value for custom_emoji

import discord, emoji, time

from STATICS import emoji_channels, conuting_channels
from SECRETS import DISCORD_TOKEN

client=discord.Client()

def is_only_emoji(message):
    custom_emoji = 0

    for i in message:
        if custom_emoji == 0: #Falls ein Unicode-Emoji oder Zeichen 0 (<)
            if not (i in emoji.UNICODE_EMOJI or i == " " or i == "\n"):
                if i == "<": custom_emoji = 1
                else: return False
        elif custom_emoji == 1: #Custom-Emoji Zeichen 1 (a oder :)
            if i == "a":            #Falls animiert
                custom_emoji = 2        #Erwarte beim zächsten Zeichen 2 (:)
            elif i == ":":          #Falls nicht animiert
                custom_emoji = 3        #Erwarte beim nächsten mal den Namen (Zeichen 3)
            else:
                return False

        elif custom_emoji == 2: #Custom-Emoji Zeichen 2 (:) (tritt ein falls animiert)
            if i == ":":
                custom_emoji = 3 #Erwarte beim nächsten mal den Namen (Zeichen 3)
            else:
                return False
        elif custom_emoji == 3: #Zeichen vom Namen
            if i == ">": return False
            if i == ":": custom_emoji = 4 #Mache weiter, sobald : erscheint
        elif 4 <= custom_emoji <= 21: # Zeichen 4 bis 21 müssen Nummern sein
            if not i.isdigit():
                return False
            custom_emoji += 1
        else:   #Ansonsten (Zeichen 22), Emoji-End mit >
            if i == ">":
                custom_emoji = 0
            else:
                return False

    if custom_emoji == 0: #Falls nicht bei einem Custom-Emoji unterbrochen wurde
        return True
    else:
        return False


async def is_nuber_right(new_message):

    messages = await new_message.channel.history(limit=2).flatten()
    message_before = messages[1]

    try:
        new_number = int(new_message.content)
        old_number = int(message_before.content)
        if new_number == old_number+1:
            return True
        else:
            return False
    except Exception:
        return False


async def checking(message):
    try:
        if message.author.bot:
            time.sleep(2)
            await message.delete()
            return

        if emoji_channels.__contains__(message.channel.id):
            if not is_only_emoji(message.content):
                await message.delete()

        elif conuting_channels.__contains__(message.channel.id):
            if not await is_nuber_right(message):
                await message.delete()

    except Exception as err:
        print(err)

@client.event
async def on_ready():
    print("Bot is running")

@client.event
async def on_message(message):
    await checking(message)

@client.event
async def on_message_edit(message_before, message):
    await checking(message)

client.run(DISCORD_TOKEN)