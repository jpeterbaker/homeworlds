# Tool for interaction between a Discord channel and the game state, game history, and timer

from discord import File
import chessClock as cc
from asyncio import sleep
from sys import path
path.append('hwlogic/')
from draw import drawState
from buildState import HWState,buildState
from text2turn import applyTextTurn as att
from os import path as ospath

imgSaveDir = ospath.join(ospath.dirname(__file__), 'stateImages/')

maxTime = cc.timedelta(hours=6)
defaultTime = cc.timedelta(minutes=45)
maxPlayers = 2

class InvalidTimerIteraction(Exception):
    pass

class GameMaster:
    def __init__(self,channel,admin):
        self.channel = channel
        self.state = None
        self.admin = admin
        self.reset()

    def reset(self):
        # Start over, except don't throw away the state
        self.clock = None
        self.inProgress = False
        self.history = []

        # map registration number requests to user,time-allocation pairs
        # registration numbers don't  have to be 0,1 or 1,2
        self.reg2userTimePair = {}
        # map users to their registration
        # later, registration number will be replaced with index of player order
        self.player2reg = {}

        self.timerMessage = None
        self.names = None

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

    def getHistStr(self):
        if len(self.history) == 0:
            return 'NO MOVES WERE MADE'
        x = []
        playernames = [self.reg2userTimePair[k][0].name for k in range(2)]
        for i in range(len(self.history)):
            x.append('{} {}.\n{}\n'.format(playernames[i%2],i//2+1,self.history[i]))
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
        await self.showState()
        await self.startup(message)
        self.state = state # This needs to be done again because a new state is created by startup
        self.clock.onmove = state.onmove
        await self.loopUpdate()

    async def showState(self):
        fname = ospath.join(imgSaveDir,'{}.png'.format(self.channel.id))
        drawState(self.state,fname)
        # Upload the image
        with open(fname,'rb') as fin:
            df = File(fin)
            await self.channel.send('',file=df)

    def nPlayers(self):
        return len(self.player2reg)

    async def unregister(self,message):
        user = message.author
        reg = self.player2reg.pop(user)
        self.reg2userTimePair.pop(reg)
        await self.channel.send('{} removed from game.'.format(user.name))

    async def register(self,message):
        # Add a user as player i in a game with time bank dt (number of seconds)
        # i does not need to be an int, only comparable with all other registrations
        if self.inProgress:
            raise InvalidTimerIteraction('Users cannot be added after game has started.')

        # Throw away the exclamation point
        words = message.content[1:].split()
        n = len(words)
        if n == 1:
            i = None
            dt = None
        elif n == 3:
            i = int(words[1])
            dt = int(words[2])
        else:
            await self.channel.send('Wrong number of arguments.\nSee "bot_instructions" channel for help.')
            return
        
        if dt is None:
            await self.channel.send('Using default time bank of {} seconds.'.format(
                int(defaultTime.total_seconds())
            ))
            dt = defaultTime
        else:
            dt = cc.timedelta(seconds=dt)

        if dt > maxTime:
            raise InvalidTimerIteraction('Maximum time for a player is {} seconds.'.format(
                int(maxTime.total_seconds())
            ))

        user = message.author

        if user in self.player2reg:
            # Same user, new number
            oldi = self.player2reg[user]
            await self.channel.send('{} was player {}.'.format(
                user.name,oldi
            ))
            self.player2reg.pop(user)
            self.reg2userTimePair.pop(oldi)

        if i is None:
            if self.nPlayers() == 0:
                i = 0
            else:
                i = max(self.reg2userTimePair)+1

        if i in self.reg2userTimePair:
            # Same number, new user
            other = self.reg2userTimePair[i][0]
            await self.channel.send('{} will replace {} as player {}.'.format(
                user.name,other.name,i
            ))
            self.player2reg.pop(other)
            self.reg2userTimePair.pop(i)

        if self.nPlayers() >= maxPlayers:
            raise InvalidTimerIteraction('Registration cancelled: max players reached.')
        await self.channel.send('Successfully registered {} as player {}.'.format(user.name,i))

        self.reg2userTimePair[i] = (user,dt)
        self.player2reg[user] = i

    async def startup(self,message):
        # Begin a new game, but don't run the loop
        if self.nPlayers() < 2:
            raise Exception('Two players need to register before game can start.')
        user = message.author
        self.confirmPlayer(user)
        self.inProgress = True

        reglist = list(self.reg2userTimePair)
        reglist.sort()
        self.clock = cc.ChessClock([self.reg2userTimePair[key][1] for key in reglist])
        self.names = [self.reg2userTimePair[key][0].name for key in reglist]

        newreg2pair = {}
        # Replace registration numbers (which could be 1,2 for example)
        # With player numbers 0,1
        for i in range(len(reglist)):
            oldreg = reglist[i]
            # User,time tuple
            pair = self.reg2userTimePair[oldreg]
            self.player2reg[pair[0]] = i
            newreg2pair[i] = pair
        self.reg2userTimePair = newreg2pair
        t = cc.datetime.utcnow()
        self.clock.unpause(t)
        self.state = HWState()
        await self.sendTimerMessage()

    async def begin(self,message):
        # Start with the players we have
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

        await self.showState()

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
        user = message.author
        self.confirmPlayer(user)
        if self.player2reg[user] != self.clock.onmove and user.id != self.admin:
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
        if not user in self.player2reg and not user.id == self.admin:
            raise InvalidTimerIteraction('Only players may interact with the timer.')

    async def stop(self,message):
        user = message.author
        if self.inProgress:
            self.confirmPlayer(user)
            report = self.getHistStr()
            await self.channel.send('{}\nGame was cancelled by {}.'.format(report,user.name))
            await self.channel.send('If you would like to continue this game later, you can re-register and then provide the game state to the !resume command as printed below.\n\n!resume {}'.format(self.state.buildStr()))
        elif len(self.player2reg) > 0:
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

    ######################
    # Registration tests #
    ######################
    p0 = TestUser('Billy')
    p1 = TestUser('Bob')
    p2 = TestUser('Alice')
    master = GameMaster(None)
    master.register(p0,4)
    master.register(p0,0,10)
    master.register(p1,0,10)
    master.register(p2,1,10)
    try:
        master.register(p0,2,10)
        print('FAILED')
    except InvalidTimerIteraction as e:
        print(e)
    master.register(p0,0,10)
    master.register(p1,1,10)
    print(master)
    try:
        master.register(p0,0,10000000)
        print('\n\nFAILED\n\n')
    except InvalidTimerIteraction as e:
        print(e)

    ###############
    # Clock tests #
    ###############

