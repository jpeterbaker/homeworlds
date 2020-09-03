#!/usr/bin/python3.7
# Tools for drawing a state VERTICALLY

import matplotlib.pyplot as plt
import numpy as np
import color
from ship import Ship
from piece import Piece
import placement

rgb = ['#FF0000','#FFFF00','#00BB00','#0044FF']
bankBackground = '#888888'
turnTokenColor = '#D4AF37'

pipsize = 4

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
# Also the width of the base of a piece of that size
scales = [None , 9/16 , 3/4 , 1]
# Thickness of a piece (for stacking)
thickness = 1/3
# Horizontal space between objects in same system
buffin = 1/8
# Horizontal space between objects in different systems
buffout = 1
# Vertical space allocated for each row
rowHeight = 2.75
# Space to leave at the top and bottom
margin = 0.5

turnTokenRadius = 0.75

bankHeight = 6*thickness + sum(scales[1:])*1.75 + 4*buffin
bankWidth  = 4+5*buffin
bankBounds = np.array([
    [-bankWidth/2,          0],
    [ bankWidth/2,          0],
    [ bankWidth/2,-bankHeight],
    [-bankWidth/2,-bankHeight],
])
# y coordinates of the bottoms of the stacks
bankYbots = [None,
    -3*(buffin+2*thickness)-1.75*(scales[1]/2+scales[2]+scales[3]),
    -2*(buffin+2*thickness)-1.75*(scales[2]/2+scales[3]),
    -1*(buffin+2*thickness)-1.75*(scales[3]/2)
]

def drawTurnToken(x,y):
    plt.gca().add_patch(plt.Circle(
        [x,y],
        turnTokenRadius,
        facecolor=turnTokenColor,
        edgecolor='k',
        linewidth=2,
    ))
    plt.text(x,y,'MY\nTURN',ha='center',va='center',fontsize=20)

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

def drawRow(row,y,homeOnMove=None):
    # list of systems to draw
    # y coordinate at which to draw
    # homeOnMove 0 or 1 if this is a home row and that player is on-move
    # Returns the width of the row
    wid = 0
    for sys in row:
        for ship in sys.ships:
            wid += scales[ship.piece.size]
        for marker in sys.markers:
            wid += scales[marker.size]
        wid += buffin*(len(sys.ships)+len(sys.markers)-1)
    wid += buffout*(len(row)-1)
    if homeOnMove is not None:
        wid += 2*turnTokenRadius + buffin
    x = -wid/2
    if homeOnMove == 0:
        # Draw the token on the left
        drawTurnToken(x+turnTokenRadius,y)
        x += 2*turnTokenRadius + buffin
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
        label = sys.name
        plt.text(x,y+1,label,fontsize=14)
        for marker in sys.markers:
            scale = scales[marker.size]
            drawMarker(marker,x+scale/2,y)
            x += scale+buffin
        ships = [s for s in sys.ships if s.player == 1]
        ships.sort(reverse=True)
        for ship in ships:
            scale = scales[ship.piece.size]
            drawShip(ship,x+scale/2,y)
            x += scale + buffin
        x += buffout - buffin
    if homeOnMove == 1:
        # Draw the token on the right
        x -= buffout - buffin
        drawTurnToken(x+turnTokenRadius,y)
    return wid

def drawState(state,fname=None):
    # Draws the currents state of a Binary HW game
    drawStash(state.stash)
    rows = placement.systemSort(state.systems)
    nrows = len(rows)
    # Determine if token should be drawn for player 0
    if nrows > 1 and state.onmove == 0:
        token = 0
    else:
        token = None
    # Start with width of stash
    width = 4+2*buffin
    if nrows > 0:
        width = max(width,drawRow(rows[0],(nrows-0.5)*rowHeight,token))
    for i in range(1,nrows-1):
        width = max(width,drawRow(rows[i],(nrows-i-0.5)*rowHeight))
    # Determine if token should be drawn for player 1
    if nrows > 1 and state.onmove == 1:
        token = 1
    else:
        token = None
    if nrows > 0:
        width = max(width,drawRow(rows[nrows-1],rowHeight/2,token))

    height = 5+nrows*rowHeight
    plt.xlim(-width/2-margin,width/2+margin)
    plt.ylim(-6.75,height-4)
    plt.axis('off')

    plt.gcf().set_size_inches(width,height)
    plt.subplots_adjust(left=0., right=1., top=1., bottom=0.)

    if fname is not None:
        plt.savefig(fname,dpi=100)
        plt.clf()

