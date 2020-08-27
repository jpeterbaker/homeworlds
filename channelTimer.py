
import chessClock as cc
from asyncio import sleep

maxTime = cc.timedelta(hours=6)
defaultTime = cc.timedelta(minutes=45)
maxPlayers = 2

class InvalidTimerIteraction(Exception):
    pass

class ChannelTimer:
    def __init__(self,channel):
        # Keep track of the state of players' interactions with a ChessClock on a Discord channel
        self.channel = channel
        self.timerMessage = None
        # map registration number requests to user,time-allocation pairs
        # registration numbers don't  have to be 0,1 or 1,2
        self.reg2userTimePair = {}
        # map users to their registration
        # later, registration number will be replaced with index on clock player order
        self.player2reg = {}
        self.clock = None
        self.timing = False
        self.names = None

    def getNusers(self):
        return len(self.player2reg)

    async def register(self,user,i=None,dt=None):
        # Add a user as player i in a game with time bank dt (number of seconds)
        # i does not need to be an int, only comparable with all other registrations
        if self.timing:
            raise InvalidTimerIteraction('Users cannot be added after game has started')
        
        if dt is None:
            await self.channel.send('Using default time bank of {} seconds'.format(
                int(defaultTime.total_seconds())
            ))
            dt = defaultTime
        else:
            dt = cc.timedelta(seconds=dt)

        if dt > maxTime:
            raise InvalidTimerIteraction('Maximum time for a player is {} seconds'.format(
                int(maxTime.total_seconds())
            ))

        if user in self.player2reg:
            # Same user, new number
            oldi = self.player2reg[user]
            await self.channel.send('{} was player {} but will now be player {}'.format(
                user.name,oldi,i
            ))
            self.player2reg.pop(user)
            self.reg2userTimePair.pop(oldi)

        if i is None:
            i = len(self.reg2userTimePair)

        if i in self.reg2userTimePair:
            # Same number, new user
            other = self.reg2userTimePair[i][0]
            await self.channel.send('{} will replace {} as player {}'.format(
                user.name,other.name,i
            ))
            self.player2reg.pop(other)
            self.reg2userTimePair.pop(i)

        if len(self.reg2userTimePair) >= maxPlayers or len(self.player2reg) >= maxPlayers:
            raise InvalidTimerIteraction('Registration cancelled: max players reached')
        else:
            await self.channel.send('Successfully registered {} as player {}'.format(
                user.name,i
            ))
            

        self.reg2userTimePair[i] = (user,dt)
        self.player2reg[user] = i

    async def begin(self,message):
        # Start with the players we have
        user = message.author
        self.playerCheck(user)

        self.timing = True
        reglist = list(self.reg2userTimePair)
        reglist.sort()
        self.clock = cc.ChessClock([self.reg2userTimePair[key][1] for key in reglist])
        self.names = [self.reg2userTimePair[key][0].name for key in reglist]

        # Replace registration numbers (which could be 1,2 for example)
        # With player numbers 0,1
        for i in range(len(reglist)):
            self.player2reg[self.reg2userTimePair[reglist[i]][0]] = i
#        t = message.created_at
        t = cc.datetime.utcnow()
        self.clock.unpause(t)
        await self.sendTimerMessage()
        await self.loopUpdate()

    async def sendTimerMessage(self):
        # Move timer message to the bottom of chat
        # Use this after most commands
        if self.timerMessage is not None:
            await self.timerMessage.delete()
        t = cc.datetime.utcnow()
        self.timerMessage = await self.channel.send(self.strAt(t))

    async def loopUpdate(self):
        # Start main loop
        while self.timing and not self.clock.paused and not self.clock.expired:
            # Main timing loop
            t = cc.datetime.utcnow()
            try:
                await self.timerMessage.edit(content=self.strAt(t))
            except Exception as e:
                # Hopefully, this isn't needed
                # The message has sometimes been deleted because of commands,
                # but I don't anticipate other exceptions happening
