#!/usr/bin/python3.7
# A bot that makes simple observations about who sends chat messages
# and the elapsed time between the same user sending two consecutive messages

import discord

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

lastMessage = [None]
lastTime = [None]

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author == lastSpeaker[0]:
        await message.channel.send('You sent two messages in a row')
        await message.channel.send('Time between messages: {}'.format(message.created_at-lastTime[0]))
        lastTime[0] = message.created_at
    else:
        lastSpeaker[0] = message.author
        lastTime[0] = message.created_at
        await message.channel.send('New speaker')


client.run(TOKEN)
