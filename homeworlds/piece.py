
import color

sizes = [1,2,3]

def fromTuple(t):
    return Piece(t[1],t[0])

class Piece:
    def __init__(self,size,color):
        self.size  = size
        self.color = color

    def __hash__(self):
        return (self.size,self.color).__hash__()

    def __eq__(self,other):
        return (self.size==other.size) & (self.color==other.color)
    def __lt__(self,other):
        return self.tuplify() < other.tuplify()

    def __str__(self):
        return color.names[self.color]+str(self.size)
    def __repr__(self):
        return str(self)
    def tuplify(self):
        return (self.color,self.size)
    def deepCopy(self):
#        return Piece(self.size,self.color)
        return self

