# Tools for drawing a state

import matplotlib.pyplot as plt
import numpy as np
import color
from ship import Ship
from piece import Piece
import placement

rgb = ['#FF0000','#FFFF00','#00BB00','#0044FF']
bankBackground = '#888888'

pipsize = 4

bankBounds = np.array([
    [-3,.5],
    [ 3,.5],
    [ 3,-7],
    [-3,-7],
])
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
buffout = 1
# Vertical space allocated for each row
rowHeight = 2.75
# Space to leave at the top and bottom
margin = 0.5

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
        plt.plot(x-i*sgn/6,y-scale*7/8+sgn*0.2,'ko',markersize=pipsize)

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
        plt.plot(x-i/6,y-scale/2+0.2,'ko',markersize=pipsize)

def drawRow(row,y):
    # list of systems to draw
    # y coordinate at which to draw
    # Returns the width of the row
    wid = 0
    for sys in row:
        for ship in sys.ships:
            wid += scales[ship.piece.size]
        for marker in sys.markers:
            wid += scales[marker.size]
        wid += buffin*(len(sys.ships)+len(sys.markers)-1)
    wid += buffout*(len(row)-1)
    x = -wid/2
    for sys in row:
        # Ships on the left
        ships = [s for s in sys.ships if s.player == 0]
#        placement.shipSort(ships)
        ships.sort()
        for ship in ships:
            scale = scales[ship.piece.size]
            drawShip(ship,x+scale/2,y)
            x += scale+buffin
        markers = sys.markers
        markers.sort(reverse=True)
        plt.text(x,y+1,sys.name)
        for marker in sys.markers:
            scale = scales[marker.size]
            drawMarker(marker,x+scale/2,y)
            x += scale+buffin
        ships = [s for s in sys.ships if s.player == 1]
        ships.sort(reverse=True)
        for ship in ships:
            scale = scales[ship.piece.size]
            drawShip(ship,x+scale/2,y)
            x += scale+buffin
        x += buffout-buffin
    return wid

def drawState(state,fname=None):
    # Draws the currents state of a Binary HW game
    drawStash(state.stash,0,0)
    rows = placement.systemSort(state.systems)
    nrows = len(rows)
    width = 0
    for i in range(nrows):
        width = max(width,drawRow(rows[i],(nrows-i)*rowHeight-0.5))
    height = 5+nrows*rowHeight
    plt.xlim(-width/2-margin,width/2+margin)
    plt.ylim(-6.75,height-4.5)
    plt.axis('off')

    plt.gcf().set_size_inches(width,height)
    plt.subplots_adjust(left=0., right=1., top=1., bottom=0.)

    if fname is not None:
        plt.savefig(fname,dpi=100)


def drawStash(stash,x,y):
    # Draw the given system with x,y as middle of top
    plt.gca().add_patch(plt.Polygon(
        bankBounds+[x,y] ,
        facecolor=bankBackground,
    ))
    x -= 2
    y -= 6
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
        att('homeworld b3 y1 g3 Bob',state)

        att('build g1 Alice',state)
        att('build g1 Bob',state)

        att('trade g1 y1 Alice',state)
        att('discover g1 Bob b2 Howdy',state)

        att('discover y1 Alice g3 Doody',state)
        att('build g1 Howdy',state)

        att('build y1 Doody',state)
        att('build g1 Howdy',state)

        att('discover y1 Doody b1 Partner',state)
        att('trade g1 r1 Howdy',state)

        att('build y2 Doody',state)
        att('build g1 Bob',state)

        att('move y2 Doody Howdy',state)
        att('build g2 Howdy',state)

        att('discover y1 Doody g2 Rustle',state)
        att('trade g2 r2 Howdy',state)

        att('discover y1 Partner r2 Saddle',state)
        att('build g2 Bob',state)

        att('discover y1 Saddle g3 HappyNow',state)

        drawState(state,'stateImages/game.png')



