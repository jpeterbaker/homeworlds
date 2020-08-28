
import event
from color import colors
from piece import fromTuple as pieceFromTuple
from ship import fromTuple as shipFromTuple

nNameless = [0]

def fromSaveTuple(t):
    home = t[0]
    name = t[1]
    markers = [pieceFromTuple(p) for p in t[2]]
    ships = [shipFromTuple(s) for s in t[3]]
    sys = System(markers,home,name)
    for ship in ships:
        sys.addShip(ship)
    return sys

class System:
    def __init__(self,markers,home=None,name=None):
        markers.sort()
        self.markers = markers
        self.home = home # player number for whom this system is home
        self.ships = []
        if name is None:
            name = str(nNameless[0])
            nNameless[0] += 1
        self.name = name
        self.concentration = [0]*4
        for m in markers:
            self.concentration[m.color] += 1

    # Don't deep copy ships or markers since they never change
    def deepCopy(self):
        markers = list(self.markers)
        ships = list(self.ships)
        ships.sort()
        sys = System(markers,self.home,self.name)
        sys.ships = ships
        return sys

    def getTech(self,player):
        # Get a set of technology colors available to player
        return (
            set([m.color for m in self.markers])
            | set([s.piece.color for s in self.ships if s.player == player])
        )

    def tuplify(self):
        self.ships.sort()
        return (self.home,
                tuple([m.tuplify() for m in self.markers]),
                tuple([s.tuplify() for s in self.ships]))

    def saveTuple(self):
        return (self.home,
                self.name,
                tuple([m.tuplify() for m in self.markers]),
                tuple([s.tuplify() for s in self.ships]))

    def connectsTo(self,other):
        for m1 in self.markers:
            for m2 in other.markers:
                if m1.size == m2.size:
                    return False
        return True

    def isEmpty(self):
        return len(self.ships) == 0

    def isVoid(self):
        # returns true if all this system's markers have been destroyed or all the ships have left
        return (len(self.ships) == 0) or (len(self.markers) == 0)

    def hasPresence(self,player,c=None):
        # returns true if given player has at least one ship in this system
        #                 and that ship is the specified color, or a system marker is that color
        # if c=None, a ship of any color counts
        if not c is None:
            # If a specific color is desired, remove that requirement if a system marker has it
            for m in self.markers:
                if m.color == c:
                    # If a 
                    c = None
                    break
        for s in self.ships:
            if s.player == player:
                if c is None or s.piece.color == c:
                    return True
        return False

    def getLargestShip(self,player):
        hisize = 0
        hiship = None
        for ship in self.ships:
            if ship.player == player and ship.piece.size > hisize:
                if ship.piece.size == 3:
                    return ship
                hisize = ship.piece.size
                hiship = ship
        return hiship

    def removeMarker(self,marker):
        self.markers.remove(marker)
        self.concentration[marker.color] -= 1

    def restoreMarker(self,marker):
        self.markers.append(marker)
        self.markers.sort()
        self.concentration[marker.color] += 1

    def addShip(self,ship):
        self.ships.append(ship)
        self.concentration[ship.piece.color] += 1

    def removeShip(self,ship):
        self.ships.remove(ship)
        self.concentration[ship.piece.color] -= 1

    def getCatastrophes(self):
        cats = []
        for c in colors:
            if self.concentration[c] >= 4:
                cats.append(event.Catastrophe(self,c))
        return cats

    def getFade(self):
        # Get the Fade action caused by this system being forgotten
        # If the marker or ships were destroyed or moved away by other events, the pieces should have already been returned to the stash
        # We just need a list of additional things that disappear as a result
        if not self.isVoid():
            return None
        return event.Fade(self)

    def __str__(self):
        if not self.home is None:
            homestr = ' (home of %s)'%(str(self.home))
        else:
            homestr = ' (nobody\'s home)'
        return 'System %s: %s%s%s'% \
            (self.name, \
            self.markers, \
            homestr, \
            '\n\t'.join(['']+[str(s) for s in self.ships]))

