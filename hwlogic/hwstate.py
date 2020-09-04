
# Represents piece position, ownership, and partial turns

from stash import Stash
from turn import Turn
import event
from color import colors
import piece
from system import System,fromSaveTuple as systemFromTuple
from hwExceptions import TurnNotOverException
from text2turn import applyTextTurn

divideSysStr = '='*30

def fromTuple(t):
    # Create a state from a standard tuple
    onmove = t[0]
    alive = list(t[1])
    nplayers = len(alive)
    systems = [systemFromTuple(s) for s in t[2]]
    return HWState(nplayers,onmove,systems,alive=alive)

class HWState:
    def __init__(
        self,
        nplayers=2,
        onmove=0,
        systems=None,
        stash=None,
        alive=None, # list of player statuses, None for not yet created
    ):
        self.nplayers = nplayers
        self.onmove = onmove

        if systems is None:
            systems = []
            alive = [None]*nplayers
        self.systems = systems

        if stash is None:
            stash = Stash(nplayers+1)
            for sys in systems:
                for m in sys.markers:
                    stash.request(m)
                for s in sys.ships:
                    stash.request(s.piece)
        self.stash = stash

        if alive is None:
            # This assumes that players with no home have been eliminated
            alive = [False]*nplayers
            for sys in systems:
                if not sys.home is None:
                    alive[sys.home] = True

        self.alive = alive
        # This turn will be built one event as a time 
        self.curTurn = Turn(self)

    def deepCopy(self):
        systems = [s.deepCopy() for s in self.systems]
        stash = self.stash.deepCopy()
        alive = list(self.alive)
        return HWState(
            self.nplayers,
            self.onmove,
            systems,
            stash,
            alive
        )

    def creationOver(self):
        return self.alive.count(None) == 0

    def addSystem(self,system):
        self.systems.append(system)

    def removeSystem(self,system):
        self.systems.pop(self.systems.index(system))

    def findHome(self,player):
        for sys in self.systems:
            if sys.home == player:
                return sys
        # Player's home is missing
        return None

    def cancelTurn(self):
        self.curTurn.undoAll()

    def addEvent(self,e):
        # Event should be a Creation, Action, Catastrophe, or Pass
        # Fade and Elimination events are checked for and triggered here

        self.curTurn.addEvent(e)
        try:
            e.enact(self)
        except Exception as ex:
            # Signal the turn that the event is cancelled
            # This affects the turn's understanding of whether a sacrifice is occurring
            try:
                self.curTurn.undoLast()
            except:
                print('A problem occurred while resetting the turn. This could be a serious problem.')
                print(str(ex))
            raise ex

        # Check for Fades (but not for home systems)
        sys = e.getThreatenedSystem()
        if (not sys is None) and (sys.home is None) and sys.isVoid():
            fade = sys.getFade()
            self.curTurn.addEvent(fade)
            fade.enact(self)

    def finishTurn(self):
        # Checks for home system fades and eliminations
        if not self.curTurn.isCompleted():
            self.cancelTurn()
            raise TurnNotOverException('Turn is not complete. Did you forget to pass an unwanted sacrifice action?')

        # Check for elimination
        # TODO this is better for huge numbers of players, but slower otherwise
#        for player in self.curTurn.getThreatenedPlayers()
        for player in range(self.nplayers):
            # Check if player has been eliminated
            if self.alive[player] != True:
                # Player is either already known to be dead or hasn't created a home
                continue
            # Player is believed to be alive but may have just been eliminated
            home = self.findHome(player)
            abandoned  = not home.hasPresence(player)
            voided     = home.isVoid()

            if abandoned or voided:
                # Player has been eliminated
                elim = event.Elimination(player,self.onmove)
                self.curTurn.addEvent(elim)
                elim.enact(self)
            if voided:
                fade = home.getFade()
                self.curTurn.addEvent(fade)
                fade.enact(self)

    def startNewTurn(self):
        if self.isEnd():
            raise Exception('State is at endpoint.')
        self.advanceOnmove()
        self.curTurn = Turn(self)

    def advanceOnmove(self,d=1):
        # set d=-1 to get previous player
        self.onmove = self.getNextPlayer(d)

    def getNextPlayer(self,d=1):
        # set d=-1 to get previous player
        i = (self.onmove+d)%self.nplayers
        # TODO if current player is somehow dead, this is an endless loop
        while self.alive[i] == False:
            i = (i+d)%self.nplayers
        return i

    def getScores(self):
        if not self.isEnd():
            raise Exception('Game is not over.')
        if self.alive.count(True) == 0:
            return [1/self.nplayers]*self.nplayers
        scores = [0]*self.nplayers
        scores[self.alive.index(True)] = 1
        return scores

    def saveTuple(self):
        # Returns a tuple appropriate for saving the game
        # Systems are not sorted, so not appropriate for comparing states
        # Includes system names
        stuples = [s.saveTuple() for s in self.systems]
        return (self.onmove,tuple(self.alive),tuple(stuples))

    def tuplify(self):
        # Does not include system names, but systems are sorted
        # Appropriate for comparing states
        if not self.tupled is None:
            return self.tupled
        stuples = [s.tuplify() for s in self.systems]
        stuples.sort()
        self.tupled = (self.onmove,tuple(self.alive),tuple(stuples))
        return self.tupled

    def __hash__(self):
        return self.calcHash()

    def calcHash(self):
        return hash(self.tuplify())

    def isEnd(self):
        # TODO implement other win conditions
        if not self.creationOver():
            return False
        return self.alive.count(True) <= 1

    def __eq__(self,other):
        return self.tuplify() == other.tuplify()

    def __str__(self):
        divider = '/'*30
        movestr = 'Player %s to move'%self.onmove
        stashStr = str(self.stash)
        sysStr = ('\n%s\n'%divideSysStr).join([str(s) for s in self.systems])
        return '%s\n%s\n%s\n%s\n%s'%(divider,movestr,stashStr,sysStr,divider)

    def buildStr(self):
        return '<{}>;\n{}'.format(self.onmove,';\n'.join([sys.buildStr(self.nplayers) for sys in self.systems]))

    def getConnections(self,sys):
        # Return a list of systems connected to sys INCLUDING DISCOVERIES
        # TODO remember connections so this doesn't have to keep getting called
        connects = []
        # Existing systems
        for s in self.systems:
            if s.connectsTo(sys):
                connects.append(s)

        # Discoveries
        for size in piece.sizes:
            for m in sys.markers:
                if m.size == size:
                    break
            else:
                # Inner loop exited normally, discoveries may have this size
                for c in colors:
                    if self.stash.isAvailable(c,size):
                        p = piece.Piece(size,c)
                        connects.append(System([p]))
        return connects

