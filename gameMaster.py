# Tool for interaction between a Discord channel and the game state, game history, and timer

from discord import File
import chessClock as cc
from asyncio import sleep
from sys import path
path.append('hwlogic/')
from drawH import drawState
from buildState import HWState,buildState
import text2turn as t2t
from os import path as ospath
from numpy.random import randint

imgSaveDir = ospath.join(ospath.dirname(__file__), 'stateImages/')

maxPlayers = 2

maxTime = cc.timedelta(hours=6)
defaultTime = cc.timedelta(minutes=45)
defaultInc = cc.timedelta(seconds=30)

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
        # Start over except don't throw away the state
        self.clock = None
        self.clockType = cc.ChessClock
        self.inProgress = False
        self.history = []

        # Game clocks as they were when turns were completed (in case players undo)
        self.pastClocks = []

        # map players to their initial time bank in the form of a tuple for clock constructor
        self.player2time = {}
        # players in their play order
        self.players = [None]*2

        self.timerMessage = None

    def nPlayers(self):
        return len(self.player2time)

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
        await self.channel.send('Successfully registered {} as player {} with default time bank {}:{:02}.\nUse "!time <minutes>:<seconds>" for different timer setting.'.format(user.name,pos,sec//60,sec%60))

        self.players[pos] = user
        self.player2time[user] = [defaultTime]
        if self.clockType == cc.FischerClock:
            await self.channel.send('You have the default Fischer incrementation of {} seconds. Use "!fischer <seconds>" to modify.'.format(int(defaultInc.total_seconds())))
            self.player2time[user].append(defaultInc)

    async def unregister(self,user):
        if self.inProgress:
            await self.channel.send('Game is in progress. Use "!stop" to cancel.')
            return
        self.player2time.pop(user)
        self.players[self.players.index(user)] = None
        await self.channel.send('{} removed from game.'.format(user.name))

    async def cancel(self,user):
        if self.nPlayers() > 0:
            self.confirmPlayer(user)
            await self.channel.send('Game setup cancelled. Clearing registration.')
        else:
            await self.channel.send('No game running, no users registered.')
        self.reset()

    async def setTime(self,user,sec):
        '''
        sec: integer number of seconds to start with
        '''
        if not user in self.player2time:
            await self.channel.send('You need to register before you can set your time bank.')
            return
        dt = cc.timedelta(seconds=sec)
        self.player2time[user][0] = dt
        await self.channel.send('\n'.join([
            '{} has a time bank of {}.'.format(
                p.name,
                cc.sec2str(self.player2time[p][0].total_seconds()),
            ) for p in self.players if p is not None])
        )

    async def begin(self,user,random=False):
        # Start with the players we have
        if random and randint(2):
            #Switch play order
            self.players = self.players[::-1]
            
        self.state = HWState()
        await self.startup(user)
        await self.loopUpdate()

    async def startup(self,user):
        # Begin a new game, but don't run the loop
        if self.nPlayers() < 2:
            raise Exception('Two players need to register before game can start.')
        self.confirmPlayer(user)
        self.inProgress = True

        params = list(zip(*[self.player2time[p] for p in self.players]))
        self.clock = self.clockType(*params)
        self.names = [p.name for p in self.players]

        t = cc.datetime.utcnow()
        self.clock.unpause(t)
        await showState(self.state,self.channel)
        await self.sendTimerMessage()

    async def setTimerStyle(self,user,style,special=None):
        self.confirmPlayer(user)
        if style == 'f':
            if special is None:
                await self.channel.send('Using default Fischer incrementation of {} seconds. Use "!fischer <seconds>" to modify.'.format(int(defaultInc.total_seconds())))
                inc = defaultInc
            else:
                inc = cc.timedelta(seconds=int(special))
            if self.clockType == cc.FischerClock:
                # The clock type has not changed, just change increment of the player who typed the command
                self.player2time[user][1] = inc
                await self.channel.send('Fischer timer was already selected. Incrementation will be modified.')
            else:
                # Append increment to the time list associated with each player
                # Set all players to have the same increment
                self.clockType = cc.FischerClock
                for p in self.players:
                    if p is None:
                        continue
                    self.player2time[p].append(inc)
            await self.channel.send('\n'.join([
                '{} has a time bank of {} seconds, incremented by {} seconds each turn.'.format(
                    p.name,
                    int(self.player2time[p][0].total_seconds()),
                    int(self.player2time[p][1].total_seconds()),
                ) for p in self.players if p is not None])
            )
        else:
            if self.clockType == cc.FischerClock:
            # We're switching away from Fischer, remove the increment
                for p in self.players:
                    if p is not None:
                        self.player2time[p].pop()
        if style == 'h':
            if self.clockType == cc.HourGlass:
                await self.channel.send('Hourglass timer was already selected. Nothing has changed.')
            else:
                self.clockType = cc.HourGlass
                await self.channel.send('Now using hourglass timer.')
        elif style == 's':
            if self.clockType == cc.ChessClock:
                await self.channel.send('Standard-style timer was already selected. Nothing has changed.')
            else:
                self.clockType = cc.ChessClock
                await self.channel.send('Now using standard-style timer.')

    async def resume(self,user,statestr):
        # Resume command was issued
        if self.inProgress:
            await self.channel.send('Stop the game in progress before resuming a different one.')
            return
        self.confirmPlayer(user)
        try:
            self.state = buildState(statestr)
        except Exception as e:
            raise Exception('There was a problem processing your state string.')
        await self.startup(user)
        self.clock.onmove = state.onmove
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

    async def addTurn(self,user,cmd):
        # Process the command
        self.confirmTurn(user)
        if cmd[0] == 'h':
            # Yes, this is kind of a sloppy way to do this
            # It's a homeworld creation:
            # append user name so that text2turn knows what to call the system
            cmd = '{} {}'.format(cmd,user.name)
        turn = t2t.applyTextTurn(cmd,self.state)
        self.history.append(turn)

        t = cc.datetime.utcnow()
        self.pastClocks.append(self.clock.copy())
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

    async def undo(self,user):
        # Check that undoing is valid
        if not self.inProgress:
            raise InvalidTimerIteraction('Game is not in progress.')
        if self.clock.paused:
            raise cc.ChessClockException('Game is paused.')
        self.confirmPlayer(user)
        if self.players[self.clock.onmove] == user:
            raise InvalidTimerIteraction('You can only undo after your own turn.')
        if len(self.history) == 0:
            raise Exception('Cannot undo before making a move')

        turn = self.history.pop()
        turn.undoAll()
        self.state.advanceOnmove(-1)

        t = cc.datetime.utcnow()
        # Any past pauses will have already taken time from the opponent's bank
        # take away the time since the last pause and then give it all back
        self.clock = self.pastClocks.pop()

        await showState(self.state,self.channel)
        await self.sendTimerMessage()

    def confirmTurn(self,user):
        # Raise an exception if player may not move
        if not self.inProgress:
            raise InvalidTimerIteraction('Game is not in progress.')
        if self.clock.paused:
            raise cc.ChessClockException('Game is paused.')
        self.confirmPlayer(user)
        if self.players[self.state.onmove] != user:
            raise InvalidTimerIteraction('It is not your turn.')

    async def togglePause(self,user):
        if not self.inProgress:
            raise InvalidTimerIteraction('Game is not in progress.')
        if self.clock.paused:
            await self.unpause(user)
        else:
            await self.pause(user)

    async def pause(self,user):
        if not self.inProgress:
            raise InvalidTimerIteraction('Game is not in progress.')
        self.confirmPlayer(user)
        t = cc.datetime.utcnow()

        self.clock.pause(t)
        await self.sendTimerMessage()

    async def unpause(self,user):
        if not self.inProgress:
            raise InvalidTimerIteraction('Game is not in progress.')
        self.confirmPlayer(user)
        t = cc.datetime.utcnow()
        self.clock.unpause(t)

        await self.sendTimerMessage()
        await self.loopUpdate()
        
    async def stop(self,user):
        self.confirmPlayer(user)
        if not self.inProgress:
            await self.channel.send('Game has not started. Use "!cancel" to cancel all registrations.')
            return
        report = self.getHistStr()
        await self.channel.send('{}\nGame was cancelled by {}.'.format(report,user.name))
        await self.sendBuildStr()
        self.reset()

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
            x.append('{} {}.\n{}\n'.format(self.names[i%2],i//2+1,str(self.history[i])))
        return '\n'.join(x)

    def confirmPlayer(self,user):
        if not user in self.player2time and not user.id == self.admin:
            raise InvalidTimerIteraction('Only players may give commands.')

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

