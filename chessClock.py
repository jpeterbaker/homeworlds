
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
        self.onclock = 0
        self.paused = True

    def addPly(self,t):
        # Pause current player's timer and start the next one
        if self.paused:
            raise ChessClockException('Button disabled while timer is paused')
        if self.expired:
            raise ChessClockException('Timer is expired')
        self._takeTime(t)
        self.onclock = (self.onclock+1)%self.n
        self.lastPress = t

    def unpause(self,t):
        # Begin countdown either for the first time or after a pause
        if self.expired:
            raise ChessClockException('Timer is expired')
        if self.lastPress is None:
            self.lastPress = t
        if t < self.lastPress:
            raise ChessClockException('Reverse time travel not allowed')
        self.paused = False

    def pause(self,t):
        # Pause the countdown
        if self.expired:
            raise ChessClockException('Timer is expired')
        if self.lastPress is None:
            return
        # Subtract elapsed time from current player
        self._takeTime(t)
        self.lastPress = t
        self.paused = True

    def _takeTime(self,t):
        # Take time from current player according to the time that has passed since lastPress
        # This does not affect lastPress, which is a little unintuitive
        # so the function is being hidden with an underscore name
        if t < self.lastPress:
            raise ChessClockException('Reverse time travel not allowed')
        if self.paused:
            raise ChessClockException('Time may not be taken away while paused')
        self.times[self.onclock] -= t - self.lastPress
        if self.times[self.onclock] < notime:
            self.expired = True
            self.times[self.onclock] = notime

    def getTimes(self,t):
        # Get current time remaining for all players
        # Does not affect internal variables
        # UNLESS a player has timed out, in which case,
        # expired flag is set and the time list is updated
        if self.lastPress is not None and t < self.lastPress:
            raise ChessClockException('Reverse time travel not allowed')
        times = list(self.times)
        if self.paused:
            return times
        times[self.onclock] -= t - self.lastPress
        if times[self.onclock] <= notime:
            self.expired = True
            times[self.onclock] = notime
            self.times = times
        return times

    def getLoser(self):
        if not self.expired:
            return None
        for i in range(self.n):
            if self.times[i] <= notime:
                return i
        raise Exception('Somehow, expired flag is set but no player is out of time')

    def strAt(self,t):
        times = self.getTimes(t)
        s = ['Player {} -- {}:{:02}'.format(
            i,
            int(times[i].total_seconds())//60,
            int(times[i].total_seconds())%60
        ) for i in range(self.n)]
        if self.expired:
            s[self.getLoser()] += ' (expired)'
        elif self.paused:
            s[self.onclock] += ' (turn paused)'
        else:
            s[self.onclock] += ' <----'
        return '\n'.join(s)

    def repr(self):
        return str(self)
    def __str__(self):
        return timesToStr(self.times)

def timesToStr(times):
        return '\n'.join(['Player {} -- {}:{:02}'.format(
            i,
            int(times[i].total_seconds())//60,
            int(times[i].total_seconds())%60
        ) for i in range(len(times))])

if __name__=='__main__':
    t = datetime.utcnow()
    asecond = timedelta(seconds=1)
    clock = ChessClock([asecond*60]*2)
    print(clock)
    print()
    clock.unpause(t)
    t += asecond*3
    print(clock.strAt(t))
    print()
    t += asecond*3
    print(clock.strAt(t))
    print()
    t += asecond*3
    print(clock.strAt(t))
    print()
    t += asecond*3
    clock.addPly(t)
    print(clock.strAt(t))
    print()
    t += asecond*3
    print(clock.strAt(t))
    print()

