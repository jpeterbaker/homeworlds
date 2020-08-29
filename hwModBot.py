#!/usr/bin/python3.7
# Homeworlds moderation and timer
# Initializes server
# Cleans inputs for GameMaster
# Displays the game state
import discord
from asyncio import sleep
from gameMaster import GameMaster
from sys import path

with open('private/token.txt','r') as fin:
    TOKEN = fin.readline().strip()

client = discord.Client()

"""
# THIS ONLY SEEMS TO BE NECESSARY IF A REFERENCE TO THE GUILD IS NEEDED
# Main HW server
with open('private/guildID.txt','r') as fin:
    GUILD = int(fin.readline().strip())

"""

@client.event
async def on_ready():
#    guild = discord.utils.get(client.guilds,id=GUILD)
    print(
        f'{client.user} is connected"'
    )

# Map each channel to the corresponding GameMaster
channel2master = {}

async def parseRegistration(message):
    channel = message.channel
    master = channel2master[channel]
    words = message.content.split()
    n = len(words)
    if n == 1:
        i = None
        dt = None
    elif n == 3:
        i = int(words[1])
        dt = int(words[2])
    else:
        await channel.send('Wrong number of arguments.\nSee "bot_instructions" channel for help.')
        return
    await master.register(message.author,i,dt)

async def processCommand(message):
    channel = message.channel
    if not channel in channel2master:
        channel2master[channel] = GameMaster(channel)
    master = channel2master[channel]
    if message.content == '!':
        await master.togglePause(message)
    elif message.content == '!pause':
        await master.pause(message)
    elif message.content.startswith('!begin'):
        await master.begin(message)
    elif message.content == '!unpause':
        await master.unpause(message)
    elif message.content.startswith('!register'):
        await parseRegistration(message)
    elif message.content == '!unregister':
        await master.unregister(message)
    elif message.content == '!stop':
        await master.stop(message)
    else:
        # It isn't a timer command, so it should be a game move
        await master.addTurn(message)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '' or message.content[0] != '!':
        return
    try:
        await processCommand(message)
    except IndexError as e:
        # Make sure that any partial turn got cancelled
        channel = message.channel
        master = channel2master[channel]
        master.cancelTurn()
        await channel.send('{}\n\nYou probably typed your move incorrectly.\nSee "bot_instructions" channel for help.\nIf you think there\'s a bug, tell Babamots.'.format(str(e)))
#        raise e
    except Exception as e:
        channel = message.channel
        master = channel2master[channel]
        master.cancelTurn()
        await channel.send('{}\n\nSee "bot_instructions" channel for help.\nIf you think there\'s a bug, tell Babamots.'.format(str(e)))
#        raise e

client.run(TOKEN)

