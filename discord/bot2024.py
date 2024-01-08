'''
The commands "in' and "out" will add/remove the role named "Seeking opponent"
if given in a channel named "looking_for_opponent"

The user with ID given in private/adminID/txt can set emoji permissions
with the command
    set emoji role <emoji name> <role name>
I haven't made a way to make the emoji usable by multiple roles yet
(note that role names may have spaces)
'''
from sys import path,argv

import discord
from discord.utils import get
from discord.ext import commands

import re
from random import uniform
from asyncio import sleep

patmoji = re.compile('set emoji role ([^ ]+) (.+)')

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

intents = discord.Intents.all()

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)

######################
# Responses to event #
######################
@client.event
async def on_ready():
#    guild = discord.utils.get(client.guilds,id=GUILD)
    print(
        '{} is connected'.format(client.user)
    )

async def member_role_set(member,role_name,value):
    guild = member.guild
    role = get(guild.roles,name=role_name)
    if value:
        await member.add_roles(role)
    else:
        await member.remove_roles(role)
    return role

async def emoji_role_set(guild,emoji_name,role_names):
    emoji = get(guild.emojis,name=emoji_name)
    roles = [get(guild.roles,name=role_name) for role_name in role_names]
    await emoji.edit(roles=roles)

def get_delay(mlow):
    if len(mlow) == 2:
        return 4.0
    return float(mlow[2:])

def sample(x):
    # Get a random member of x
    return x[int(uniform(0,len(x)))]

greets = ["What's up!","How's it going!","Howdy!"]
signatures = [
    "I may be a bot, but this message was crafted with love.",
    "I was able to greet you so fast because I'm a bot. A human should acknowledge your arrival soon.",
    "I'm a bot with only a few programmed responses, so I'm afraid I can't answer questions myself."
]
invitation_template = '''
Feel free to introduce yourself, ask questions, or just look around.

The {} channel is a good place for self-service Homeworlds info.'''

async def greet(member,channel):
    # Send a random greeting
    guild = member.guild
    resources_channel = get(guild.channels,name='resources')

    greeting = sample(greets)
    invitation = invitation_template.format(resources_channel.mention)
    signature = sample(signatures)
    await channel.send(
        '{} {} {}\n\n{}'.format(
            member.mention,
            greeting,
            invitation,
            signature
        )
    )

@client.event
async def on_member_join(member):
    general_channel = get(member.guild.channels,name='general')
    await greet(member,general_channel)

@client.event
async def on_message(message):
    author = message.author
    if author == client.user:
        # This was a bot message
        return
    channel = message.channel
    if message.content == 'greet me':
        await greet(author,channel)
        return
    if channel.name == 'looking_for_opponent':
        mlow = message.content.lower()
        if mlow == 'out':
            # User wants to leave @Seeking opponent
            await member_role_set(author,'Seeking opponent',False)
            await channel.send(
                '{} is no longer seeking an opponent.'.format(
                    author.mention,
                )
            )
            return
        elif mlow.startswith('in'):
            # User wants to join @Seeking opponent
            try:
                hours = get_delay(mlow)
            except ValueError:
                # They said something that wasn't a number, so ignore it
                return
            if hours <= 0 or hours > 24:
                await channel.send('Time parameter must be between 0 and 24 (hours)')
                return
            role = await member_role_set(author,'Seeking opponent',True)
            seekers = [m for m in role.members if m != author]
            if len(seekers) == 0:
                seeker_note = 'No one else is currently looking.'
            else:
                seeker_note = 'All opponent seekers:\n{}'.format(
                    '\n'.join([m.mention for m in seekers])
                )
            await channel.send(
                'For the next {} hours, {} is {}\n\n{}'.format(
                    hours,
                    author.mention,
                    role.mention,
                    seeker_note
                )
            )
            await sleep(3600*hours)
            # Check if they are still seeking opponent
            r = get(author.roles,name='Seeking opponent')
            if r is None:
                # They no longer have the role and must have canceled early
                return
            role = await member_role_set(author,'Seeking opponent',False)
            await channel.send(
                'Time expired. {} is no longer seeking an opponent.'.format(
                    author.mention,
                )
            )
        return
    if author.id == ADMIN and message.content.lower().startswith('set'):
        mat = patmoji.search(message.content)
        if mat is None:
            return
        gs = mat.groups()
        emoji_name = gs[0]
        role_names = [gs[1]]
        await emoji_role_set(author.guild,emoji_name,role_names)
        await channel.send('Emoji permission updated')

#######
# Run #
#######
client.run(TOKEN)

