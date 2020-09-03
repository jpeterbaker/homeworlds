'''
Use a string to build a state
Example:

<0> ;
Babamots (0,b2r1)g3 y1-   ;
Bunny    (b1)         -g1 ;
Pib      (1,y3b2)     -g3

<0> means it's player 0's turn
Spaces are allowed in the obvious places
'''

import re
from hwstate import HWState,System
from ship import Ship
from piece import fromTuple as pieceFromTuple
import color

char2color = {'r':color.RED,'y':color.YELLOW,'g':color.GREEN,'b':color.BLUE}

turnRE = r'<\s*(\d)\s*>'

# System regex
# Group 1: system name
# Group 2: number of player whose home this is (if any)
# Group 3: system markers
# Group 4: ships (player groups separated by dashes)
sysRE = r'(\w+)\s*\(\s*(?:(\d),)?((?:[rygb][1-3]\s*)+)\)\s*([-\wrygb1-3 ]*)'

# Each match should be a ship
pieceRE = r'[rygb][1-3]'

def getPieceList(s):
    matches = re.findall(pieceRE,s)
    return [pieceFromTuple( (char2color[m[0]],int(m[1])) ) for m in matches]

def addSystem(s,state):
    # s is the string for a single system (the stuff between semicolons)
    # This function creates the system and ships and takes all pieces from the states stash
    match = re.search(sysRE,s)
    name = match.group(1)
    home = match.group(2)
    markerStr = match.group(3)
    shipsStr = match.group(4)
    if not home is None:
        home = int(home)
    markers = getPieceList(markerStr)
    system = System(markers,home,name)
    state.addSystem(system)
    for m in markers:
        state.stash.request(m)

    playerShipStrs = shipsStr.split('-')
    n = len(playerShipStrs)
    for i in range(n):
        # String representations of the pieces of the ships that belong to player i
        ipieces = getPieceList(playerShipStrs[i])
        for p in ipieces:
            state.stash.request(p)
            ship = Ship(p,i)
            system.addShip(ship)
    return system

def buildState(s):
    systemStrs = s.split(';')
    # The first "system" is the indicator of whose turn it is
    onmove = int(re.search(turnRE,systemStrs[0]).group(1))
    # The number of players should be determinable from the number of dashes separating ships
    n = systemStrs[1].count('-')+1
    state = HWState(n,onmove)
    for ss in systemStrs[1:]:
        sys = addSystem(ss,state)
        if sys.home is not None:
            if sys.hasPresence(sys.home):
                state.alive[sys.home] = True
            else:
                state.alive[sys.home] = False
    return state

if __name__=='__main__':
    import draw
    s = '''
    <1>;
    Babamots(0,r1b2)g3y1-;
    Pib(1,y3b2)-g3g1
    '''
    state = buildState(s)
    draw.drawState(state,'buildStateTest.png')
    print(state.buildStr())

