
import piece, color
from hwExceptions import StashOutException

displayStr = '''
   R Y G B
3: {} {} {} {}
2: {} {} {} {}
1: {} {} {} {}
'''

class Stash:
    def __init__(self,hi,pieces=None):
        self.hi = hi
        if pieces is None:
            pieces = dict([(c,{1:hi,2:hi,3:hi}) for c in color.colors])
        self.pieces = pieces
        
    def request(self,c,s=None):
        '''
        request(piece)
            returns desired piece, it is removed from the stash
        request(color)
            returns the smallest piece of color, it is removed from the stash
        request(color,size)
            returns desired piece, it is removed from the stash
        '''
        if isinstance(c,piece.Piece):
            # c is actually a Piece
            s = c.size
            c = c.color
        if not s is None:
            if self.pieces[c][s]>0:
                self.pieces[c][s] -= 1
                return piece.Piece(s,c)
            raise StashOutException('No such pieces remain')
        
        s = self.querySmallest(c)
        if s is None:
            raise StashOutException('No pieces of this color remain')

        self.pieces[c][s] -= 1
        return piece.Piece(s,c)

    def isAvailable(self,c,s=None):
        '''
        returns a bool

        isAvailable(piece)
            Is at least one such piece in the stash?
        isAvailable(color)
            Is at least one piece of this color in the stash?
        isAvailable(color,size)
            Is at least one such piece in the stash?
        '''
        if isinstance(c,piece.Piece):
            # c is actually a Piece
            s = c.size
            c = c.color
        if s is None:
            return any(self.pieces[c])
        return self.pieces[c][s] > 0
        

    def querySmallest(self,c):
        for size in piece.sizes:
            if self.pieces[c][size] > 0:
                return size
        return None
    
    def putBack(self,piece):
        self.pieces[piece.color][piece.size] += 1

    def asList(self):
        result = []
        for s in piece.sizes[::-1]:
            for c in color.colors:
                result.append(self.pieces[c][s])
        return result

    def __str__(self):
        return displayStr.format(*self.asList())

    def deepCopy(self):
        pieces = dict(self.pieces)
        for c in pieces:
            pieces[c] = dict(pieces[c])
        return Stash(self.hi,pieces)