#                print('An exception in main loop')
#                print(e)
                pass
            await sleep(1)
        if self.clock is None or self.clock.expired:
            # Game is over, so don't delete the old message anymore
            self.timerMessage = None

    async def stop(self,message):
        self.timerMessage = None
        self.reg2userTimePair = {}
        self.player2reg = {}
        self.clock = None
        self.timing = False
        self.names = None
        await self.channel.send('Game cancelled. Please report anyone abusing this feature to Babamots.')

    def confirmTurn(self,message):
        # Raise an exception if player may not move
        if not self.timing:
            raise InvalidTimerIteraction('Game has not started yet')
        user = message.author
        self.playerCheck(user)
        if not user in self.player2reg:
            raise InvalidTimerIteraction('{} is not a player'.format(user.name))
        if self.player2reg[user] != self.clock.onmove:
            raise InvalidTimerIteraction('It is not your turn')

    async def addPly(self,message):
#        t = message.created_at
        self.confirmTurn(message)
        t = cc.datetime.utcnow()
        self.clock.addPly(t)
        await self.sendTimerMessage()
            
    async def togglePause(self,message):
        if not self.timing:
            raise InvalidTimerIteraction('Game has not started yet')
        if self.clock.paused:
            await self.unpause(message)
        else:
            await self.pause(message)

    async def pause(self,message):
        if not self.timing:
            raise InvalidTimerIteraction('Game has not started yet')
        user = message.author
        self.playerCheck(user)
#        t = message.created_at
        t = cc.datetime.utcnow()
        self.clock.pause(t)
        await self.sendTimerMessage()

    async def unpause(self,message):
        if not self.timing:
            raise InvalidTimerIteraction('Game has not started yet')
        user = message.author
        self.playerCheck(user)
#        t = message.created_at
        t = cc.datetime.utcnow()
        self.clock.unpause(t)

        await self.sendTimerMessage()
        await self.loopUpdate()
        
    def playerCheck(self,user):
        if not user in self.player2reg:
            raise InvalidTimerIteraction('Only players may interact with the timer')

    def strAt(self,t):
        if not self.timing:
            return str(self)
        return self.clock.strAt(t,self.names)

    def __str__(self):
        if self.timing:
            return str(self.clock)
        return 'GAME HAS NOT BEGUN\n'+'\n'.join(['Player {} is {} with time bank of {}'.format(
            i,
            self.reg2userTimePair[i][0].name,
            self.reg2userTimePair[i][1]
        ) for i in self.reg2userTimePair])
    def __repr__(self):
        return str(self)
        
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
    ctimer = ChannelTimer(None)
    ctimer.register(p0,4)
    ctimer.register(p0,0,10)
    ctimer.register(p1,0,10)
    ctimer.register(p2,1,10)
    try:
        ctimer.register(p0,2,10)
        print('FAILED')
    except InvalidTimerIteraction as e:
        print(e)
    ctimer.register(p0,0,10)
    ctimer.register(p1,1,10)
    print(ctimer)
    try:
        ctimer.register(p0,0,10000000)
        print('\n\nFAILED\n\n')
    except InvalidTimerIteraction as e:
        print(e)

    ###############
    # Clock tests #
    ###############
    notime = cc.timedelta(0)
    sec = cc.timedelta(seconds=1)
    t = cc.datetime.utcnow()

    try:
        ctimer.begin(TestMessage(p2,t))
        print('\n\nFAILED\n\n')
    except InvalidTimerIteraction as e:
        print(e)
    ctimer.begin(TestMessage(p0,t))
    print(ctimer.strAt(t))

    ctimer.unpause(TestMessage(p0,t))
    t += 3*sec
    ctimer.addPly(TestMessage(p0,t))
    print(ctimer.strAt(t))

    t += 3*sec
    try:
        ctimer.addPly(TestMessage(p0,t))
        print('\n\nFAILED\n\n')
    except InvalidTimerIteraction as e:
        print(e)
    ctimer.addPly(TestMessage(p1,t))
    print(ctimer.strAt(t))
    t += 3*sec
    ctimer.pause(TestMessage(p1,t))
    try:
        ctimer.addPly(TestMessage(p0,t))
        print('\n\nFAILED\n\n')
    except cc.ChessClockException as e:
        print(e)
    t += 3*sec
    ctimer.togglePause(TestMessage(p1,t))
    t += 3*sec
    print(ctimer.strAt(t))
    try:
        ctimer.addPly(TestMessage(p0,t))
        print('\n\nFAILED\n\n')
    except cc.ChessClockException as e:
        print(e)



        