def drawStash(stash):
    # Draw the given system with x,y as middle of top
    plt.gca().add_patch(plt.Polygon(
        bankBounds,
        facecolor=bankBackground,
    ))
    for c in color.colors:
        x = c*(1+buffin) - 2 - buffin*1.5 + scales[3]/2
        for size in range(1,4):
            # y coord of center of bottom piece in this stack
            boty = bankYbots[size]
            piece = Piece(size,c)
            ship = Ship(piece,1)
            for i in range(stash.pieces[c][size]):
                drawShip(ship,x,boty+i*thickness)

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
        drawStash(stash)
        plt.xlim([-1,5])
        plt.ylim([-2,8])
        plt.show()
    if 1:
        from hwstate import HWState
        from text2turn import applyTextTurn as att
        state = HWState()
        i=0
        att('homeworld r2 b1 g3 Alice',state);        i+=1; drawState(state,"../stateImages/game{}.png".format(i))
        att('homeworld b3 y1 g3 Bob',state);          i+=1; drawState(state,"../stateImages/game{}.png".format(i))

        att('build g1 Alice',state);                  i+=1; drawState(state,"../stateImages/game{}.png".format(i))
        att('build g1 Bob',state);                    i+=1; drawState(state,"../stateImages/game{}.png".format(i))

        att('trade g1 y1 Alice',state);               i+=1; drawState(state,"../stateImages/game{}.png".format(i))
        att('discover g1 Bob b2 Howdy',state);        i+=1; drawState(state,"../stateImages/game{}.png".format(i))

        att('discover y1 Alice g3 Doody',state);      i+=1; drawState(state,"../stateImages/game{}.png".format(i))
        att('build g1 Howdy',state);                  i+=1; drawState(state,"../stateImages/game{}.png".format(i))

        att('build y1 Doody',state);                  i+=1; drawState(state,"../stateImages/game{}.png".format(i))
        att('build g1 Howdy',state);                  i+=1; drawState(state,"../stateImages/game{}.png".format(i))

        att('discover y1 Doody b1 Partner',state);    i+=1; drawState(state,"../stateImages/game{}.png".format(i))
        att('trade g1 r1 Howdy',state);               i+=1; drawState(state,"../stateImages/game{}.png".format(i))

        att('build y2 Doody',state);                  i+=1; drawState(state,"../stateImages/game{}.png".format(i))
        att('build g1 Bob',state);                    i+=1; drawState(state,"../stateImages/game{}.png".format(i))

        att('move y2 Doody Howdy',state);             i+=1; drawState(state,"../stateImages/game{}.png".format(i))
        att('build g2 Howdy',state);                  i+=1; drawState(state,"../stateImages/game{}.png".format(i))

        att('discover y1 Doody g2 Rustle',state);     i+=1; drawState(state,"../stateImages/game{}.png".format(i))
        att('trade g2 r2 Howdy',state);               i+=1; drawState(state,"../stateImages/game{}.png".format(i))

        att('discover y1 Partner r2 Saddle',state);   i+=1; drawState(state,'../stateImages/game{}.png'.format(i))
        att('build g2 Bob',state);                    i+=1; drawState(state,'../stateImages/game{}.png'.format(i))

        att('discover y1 Saddle g3 HappyNow',state);  i+=1; drawState(state,'../stateImages/game{}.png'.format(i))




