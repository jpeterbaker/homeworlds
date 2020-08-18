
from piece import fromTuple as pieceFromTuple

def fromTuple(t):
    return Ship(pieceFromTuple(t[1]),t[0])

class Ship:
    def __init__(self,piece,player=None):
        self.piece  = piece
        self.player = player
    def __str__(self):
        return '%s: %s'%(self.player,self.piece)
    def tuplify(self):
        return (self.player,self.piece.tuplify())
    def deepCopy(self):
#        return Ship(self.piece.deepCopy(),self.player)
        return self
    def __lt__(self,other):
        return self.tuplify() < other.tuplify()
