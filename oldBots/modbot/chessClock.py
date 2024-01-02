
# Chess clock interface
# Bring your own time-keeping method

from datetime import timedelta,datetime
notime = timedelta(0)

class ChessClockException(Exception):
    pass

class ChessClock:
    def __init__(self,times):
        # n = number of players
        # times = list of beginning times (timedeltas)
        #     or, just one of them which will be given to all players
        self.times = list(times)
        self.n = len(times)
        self.expired = False
        for i in range(self.n):
            if self.times[i] < notime:
                self.expired = True
                self.times[i] = notime
        self.lastPress = None
        # Player whose clock is running
        self.onmove = 0
        self.paused = True

    def addPly(self,t):
        # Pause current player's timer and start the next one
        if self.paused:
            raise ChessClockException('Button disabled while timer is paused.')
        if self.expired:
            raise ChessClockException('Timer is expired.')
        self.takeTime(t)
        self.onmove = (self.onmove+1)%self.n

    def unpause(self,t):
        # Begin countdown either for the first time or after a pause
        if self.expired:
            raise ChessClockException('Timer is expired.')
        if self.paused:
            self.lastPress = t
        if self.lastPress is not None and t < self.lastPress:
            raise ChessClockException('Reverse time travel not allowed.')
        self.paused = False

    def copy(self):
        other = ChessClock(self.times)
        other.paused = self.paused
        other.lastPress = self.lastPress
        other.onmove = self.onmove
        return other

    def pause(self,t):
        # Pause the countdown
        if self.expired:
            raise ChessClockException('Timer is expired.')
        if self.paused:
            raise ChessClockException('Timer is already paused.')
        if self.lastPress is None:
            return
        # Subtract elapsed time from current player
        self.takeTime(t)
        self.paused = True

    def togglePause(self,t):
        if self.paused:
            self.unpause(t)
        else:
            self.pause(t)

    def takeTime(self,t):
        # Take time from current player according to the time that has passed since lastPress
        # Updates lastPress
        if t < self.lastPress:
            raise ChessClockException('Reverse time travel not allowed.')
        if self.paused:
            raise ChessClockException('Time may not be taken away while paused.')
        self.times[self.onmove] -= t - self.lastPress
        if self.times[self.onmove] < notime:
            self.expired = True
            self.times[self.onmove] = notime
        self.lastPress = t

    def getTimes(self,t):
        # Get time remaining for all players (could be negative)
        # Internal variables are only affected if t is late enough to expire
        if self.lastPress is not None and t < self.lastPress:
            raise ChessClockException('Reverse time travel not allowed.')
        times = list(self.times)
        if self.paused:
            return times
        times[self.onmove] -= t - self.lastPress
        if times[self.onmove] <= notime:
            self.expired = True
            self.takeTime(self.lastPress + self.times[self.onmove])
            self.times = times
        return times

    def getLoser(self):
        if not self.expired:
            return None
        for i in range(self.n):
            if self.times[i] <= notime:
                return i
        raise Exception('Somehow, expired flag is set but no player is out of time.')

    def strAt(self,t,names=None):
        # Represent chess clock as string
        # Can cause clock to expire
        if names is None:
            name = ['Player 0','Player 1']
        times = self.getTimes(t)
        
        flags = ['']*self.n
        if self.expired:
            flags[self.getLoser()] = '(expired)'
        elif self.paused:
            flags[self.onmove] = '(turn paused)'
        else:
            flags[self.onmove] = ' <-----'
        s = ['{} {}\n    `{}:{:02}`'.format(
            names[i],
            flags[i],
            int(times[i].total_seconds())//60,
            int(times[i].total_seconds())%60
        ) for i in range(self.n)]
        return '\n===================\n'.join(s)

    def __repr__(self):
        return str(self)
    def __str__(self):
        return timesToStr(self.times)

class FischerClock(ChessClock):
    def __init__(self,times,incs):
        # incs is a list of timedelta
        # it's the amount of time added to the player's clocks each time their turn starts
        ChessClock.__init__(self,times)
        self.incs = incs
    def addPly(self,t):
        ChessClock.addPly(self,t)
        self.times[self.onmove] += self.incs[self.onmove]
    def copy(self):
        other = FischerClock(self.times,self.incs)
        other.paused = self.paused
        other.lastPress = self.lastPress
        other.onmove = self.onmove
        return other

class HourGlass(ChessClock):
    def __init__(self,times):
        ChessClock.__init__(self,times)
        if not self.n == 2:
            raise ChessClockException('Hourglasses are only for two-player games')

    def takeTime(self,t):
        # Take time from current player according to the time that has passed since lastPress
        # Updates lastPress
        if t < self.lastPress:
            raise ChessClockException('Reverse time travel not allowed.')
        if self.paused:
            raise ChessClockException('Time may not be taken away while paused.')

        self.times[1-self.onmove] += t - self.lastPress
        self.times[  self.onmove] -= t - self.lastPress
        if self.times[self.onmove] <= notime:
            self.expired = True
            self.times[1-self.onmove] -= self.times[self.onmove]
            self.times[  self.onmove]  = notime
        self.lastPress = t
        
    def getTimes(self,t):
        # Get time remaining for all players (could be negative)
        # Internal variables are only affected if t is late enough to expire
        if self.lastPress is not None and t < self.lastPress:
            raise ChessClockException('Reverse time travel not allowed.')
        times = list(self.times)
        if self.paused:
            return times
        times[self.onmove] -= t - self.lastPress
        times[1-self.onmove] += t - self.lastPress
        if times[self.onmove] <= notime:
            self.expired = True
            self.takeTime(self.lastPress + self.times[self.onmove])
        return times

def sec2str(s):
    s = int(s)
    m = s//60
    return '{}:{:02}'.format(m,s%60)

def timesToStr(times):
        return '\n'.join(['Player {} -- {}'.format(
            i,
            sec2str(times[i].total_seconds())
        ) for i in range(len(times))])

if __name__=='__main__':
    print('''
    Sorry, this doesn't actually run a chess clock.
    As a script, this just runs some tests.
    As a module, this file just implements a ChessClock class
    for keeping track of time and timeouts.
    ''')
    t = datetime.utcnow()
    asecond = timedelta(seconds=1)
#    clock = ChessClock([asecond*60]*2)
#    clock = FischerClock([asecond*60]*2,[asecond*5]*2)
    clock = HourGlass([asecond*60]*2)
    print(clock)
    print()
    clock.unpause(t)
    t += asecond*3
    print(clock.strAt(t,['Billy','Bobby']))
    print()
    t += asecond*3
    print(clock.strAt(t,['Billy','Bobby']))
    print()
    t += asecond*3
    print(clock.strAt(t,['Billy','Bobby']))
    print()
    t += asecond*3
    clock.addPly(t)
    print(clock.strAt(t,['Billy','Bobby']))
    print()
    t += asecond*3
    print(clock.strAt(t,['Billy','Bobby']))
    print()

