#!/usr/bin/python3.9
# Tools for drawing a state HORIZONTALLY
from sys import path
from os import path as ospath
path.append(ospath.join(ospath.dirname(__file__),'../../hwlogic/'))
import color
from ship import Ship
from piece import Piece
import placement

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use( 'tkagg' )
import numpy as np

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

    ####################
    # Calculate height #
    ####################
    # Reserve room for the token on the other side to keep pieces centered
    if homeOnMove == 1:
        height = turnTokenRadius*2+buffin
    elif homeOnMove == 0:
        height = -turnTokenRadius*2-buffin
    else:
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
        # height started negative and could cause token to get cut off
        # if this is the tallest column
        height += 4*turnTokenRadius+2*buffin
    return height

def drawState(state,fname=None):
    # Draws the currents state of a Binary HW game
    drawStash(state.stash)
    cols = placement.systemSort(state.systems)
    ncols = len(cols)
    # Determine if token should be drawn for player 0
    if state.onmove == 1 and ncols > 1 and not state.isEnd():
        token = 0
    else:
        token = None
    # Start with height of stash
    height = bankHeight
    if ncols > 0:
        height = max(height,drawCol(cols[ncols-1],(ncols-0.5)*colWidth,token))
    for i in range(ncols-2,0,-1):
        height = max(height,drawCol(cols[i],(i+0.5)*colWidth))
    # Determine if token should be drawn for player 1
    if state.onmove == 0 and ncols > 1 and not state.isEnd():
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

helpstr = '''
    USAGE:

python drawH.py <image output template>

    Then, type the initial game state in buildState.py format
    followed by any moves you want to make.
    Lines with # as first character are ignored

    First non-empty, non-comment line must be a turn string or a state string

    EXAMPLE:

python drawH.py ../stateImages/bill_vs_susie.png < exampleGame.txt

    The result is the writing of images described by exampleGame.txt.
    The image files will be named
        ../stateImages/bill_vs_susie0.png
        ../stateImages/bill_vs_susie1.png
        etc.
'''
if __name__=='__main__':
    from sys import argv
    if len(argv) != 2:
        print(helpstr)
        exit()
    from os import path
    from hwstate import HWState
    from text2turn import applyTextTurn as att

    from sys import stdin
    from buildState import buildState

    fname = path.abspath(argv[1])
    i = fname.rfind('.')
    if i <= 0:
        print('You need to use a file extension for name templating to work')
        exit()
        
    fname_template = ''.join([fname[:i],'_{}',fname[i:]])

    lines = [line.strip() for line in stdin]
    nlines = len(lines)
    # value of first is used to mark our spot after checking for initial state
    for first in range(nlines):
        line = lines[first]
        if len(line) == 0:
            # Blank
            continue
        if line[0] == '#':
            # Comment
            continue
        if line[0] == '<':
            # Initial state specification
            # Get all the consecutive lines that end in semicolon
            # and interpret them as a state
            print('starting initial')
            initials = []
            for first in range(first,nlines):
                line = lines[first]
                initials.append(line)
                print('loop line')
                print(line)
                if line[-1] != ';':
                    # This is the last state line
                    print('does not end with ;')
                    break
                print('ends with ;')
            print(initials)
            state_str = '\n'.join(initials)
            state = buildState(state_str)
            print('Starting with initial state')
            print(state_str)
            break
        else:
            # Something else, hopefully a valid first turn
            print('Starting with blank state')
            state = HWState()
            att(line,state)
            break

    suffix = 'ab'
    moves = 2
    if state.onmove != 0:
        moves += 1

    fout_name = fname_template.format('{}{}'.format(moves//2,suffix[moves%2]))
    print('drawing in',fout_name)
    drawState(state,fout_name)
    moves += 1

    for line in lines[first+1:]:
        if len(line) == 0 or line[0] == '#':
            continue
        print(line)
        att(line,state)
        fout_name = fname_template.format('{}{}'.format(moves//2,suffix[moves%2]))
        drawState(state,fout_name)
        moves += 1

