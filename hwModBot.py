#!/usr/bin/python3.7
# Homeworlds moderation and timer
# Initializes server
# Cleans inputs for GameMaster
# Displays the game state
import discord
from asyncio import sleep
from gameMaster import GameMaster,showState,buildState
from sys import path

with open('private/TESTINGtoken.txt','r') as fin:
    TOKEN = fin.readline().strip()
with open('private/adminID.txt','r') as fin:
    ADMIN = int(fin.readline().strip())

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

async def parseTime(message):
    words = message.content[1:].split()
    n = len(words)
    if n != 2:
        await message.channel.send('The "!time" command takes one parameter in the form "minutes:seconds".')
        return
    if len(words[1]) > 10:
        await message.channel.send('Maximum time for a player is {} seconds.'.format(int(maxTime.total_seconds())))
        return
    ms = [int(x) for x in words[1].split(':')]
    if len(ms) == 1:
        m = 0
        s = ms[0]
    elif len(ms) == 2:
        m = ms[0]
        s = ms[1]
    else:
        await message.channel.send('The "!time" command takes one parameter in the form "minutes:seconds".')
        return
        
    master = channel2master[message.channel]
    user = message.author
    await master.setTime(user,m,s)

async def parseRegistration(message):
    # Throw away the exclamation point
    words = message.content[1:].split()
    n = len(words)
    if n == 1:
        pos = None
    elif n == 2:
        if not words[1].strip() in '01':
            await message.channel.send('The "!register" command takes at most one parameter ("0" for first move or "1" for second).')
            return
        pos = int(words[1])
    else:
        await message.channel.send('The "!register" command takes at most one parameter ("0" for first move or "1" for second).')
        return

    master = channel2master[message.channel]
    user = message.author
    await master.register(user,pos)
    
async def processCommand(message):
    channel = message.channel
    if not channel in channel2master:
        channel2master[channel] = GameMaster(channel,ADMIN)
    master = channel2master[channel]
    if message.content == '!':
        await master.togglePause(message)
    elif message.content == '!stop':
        await master.stop(message)
    elif message.content == '!pause':
        await master.pause(message)
    elif message.content.startswith('!begin'):
        if 'r' in message.content:
            await master.begin(message,random=True)
        else:
            await master.begin(message,random=False)
    elif message.content == '!unpause':
        await master.unpause(message)
    elif message.content.startswith('!register'):
        await parseRegistration(message)
    elif message.content == '!unregister':
        await master.unregister(message)
    elif message.content.startswith('!time'):
        await parseTime(message)
    elif message.content.startswith('!resume'):
        await master.resume(message)
    elif message.content.startswith('!draw'):
        if master.inProgress:
            await channel.send('Drawing states during the game is likely to be confusing.\nPlease use a different channel.')
            return
        try:
            await showState(buildState(message.content[5:]),channel)
        except Exception as e:
            await channel.send('There was a problem processing your state string.')
            raise e
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
        channel = message.channel
        await channel.send('{}\n\nYou probably typed your move incorrectly.\nSee "bot_instructions" channel for help.\nIf you think there\'s a bug, tell Babamots.'.format(str(e)))
        raise e
    except Exception as e:
        channel = message.channel
        await channel.send('{}\n\nSee "bot_instructions" channel for help.\nIf you think there\'s a bug, tell Babamots.'.format(str(e)))
        raise e

client.run(TOKEN)

