#!/usr/bin/python3.7
from datetime import datetime
import discord
from asyncio import sleep

with open('token.txt','r') as fin:
    TOKEN = fin.readline().strip()

with open('guildID.txt','r') as fin:
    GUILD = int(fin.readline().strip())

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds,id=GUILD)
    print(
        f'{client.user} is connected guild "{guild.name}"'
    )

timer = [None]
timerMessage = [None]
keepGoing = [False]

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print('Message received:',message.content)
    if message.content == '!go' and not keepGoing[0]:
        print('Beginning timer')
        keepGoing[0] = True
        timerMessage[0] = await message.channel.send('0')
        timer[0] = message.created_at
        while keepGoing[0]:
            await sleep(1)
            await timerMessage[0].edit(content=str(datetime.utcnow()-timer[0]))
    if message.content == '!stop' and keepGoing[0]:
        print('Stopping timer')
        keepGoing[0] = False

client.run(TOKEN)
