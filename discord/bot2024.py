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
from time_detection import get_time

import discord
from discord.utils import get
import re
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

client = discord.Client(intents=discord.Intents.all())

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

@client.event
async def on_message(message):
    author = message.author
    if author == client.user:
        # This was a bot message
        return
    channel = message.channel
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


