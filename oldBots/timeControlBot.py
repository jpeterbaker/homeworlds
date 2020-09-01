#!/usr/bin/python3.7
# A pretty serious time control bot that handles each channel separately
# and forces players to take turns
import chessClock as cc
import discord
from asyncio import sleep
import channelTimer as ct

with open('private/token.txt','r') as fin:
    TOKEN = fin.readline().strip()

with open('private/guildID.txt','r') as fin:
    GUILD = int(fin.readline().strip())

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds,id=GUILD)
    print(
        f'{client.user} is connected guild "{guild.name}"'
    )

# map Channel to its respective ChannelTimer
channel2timer = {}

async def parseRegistration(message,ctimer):
    words = message.content.split()
    n = len(words)
    if n == 1:
        i = None
        dt = None
    elif n == 3:
        i = int(words[1])
        dt = int(words[2])
    else:
        await channel.send('Wrong number of arguments. See pinned message for instructions.')
        ctimer.register(message.author,int(words[1]),int(words[2]))
        return
    await ctimer.register(message.author,i,dt)

async def processCommand(message):
    channel = message.channel
    if not channel in channel2timer:
        channel2timer[channel] = ct.ChannelTimer(channel)
    ctimer = channel2timer[channel]
    if message.content == '!':
        # Main button: change the player on move
        await ctimer.addPly(message)
    elif message.content.startswith('!begin'):
        await ctimer.begin(message)
    elif message.content == '!unpause':
        await ctimer.unpause(message)
    elif message.content == '!p':
        await ctimer.togglePause(message)
    elif message.content == '!pause':
        await ctimer.pause(message)
    elif message.content == '!stop':
        await ctimer.stop(message)
    elif message.content.startswith('!register'):
        await parseRegistration(message,ctimer)
    else:
        await channel.send('Unknown command. See pinned message for instructions.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[0] != '!':
        return
    try:
        await processCommand(message)
    except cc.ChessClockException as e:
        await message.channel.send(str(e))
#        raise(e)
    except ct.InvalidTimerIteraction as e:
        await message.channel.send(str(e))
#        raise(e)
    except Exception as e:
        await message.channel.send('An error was not handled gracefully:')
        await message.channel.send(str(e))
        await message.channel.send('Review the pinned message for instructions.\nIf there\'s a bug, tell Babamots')
        raise e

client.run(TOKEN)

