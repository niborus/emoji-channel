#Custom Emojis:
#
# <:python3:232720527448342530>
# 01222222223456789ABCDEFGHIJKL   #L=21  #value for custom_emoji

import discord, emoji

DISCORD_TOKEN = "IJustSmashedTheKeyboard.oiuhDe5ui.JFIOEAWJF93W"    # Add your discord-token here
channels = [543861314053996565]                                     #Add a List with all Channel-IDs as Integer here

client=discord.Client()

def is_only_emoji(message):
    custom_emoji = 0

    for i in message:
        if custom_emoji == 0:
            if not (i in emoji.UNICODE_EMOJI or i == " " or i == "\n"):
                if i == "<": custom_emoji = 1
                else: return False
        elif custom_emoji == 1:
            if i == ":":
                custom_emoji = 2
            else:
                return False
        elif custom_emoji == 2:
            if i == ">": return False
            if i == ":": custom_emoji = 3
        elif 3 <= custom_emoji <= 20:
            if not i.isdigit():
                return False
            custom_emoji += 1
        else:
            if i == ">":
                custom_emoji = 0
            else:
                return False
    return True


async def checking(message):
    try:
        if message.author.bot:
            return
        if channels.__contains__(message.channel.id):
            if not is_only_emoji(message.content):
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