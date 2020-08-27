# Represent a game state, game history, and timer

class Match:
    def __init__(self,ctimer):
        self.ctimer = ctimer
        self.state = None
        self.history = []
    def reset(self):
        self.state = None
        self.history = []
    def addTurn(self,text):
        self.history.append(text)
    def getHistStr(self,):
        if len(self.history) == 0:
            return 'NO MOVES WERE MADE THIS GAME'
        x = []
        playernames = [self.ctimer.reg2userTimePair[k][0].name for k in range(2)]
        for i in range(len(self.history)):
            x.append('{}:\n{}\n'.format(playernames[i%2],self.history[i]))
        return '\n'.join(x)
