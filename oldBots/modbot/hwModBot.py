#!/usr/bin/python3.7
# Homeworlds moderation and timer
# Initializes server
# Cleans inputs for GameMaster
# Displays the game state
from asyncio import sleep
from gameMaster import GameMaster,showState,buildState,t2t
from sys import path,argv
import re

################################
# Regexes for parsing commands #
################################

# !time [minutes]:seconds [h|f inc]
# h for hourglass, f for Fischer, inc is increment
# Groups are
# 1: minutes (or None)
# 2: seconds
timere = re.compile(r'^(?:(\d+)\s*:\s*)?(\d+)\s*$')

commandre = re.compile(r'^\s*!\s*(\w*)\s*(.*)$' , re.DOTALL)

beginre    = re.compile(r'^(r)?\s*$',re.I)
registerre = re.compile(r'^(0|1)?\s*')

"""
# THIS ONLY SEEMS TO BE NECESSARY IF A REFERENCE TO THE GUILD IS NEEDED
# Main HW server
with open('private/guildID.txt','r') as fin:
    GUILD = int(fin.readline().strip())

"""

#####################################
# Functions for individual commands #
#####################################
# All commands that can make a move
turnTerms = (
    t2t.buildTerms
    | t2t.tradeTerms
    | t2t.attackTerms
    | t2t.moveTerms
    | t2t.discoverTerms
    | t2t.catTerms
    | t2t.sacTerms
    | t2t.hwTerms
    | t2t.passTerms
)

# Registration commands

async def register(user,master,params):
    m = registerre.search(params)
    if m is None:
        await channel.send('The "!register" command takes one optional parameter, either 0 or 1.')
        return
    pos = m.group(1)
    if pos is None:
        await master.register(user,None)
    else:
        await master.register(user,int(pos))

async def unregister(user,master,params=''):
    await master.unregister(user)

async def cancel(user,master,params=''):
    await master.cancel(user)

async def time(user,master,params):
    m = timere.search(params)
    if m is None:
        await master.channel.send('See "bot_instructions" channel for help with "!time" command.')
        return
    minutes = m.group(1)
    seconds = safeInt(m.group(2))
    if minutes is None:
        minutes = 0
    else:
        minutes = safeInt(minutes)
    await master.setTime(user,60*minutes+seconds)

async def begin(user,master,params):
    m = beginre.search(params)
    if m is None:
        await master.channel.send('The "!begin" command takes one optional parameter "r" to randomize first move.')
        return
    pos = m.group(1)
    await master.begin(user,pos is not None)

# Timer types

def safeInt(s):
    # Turn a string into an int while checking the length for overflow attacks
    s = s.strip()
    if len(s) > 4:
        raise Exception('Input parameter appears to be too large of a number')
    return int(s)

async def simple(user,master,params=''):
    await master.setTimerStyle(user,'s')
async def fischer(user,master,params):
    m = timere.search(params)
    if m is None:
        inc = None
    else:
        minutes = m.group(1)
        seconds = safeInt(m.group(2))
        if minutes is None:
            minutes = 0
        else:
            minutes = safeInt(minutes)
        inc = 60*minutes+seconds
    await master.setTimerStyle(user,'f',inc)
async def hourglass(user,master,params=''):
    await master.setTimerStyle(user,'h')

# Gameplay commands

async def undo(user,master,params=''):
    await master.undo(user)

async def stop(user,master,params=''):
    await master.stop(user)

async def pause(user,master,params=''):
    await master.pause(user)

async def unpause(user,master,params=''):
    await master.unpause(user)

async def toggle(user,master,params=''):
    await master.togglePause(user)

# Other commands

async def draw(user,master,params):
    state = buildState(params)
    await showState(state,master.channel)

async def resume(user,master,params):
    await master.resume(user,params)

# Main command driver function
command2func = {
    'register':   register,
    'unregister': unregister,
    'cancel':     cancel,
    'time':       time,
    'begin':      begin,

    'simple':    simple,
    'fischer':   fischer,
    'fisher':    fischer,
    'hourglass': hourglass,

    'undo':       undo,
    'stop':       stop,
    'pause':      pause,
    'unpause':    unpause,
    '':           toggle,

    'draw':       draw,
    'resume':     resume
}

# Map each channel to the corresponding GameMaster
channel2master = {}

async def processCommand(command,params,user,channel):
    if not channel in channel2master:
        channel2master[channel] = GameMaster(channel,ADMIN)
    master = channel2master[channel]
    command = command.lower()
    if command in command2func:
        func = command2func[command]
        await func(user,master,params)
    elif command in turnTerms:
        await master.addTurn(user,'{} {}'.format(command,params))
    else:
        raise Exception('Command not understood: "{}"'.format(command))

if __name__=='__main__':
    import discord
    #######################
    # Load identification #
    #######################
    if len(argv) > 1:
        print('debugging mode')
        print('printing errors and connecting only to Test server')
        DEBUGGING = True
    else:
        print('production mode')
        print('silencing errors and connecting only to HW server')
        DEBUGGING = False

    if DEBUGGING:
        with open('private/TESTINGtoken.txt','r') as fin:
            TOKEN = fin.readline().strip()
    else:
        with open('private/token.txt','r') as fin:
            TOKEN = fin.readline().strip()

    with open('private/adminID.txt','r') as fin:
        # ID of the human channel admin
        # User with this id can give commands during games
        ADMIN = int(fin.readline().strip())

    client = discord.Client()

    ######################
    # Responses to event #
    ######################
    @client.event
    async def on_ready():
    #    guild = discord.utils.get(client.guilds,id=GUILD)
        print(
            '{} is connected'.format(client.user)
        )

    @client.event
    async def on_message(message):
        if message.author == client.user:
            # This was a bot message
            return
        m = commandre.search(message.content)
        if m is None:
            # This is not a command
            return
        try:
            await processCommand(m.group(1),m.group(2),message.author,message.channel)
        except Exception as e:
            channel = message.channel
            await channel.send('{}\n\nSee "bot_instructions" channel for help.'.format(str(e)))
            if DEBUGGING:
                # This causes the stack to be printed but does not interrupt execution
                raise e
    #######
    # Run #
    #######
    client.run(TOKEN)

