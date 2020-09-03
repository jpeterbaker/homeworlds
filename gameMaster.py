# Tool for interaction between a Discord channel and the game state, game history, and timer

from discord import File
import chessClock as cc
from asyncio import sleep
from sys import path
path.append('hwlogic/')
from drawH import drawState
from buildState import HWState,buildState
from text2turn import applyTextTurn as att
from os import path as ospath
from numpy.random import randint

imgSaveDir = ospath.join(ospath.dirname(__file__), 'stateImages/')

maxPlayers = 2

maxTime = cc.timedelta(hours=6)
defaultTime = cc.timedelta(minutes=45)

class InvalidTimerIteraction(Exception):
    pass

async def showState(state,channel):
    fname = ospath.join(imgSaveDir,'{}.png'.format(channel.id))
    drawState(state,fname)
    # Upload the image
    with open(fname,'rb') as fin:
        df = File(fin)
        await channel.send('',file=df)

class GameMaster:
    def __init__(self,channel,admin):
        # admin is an int: user with this id may interact with timer while out of game
        self.channel = channel
        self.state = None
        self.admin = admin
        self.reset()

    def reset(self):
        # Start over, except don't throw away the state
        self.clock = None
        self.inProgress = False
        self.history = []

        # map players to their initial time bank
        self.player2time = {}
        # players in their play order
        self.players = [None]*2

        self.timerMessage = None

    async def sendReport(self):
        s = '{}\n{}'
        if self.clock.expired:
            result = '{} ran out of time.'.format(self.names[self.clock.getLoser()])
        elif self.state.isEnd():
            scores = self.state.getScores()
            try:
                winner = scores.index(1)
                result = '{} won.'.format(self.names[winner])
            except ValueError:
                result = 'The game was a draw.'
        await self.channel.send(s.format(self.getHistStr(),result))

    async def sendBuildStr(self):
        await self.channel.send('If you would like to continue this game later, you can re-register and then provide the game state to the !resume command as printed below.\n\n!resume {}'.format(self.state.buildStr()))

    def getHistStr(self):
        if len(self.history) == 0:
            return 'NO MOVES WERE MADE'
        x = []
        for i in range(len(self.history)):
            x.append('{} {}.\n{}\n'.format(self.names[i%2],i//2+1,self.history[i]))
        return '\n'.join(x)

    async def resume(self,message):
        # Resume command was issued
        if self.inProgress:
            raise Exception('Stop the game in progress before resuming a different one.')
        # Skip the "!resume"
        statestr = message.content[7:]
        try:
            state = buildState(statestr)
        except Exception as e:
            await self.channel.send('There was a problem processing your state string.')
            raise e
        self.state = state
        await showState(self.state,self.channel)
        await self.startup(message)
        self.state = state # This needs to be done again because a new state is created by startup
        self.clock.onmove = state.onmove
        await self.loopUpdate()

    def nPlayers(self):
        return len(self.player2time)

    async def unregister(self,user):
        if self.inProgress:
            await self.channel.send('Game is in progress. Use "!stop" to cancel.')
            return
        self.player2time.pop(user)
        self.players[self.players.index(user)] = None
        await self.channel.send('{} removed from game.'.format(user.name))

    async def register(self,user,pos=None):
        # Add a user as player number pos
        if self.inProgress:
            raise InvalidTimerIteraction('Users cannot be added after game has started.')

        if user in self.player2time:
            # Same user, new number
            await self.channel.send('{} was already registered.\n"!unregister" and then "!register [n]" to choose a different play order.'.format(user.name))
            return

        if pos is None:
            for i in range(2):
                if self.players[i] is None:
                    pos = i
                    break
            else:
                # Loop exited normally
                await self.channel.send('Registration cancelled: already at max players.')
                return

        if self.players[pos] is not None:
                await self.channel.send('Registration cancelled: {} is already player {}.'.format(self.players[pos].name,pos))
                return
        sec = int(defaultTime.total_seconds())
        await self.channel.send('Successfully registered {} as player {} with default time bank {}:{:02}.\nUse "!time minutes:seconds" for different timer setting.'.format(user.name,pos,sec//60,sec%60))

        self.players[pos] = user
        self.player2time[user] = defaultTime

    async def setTime(self,user,m,s):
        if not user in self.player2time:
            await self.channel.send('You need to register before you can set your time bank.')
            return
        sec = 60*m+s
        dt=cc.timedelta(seconds=sec)
        await self.channel.send('Set time bank of {} to {}:{:02}'.format(user.name,m,s))
        self.player2time[user] = dt

    async def startup(self,message):
        # Begin a new game, but don't run the loop
        if self.nPlayers() < 2:
            raise Exception('Two players need to register before game can start.')
        user = message.author
        self.confirmPlayer(user)
        self.inProgress = True

        self.clock = cc.ChessClock([self.player2time[p] for p in self.players])
        self.names = [p.name for p in self.players]

        t = cc.datetime.utcnow()
        self.clock.unpause(t)
        self.state = HWState()
        await self.sendTimerMessage()

    async def begin(self,message,random=False):
        # Start with the players we have
        if random and randint(2):
            #Switch play order
            self.players = self.players[::-1]
            
        await self.startup(message)
        await self.loopUpdate()

    async def loopUpdate(self):
        # Start main loop
        while self.inProgress and not self.clock.paused and not self.clock.expired:
            # Main timing loop
            t = cc.datetime.utcnow()
            try:
                await self.timerMessage.edit(content=self.strAt(t))
            except Exception as e:
                # Hopefully, no further checks are needed here
                # The message has sometimes been deleted because of commands,
                # but I don't anticipate other exceptions happening
                pass
            await sleep(1)
        if self.clock is not None and self.clock.expired:
            # Game is over, so don't delete the old message anymore
            await self.sendReport()
            await self.sendBuildStr()
            self.reset()

    async def sendTimerMessage(self):
        # Move timer message to the bottom of chat
        # Use this after most commands
        if self.timerMessage is not None:
            await self.timerMessage.delete()
        t = cc.datetime.utcnow()
        self.timerMessage = await self.channel.send(self.strAt(t))

    def strAt(self,t):
        return self.clock.strAt(t,self.names)

    async def addTurn(self,message):
        # Process the command
        # The move command
        self.confirmTurn(message)
        cmd = message.content[1:].strip()
        if cmd[0] == 'h':
            # Yes, this is kind of a sloppy way to do this
            # It's a homeworld creation:
            # append user name so that text2turn knows what to call the system
            cmd = '{} {}'.format(cmd,message.author.name)
        turn = att(cmd,self.state)
        self.history.append(str(turn))
        t = cc.datetime.utcnow()
        self.clock.addPly(t)

        await showState(self.state,self.channel)

        if self.state.isEnd():
            await self.sendReport()
            self.reset()
            return
            
        await self.sendTimerMessage()

    def cancelTurn(self):
        if self.state is not None:
            self.state.cancelTurn()

    def confirmTurn(self,message):
        # Raise an exception if player may not move
        if not self.inProgress:
            raise InvalidTimerIteraction('Game is not in progress.')
        if self.clock.paused:
            raise cc.ChessClockException('Game is paused.')
        user = message.author
        self.confirmPlayer(user)
        if self.players[self.clock.onmove] != user:
            raise InvalidTimerIteraction('It is not your turn.')

    async def togglePause(self,message):
        if not self.inProgress:
            raise InvalidTimerIteraction('Game is not in progress.')
        if self.clock.paused:
            await self.unpause(message)
        else:
            await self.pause(message)

    async def pause(self,message):
        if not self.inProgress:
            raise InvalidTimerIteraction('Game is not in progress.')
        user = message.author
        self.confirmPlayer(user)
        t = cc.datetime.utcnow()
        self.clock.pause(t)
        await self.sendTimerMessage()

    async def unpause(self,message):
        if not self.inProgress:
            raise InvalidTimerIteraction('Game is not in progress.')
        user = message.author
        self.confirmPlayer(user)
        t = cc.datetime.utcnow()
        self.clock.unpause(t)

        await self.sendTimerMessage()
        await self.loopUpdate()
        
    def confirmPlayer(self,user):
        if not user in self.player2time and not user.id == self.admin:
            raise InvalidTimerIteraction('Only players may interact with the timer.')

    async def stop(self,message):
        user = message.author
        if self.inProgress:
            self.confirmPlayer(user)
            report = self.getHistStr()
            await self.channel.send('{}\nGame was cancelled by {}.'.format(report,user.name))
            await self.sendBuildStr()
        elif self.nPlayers() > 0:
            self.confirmPlayer(user)
            await self.channel.send('Game setup cancelled. Clearing registration.')
        else:
            await self.channel.send('No game running, no users registered.')
        self.reset()

if __name__=='__main__':
    class TestMessage:
        def __init__(self,user,t):
            self.user = user
            self.created_at = t
    class TestUser:
        def __init__(self,name):
            self.name = name
        def __str__(self):
            return self.name
        def __repr__(self):
            return str(self)

