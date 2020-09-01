#!/usr/bin/python3.7
# Very simple chess clock bot
# Does not control which user or channel gives commands
import chessClock as cc
import discord
from asyncio import sleep

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

cclock = cc.ChessClock([cc.timedelta(seconds=0)]*2)
timerMessage = [None]

async def processCommand(message):
    t = cc.datetime.utcnow()
    startloop = False
    if message.content == '!':
        # Main button: change the player on move
        cclock.addPly(t)
    elif message.content.startswith('!begin'):
        # Get the command argument
        try:
            x = int(message.content[6:])
            print('starting with',x)
        except:
            await message.channel.send('Usage "!begin x" to start a timer with x seconds')
        cclock.__init__([cc.timedelta(seconds=x)]*2)
    elif message.content == '!unpause' or message.content == '!!' and cclock.paused:
        startloop = True
        cclock.unpause(t)
    elif message.content == '!pause' or message.content == '!!' and not cclock.paused:
        # Pause the timer
        cclock.pause(t)

    # Delete old message if any and send a fresh one
    if timerMessage[0] is not None:
        await timerMessage[0].delete()
    timerMessage[0] = await message.channel.send(cclock.strAt(t))

    # Start the main loop
    if startloop:
        while not cclock.paused and not cclock.expired:
            # Main timing loop
            t = cc.datetime.utcnow()
            cclock.getTimes(t)
            try:
                await timerMessage[0].edit(content=cclock.strAt(t))
            except Exception:
                print('An exception: probably unfortunate timing on message deletion')
            await sleep(1)
        if cclock.expired:
            # Game is over, so don't delete the old message anymore
            timerMessage[0] = None

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[0] != '!':
        return
    try:
        await processCommand(message)
    except cc.ChessClockException as e:
        # Send any clock errors as messages
        await message.channel.send(str(e))

client.run(TOKEN)
