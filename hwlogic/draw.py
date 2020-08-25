# Tools for drawing a state

import matplotlib.pyplot as plt
import numpy as np
import color
from ship import Ship
from piece import Piece
import placement

rgb = ['#FF0000','#FFFF00','#00BB00','#0044FF']

# Vertex coordinates of triangle template
tri = np.array([
    [-1/2 , -7/8],
    [ 0   ,  7/8],
    [ 1/2 , -7/8],
])
# Vertex coordinates of square template
sqr = np.array([
    [-1,-1],
    [ 1,-1],
    [ 1, 1],
    [-1, 1],
])/2
# Scaling factor to apply to pieces of different sizes
scales = [None , 9/16 , 3/4 , 1]
# Thickness of a piece (for stacking)
thickness = 1/3
# Jimmy rigging the position of pieces in bank
bankboost = [0,2,4.4]
# Horizontal space between objects in same system
buffin = 1/8
# Horizontal space between objects in different systems
buffout = 3/4

def drawShip(ship,x,y):
    # Draw the given ship centered at x,y
    scale = scales[ship.piece.size]
    if ship.player == 0:
        scale *= -1
    plt.gca().add_patch(plt.Polygon(
        scale*tri+[x,y] ,
        facecolor=rgb[ship.piece.color],
        edgecolor='k',
        linewidth=2,
    ))
    sgn = 2*ship.player-1
    for i in range(ship.piece.size):
        plt.plot(x-i*sgn/6,y-sgn*(scale*7/8-0.2),'ko')

def drawMarker(piece,x,y):
    # Draw the given marker centered at x,y
    scale = scales[piece.size]
    plt.gca().add_patch(plt.Polygon(
        scale*sqr+[x,y] ,
        facecolor=rgb[piece.color],
        edgecolor='k',
        linewidth=2,
    ))
    for i in range(piece.size):
        plt.plot(x-i/6,y-scale/2+0.2,'ko')

def drawSystem(system,x,y):
    # Draw the given system with x,y as bottom left corner
    pass

def drawRow(row,y):
    # list of systems to draw
    # y coordinate at which to draw
    wid = 0
    for sys in row:
        for ship in sys.ships:
            wid += scales[ship.piece.size]
        for marker in sys.markers:
            wid += scales[marker.size]
        wid += buffin*(len(sys.ships)+len(sys.markers)-1)
    x = -wid/2
    for sys in row:
        # Ships on the left
        ships = [s for s in sys.ships if s.player == 0]
#        placement.shipSort(ships)
        ships.sort()
        for ship in ships:
            scale = scales[ship.piece.size]
            drawShip(ship,x+scale/2,y+scale/2)
            x += scale+buffin
        markers = sys.markers
        markers.sort()
        for marker in sys.markers:
            scale = scales[marker.size]
            drawMarker(marker,x+scale/2,y+scale/2)
            x += scale+buffin
        ships = [s for s in sys.ships if s.player == 1]
        ships.sort()
        for ship in ships:
            scale = scales[ship.piece.size]
            drawShip(ship,x+scale/2,y+scale/2)
            x += scale+buffin
        x += buffout-buffin

def drawState(state):
    # Draws the currents state of a Binary HW game
    # Stash at the bottom
    # Origin is the top center of stash
    drawStash(state.stash,-1.5,-6)
    rows = placement.systemSort(state.systems)
    nrows = len(rows)
    for i in range(nrows):
        drawRow(rows[i],(nrows-i)*2)

def drawStash(stash,x,y):
    # Draw the given system with x,y as bottom left corner
    for c in color.colors:
        for size in range(1,4):
            piece = Piece(size,c)
            ship = Ship(piece,1)
            for i in range(stash.pieces[c][size]):
                drawShip(ship,x+c,y+bankboost[size-1]+i*thickness)

if __name__=='__main__':
    if 0:
        # Ship test
        s = Ship(Piece(3,color.BLUE),0)
        drawShip(s,0,0)
        plt.show()
    if 0:
        # Ship test
        marker = Piece(3,color.BLUE)
        drawMarker(marker,0,0)
        plt.show()
    if 0:
        # Stash test
        from stash import Stash
        stash = Stash(3)
        drawStash(stash,0,0)
        plt.xlim([-1,5])
        plt.ylim([-2,8])
        plt.show()
    if 1:
        from hwstate import HWState
        from text2turn import applyTextTurn as att
        state = HWState()
        att('homeworld r2 b1 g3 Alice',state)
        drawState(state)
        plt.xlim([-5,5])
        plt.ylim([-6,10])
        plt.show()



