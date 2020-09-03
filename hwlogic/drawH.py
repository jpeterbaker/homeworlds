#!/usr/bin/python3.7
# Tools for drawing a state HORIZONTALLY

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

# Vertex coordinates of vertical triangle template
vtri = np.array([
    [-1/2 , -7/8],
    [ 0   ,  7/8],
    [ 1/2 , -7/8],
])
# Horizontal triangle
htri = np.array([
    [-7/8 , -1/2],
    [ 7/8 ,  0  ],
    [-7/8 ,  1/2],
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
# Vertical space allocated for each col
colWidth = 2.75
# Space to leave at the top and bottom
margin = 0.5

turnTokenRadius = 0.75

bankHeight = 6*thickness + sum(scales[1:])*1.75 + 4*buffin
bankWidth  = 4+5*buffin
bankBounds = np.array([
    [-bankWidth ,  bankHeight/2],
    [        0  ,  bankHeight/2],
    [        0  , -bankHeight/2],
    [-bankWidth , -bankHeight/2],
])
# y coordinates of the bottoms of the stacks
bankYbots = [None,
    bankHeight/2-3*(buffin+2*thickness)-1.75*(scales[1]/2+scales[3]+scales[2]),
    bankHeight/2-2*(buffin+2*thickness)-1.75*(scales[2]/2+scales[3]),
    bankHeight/2-1*(buffin+2*thickness)-1.75*(scales[3]/2)
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
    # Draw a horizontal ship centered at x,y
    # with orientation matching the owner
    scale = scales[ship.piece.size]
    if ship.player == 1:
        scale *= -1
    plt.gca().add_patch(plt.Polygon(
        scale*htri+[x,y] ,
        facecolor=rgb[ship.piece.color],
        edgecolor='k',
        linewidth=2,
    ))
    sgn = 2*(ship.player==1) - 1
    for i in range(ship.piece.size):
        plt.plot(x-scale*7/8-sgn*0.2,y-sgn*i/6,'ko',markersize=pipsize)

def drawPiece(piece,x,y):
    # Draw a piece centered at x,y vertically (sitting in the bank)
    scale = scales[piece.size]
    plt.gca().add_patch(plt.Polygon(
        scale*vtri+[x,y] ,
        facecolor=rgb[piece.color],
        edgecolor='k',
        linewidth=2,
    ))
    for i in range(piece.size):
        plt.plot(x-i/6,y-scale*7/8+0.2,'ko',markersize=pipsize)

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

def drawCol(col,x,homeOnMove=None):
    # list of systems to draw
    # x coordinate at which to draw
    # homeOnMove 0 or 1 if this is a home row and that player is on-move
    # Returns the height of the col
    height = 0
    for sys in col:
        for ship in sys.ships:
            height += scales[ship.piece.size]
        for marker in sys.markers:
            height += scales[marker.size]
        # A little extra for the system label
        height += buffin*(len(sys.ships)+len(sys.markers))
    height += buffout*(len(col)-1)
    if homeOnMove is not None:
        height += 2*turnTokenRadius + buffin
    # y is the bottom of the next object to draw
    y = -height/2
    if homeOnMove == 1:
        # Draw the token on bottom
        drawTurnToken(x,y+turnTokenRadius)
        y += 2*turnTokenRadius + buffin
    for sys in col:
        # Ships on the left
        ships = [s for s in sys.ships if s.player == 0]
#        placement.shipSort(ships)
        ships.sort()
        for ship in ships:
            scale = scales[ship.piece.size]
            drawShip(ship,x,y+scale/2)
            y += scale+buffin
        markers = sys.markers
        markers.sort(reverse=True)
        label = sys.name
        for marker in sys.markers:
            scale = scales[marker.size]
            drawMarker(marker,x,y+scale/2)
            y += scale+buffin
        plt.text(x,y,label,fontsize=14,ha='center',va='center')
        y += buffin
        ships = [s for s in sys.ships if s.player == 1]
        ships.sort(reverse=True)
        for ship in ships:
            scale = scales[ship.piece.size]
            drawShip(ship,x,y+scale/2)
            y += scale + buffin
        y += buffout - buffin
    if homeOnMove == 0:
        # Draw the token on the right
        y -= buffout - buffin
        drawTurnToken(x,y+turnTokenRadius)
    return height

def drawState(state,fname=None):
    # Draws the currents state of a Binary HW game
    drawStash(state.stash)
    cols = placement.systemSort(state.systems)
    ncols = len(cols)
    # Determine if token should be drawn for player 0
    if ncols > 1 and state.onmove == 1:
        token = 0
    else:
        token = None
    # Start with height of stash
    height = bankHeight
    if ncols > 0:
        height = max(height,drawCol(cols[ncols-1],(ncols-0.5)*colWidth,token))
    for i in range(ncols-2,0,-1):
        height = max(height,drawCol(cols[i],(ncols-i-0.5)*colWidth))
    # Determine if token should be drawn for player 1
    if ncols > 1 and state.onmove == 0:
        token = 1
    else:
        token = None
    if ncols > 1:
        height = max(height,drawCol(cols[0],colWidth/2,token))
    height += 2*margin

    width = 4+5*buffin+ncols*colWidth
    plt.xlim(-bankWidth,width-bankWidth)
    plt.ylim(-height/2,height/2)
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
        x = c*(1+buffin) - 3.5 - buffin*4
        for size in range(1,4):
            # y coord of center of bottom piece in this stack
            boty = bankYbots[size]
            piece = Piece(size,c)
            for i in range(stash.pieces[c][size]):
                drawPiece(piece,x,boty+i*thickness)

if __name__=='__main__':
    if 0:
        # Ship test
        s = Ship(Piece(3,color.BLUE),0)
        drawShip(s,0,0)
        plt.show()
    if 0:
        # Star marker test
        marker = Piece(3,color.BLUE)
        drawMarker(marker,0,0)
        plt.show()
    if 1:
        from hwstate import HWState
        from text2turn import applyTextTurn as att
        state = HWState()
        i=0
        drawState(state,"../stateImages/game{}.png".format(i))
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



