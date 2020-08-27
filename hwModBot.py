#!/usr/bin/python3.7
# Homeworlds moderation and timer
# Displays the game state and keeps time control
import chessClock as cc
import discord
from asyncio import sleep
import channelTimer as ct
from sys import path
path.append('hwlogic/')
from text2turn import applyTextTurn as att
from hwstate import HWState
from draw import drawState
from match import Match

from os import path as ospath
imgSaveDir = ospath.join(ospath.dirname(__file__), 'stateImages/')

with open('private/token.txt','r') as fin:
    TOKEN = fin.readline().strip()

if 1:
    # Main HW server
    with open('private/guildID.txt','r') as fin:
        GUILD = int(fin.readline().strip())
else:
    # Testing server
    with open('private/testID.txt','r') as fin:
        GUILD = int(fin.readline().strip())

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds,id=GUILD)
    print(
        f'{client.user} is connected guild "{guild.name}"'
    )

# Map each channel to the match that is happening there
channel2match = {}

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

async def processTurn(message):
    # Check that this person should be making a move at all
    channel = message.channel
    match = channel2match[channel]
    ctimer = match.ctimer
    ctimer.confirmTurn(message)
    state = match.state
    # The move command
    cmd = message.content[1:]
    if cmd[0] == 'h':
        # Yes, this is kind of a sloppy way to do this
        # It's a homeworld creation:
        # append user name so that text2turn knows what to call the system
        cmd = '{} {}'.format(cmd,message.author.name)
    att(cmd,state)
    match.addTurn(cmd)

    fname = ospath.join(imgSaveDir,'{}.png'.format(channel.id))
    drawState(state,fname)
    # Upload the image
    with open(fname,'rb') as fin:
        df = discord.File(fin)
        await channel.send('',file=df)
    if state.isEnd():
        await channel.send('Game has ended:')
        await channel.send(match.getHistStr())
        await ctimer.stop(message)
        match.reset()
    else:
        await ctimer.addPly(message)

async def processCommand(message):
    channel = message.channel
    if not channel in channel2match:
        channel2match[channel] = Match(ct.ChannelTimer(channel))
    match = channel2match[channel]
    ctimer = match.ctimer
    if message.content == '!p':
        await ctimer.togglePause(message)
    elif message.content == '!pause':
        await ctimer.pause(message)
    elif message.content.startswith('!begin'):
        if ctimer.timing:
            raise Exception('Game is already running')
        channel2match[channel].state = HWState()
        await ctimer.begin(message)
    elif message.content == '!unpause':
        await ctimer.unpause(message)
    elif message.content == '!stop':
        if not ctimer.timing:
            await channel.send('Game is not running.')
            return
        await channel.send(match.getHistStr())
        await ctimer.stop(message)
        match.reset()
        await channel.send('Game cancelled. Please report anyone abusing this feature to Babamots.')
    elif message.content.startswith('!register'):
        await parseRegistration(message,ctimer)
    else:
        # It isn't a timer command, so it should be a game move
        await processTurn(message)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '' or message.content[0] != '!':
        return
    try:
        await processCommand(message)
    except cc.ChessClockException as e:
        await message.channel.send(str(e))
#        raise(e)
    except ct.InvalidTimerIteraction as e:
        await message.channel.send(str(e))
#        raise(e)
    except IndexError as e:
        # Make sure that any partial turn got cancelled
        channel2match[message.channel].state.cancelTurn()
        await message.channel.send('{}\n\nYou probably typed your move wrong.\nIf you think there\'s a bug, tell Babamots.'.format(str(e)))
    except Exception as e:
        channel2match[message.channel].state.cancelTurn()
        await message.channel.send('{}\n\nPlease check the instructions in the message pinned in the lobby channels.\nIf you think there\'s a bug, tell Babamots.'.format(str(e)))
        raise e

client.run(TOKEN)


