'''
The commands "in' and "out" will add/remove the role named "Seeking opponent"
if given in a channel named "looking_for_opponent"

The user with ID given in private/adminID.txt can give or take emoji permissions
to a role with the commands
    open <emoji name>
        Make emoji unrestricted
    set <emoji name> <role name>
        Make emoji usable ONLY by the given role
    give <emoji name> <role name>
        Add the given role to those who can use the emoji
    take <emoji name> <role name>
        Remove emoji permission from the given role
Note that <role name> may have spaces
'''
from sys import argv

import discord
from discord.utils import get

import re
from random import uniform

import role_commands as rc

patmoji = re.compile('(set|give|take|open) ([^ ]+) *(.+)?')

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

#############
# Utilities #
#############

def sample(x):
    # Get a random member of x
    return x[int(uniform(0,len(x)))]


######################
# Responses to event #
######################
@client.event
async def on_ready():
#    guild = discord.utils.get(client.guilds,id=GUILD)
    print(
        '{} is connected'.format(client.user)
    )

greets = ["What's up!","How's it going!","Howdy!","Welcome!"]
signatures = [
    "Although I am an emotionless bot, this form letter was human-written with love.",
    "I was able to greet you so fast because I'm a bot. A human should acknowledge your arrival soon.",
    "I'm a bot with only a few programmed behaviors, so I'll have to leave any question-answering to the humans."
]
invitation_template = '''
Feel free to introduce yourself, ask questions, or just look around.

The {} channel is a good place for self-service Homeworlds info.'''

async def greet(member,channel):
    # Send a random greeting
    resources_channel = get(member.guild.channels,name='resources')

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

############
# Commands #
############

@client.event
async def on_message(message):
    author = message.author
    if author == client.user:
        # This was a bot message
        return
    text = message.content
    if message.channel.name == 'looking_for_opponent':
        if text == 'out':
            # User wants to leave @Seeking opponent
            await rc.command_out(message)
            return
        elif text.startswith('in'):
            await rc.command_in(message)
            return
    if author.id == ADMIN:
        mat = patmoji.search(message.content)
        if mat is None:
            return
        gs = mat.groups()
        cmd = gs[0]
        emoji_name = gs[1]
        role_name = gs[2]
        if cmd == 'open':
            await rc.emoji_role_open(author.guild,emoji_name)
        elif cmd == 'set':
            await rc.emoji_role_set(author.guild,emoji_name,role_name)
        elif cmd == 'give':
            await rc.emoji_role_change(author.guild,emoji_name,role_name,True)
        elif cmd == 'take':
            await rc.emoji_role_change(author.guild,emoji_name,role_name,False)
        else:
            raise Exception('Unknown emoji role command')

        emoji = get(author.guild.emojis,name=emoji_name)
        if len(emoji.roles) == 0:
            role_list = 'Everyone'
        else:
            role_list = '\n'.join([r.name for r in emoji.roles])
        await message.channel.send('Emoji now useable by:\n{}'.format(
            role_list
        ))

#######
# Run #
#######
client.run(TOKEN)

