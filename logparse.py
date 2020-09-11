#!/usr/bin/python3.7
# Look through a Discord chat and convert to a game
# THIS SCRIPT WILL HANG because of the main timer loop in gameMaster
# You just need to have the loopUpdate function return immediately
# This prevents the script from finding problems with the loop

from hwModBot import re,processCommand,GameMaster,channel2master
from asyncio import get_event_loop
import traceback

# example chat messages
'''
[3:06 PM] Babamots: !register

[3:32 PM] Babamots: !s g3 babamots
build b2 safety
build b3 safety
build b3 Risa

'''

# Group 1: name (e.g. "Babamots")
# Group 2: command (e.g. "build")
# Group 3: params (e.g. "g1 Bajor")
messagere = re.compile(r'(?sm)M] (\w+): \s*!\s*(\w+)\s*?(.*?)\n\[\d')

class MyMessage:
    async def edit(*args,**kwargs):
        pass
    async def delete(*args,**kwargs):
        pass

message = MyMessage()

class MyChannel:
    def __init__(self):
        self.id = 7
    async def send(self,s,**kwargs):
        print('Bot:\n{}\n'.format(s))
        return message
    def __hash__(self):
        return 0
    def __eq__(self,other):
        return True

class MyUser:
    def __init__(self,name,id):
        self.name = name
        self.id = id
    def __eq__(self,other):
        return self.id == other.id
    def __hash__(self):
        return self.id

# Dump file into a single str
with open('private/bugGame.txt','r') as fin:
    log = '\n'.join([line for line in fin])

channel = MyChannel()
master = GameMaster(channel,None)
channel2master[channel] = master

name2user = {}

async def parseFile():
    for match in messagere.finditer(log):
        name = match.group(1)
        command = match.group(2)
        params = match.group(3).strip()
        if not name in name2user:
            name2user[name] = MyUser(name,len(name2user))
        user = name2user[name]
        print('{}:\n!{} {}'.format(name,command,params))
        try:
            await processCommand(command,params,user,channel)
        except Exception as e:
            print('A promblem came to the outside.')
            print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))

loop = get_event_loop()
loop.run_until_complete(parseFile())
loop.close()
