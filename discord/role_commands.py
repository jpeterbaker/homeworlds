from discord.utils import get
from asyncio import sleep

def get_delay(s):
    if len(s) == 2:
        return 4.0
    return float(s[2:])

async def command_out(message):
    author = message.author
    await member_role_set(author,'Seeking opponent',False)
    await message.channel.send(
        '{} is no longer seeking an opponent.'.format(
            author.mention,
        )
    )
async def command_in(message):
    # User wants to join @Seeking opponent
    try:
        hours = get_delay(message.content)
    except ValueError:
        # They said something that wasn't a number, so ignore it
        return
    if hours <= 0 or hours > 24:
        await channel.send('Time parameter must be between 0 and 24 (hours)')
        return
    author = message.author
    channel = message.channel
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

async def member_role_set(member,role_name,value):
    guild = member.guild
    role = get(guild.roles,name=role_name)
    if value:
        await member.add_roles(role)
    else:
        await member.remove_roles(role)
    return role

async def emoji_role_open(guild,emoji_name):
    # Make emoji unrestricted
    emoji = get(guild.emojis,name=emoji_name)
    await emoji.edit(roles=[])

async def emoji_role_set(guild,emoji_name,role_name):
    # Make emoji useable only by this role
    emoji = get(guild.emojis,name=emoji_name)
    roles = [get(guild.roles,name=role_name)]
    await emoji.edit(roles=roles)

async def emoji_role_change(guild,emoji_name,role_name,value):
    # Let the role use the emoji if value is True
    # Disallow if value is False
    emoji = get(guild.emojis,name=emoji_name)
    if len(emoji.roles) == 0:
        # Emoji is already universal, do nothing
        return
    role = get(guild.roles,name=role_name)
    roles = [r for r in emoji.roles if r != role]
    if value:
        roles.append(role)
    await emoji.edit(roles=roles)

