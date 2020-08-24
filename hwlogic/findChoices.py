# Produces lists of available turn Events from state information

import piece,event
from ship import Ship
from system import System
from color import colors,RED,YELLOW,GREEN,BLUE

# For testing, it may be useful to disallow yellow and even blue sacrifices
allowedSacColors = set([RED,YELLOW,GREEN,BLUE])

def getCreations(state):
    creates = []
    for shipi in range(12):
        # TODO this assumes colors are ints
        shipp = piece.Piece(shipi//4+1,shipi%4)
        ship = Ship(shipp,state.onmove)
        for mark0i in range(12):
            mark0p = piece.Piece(mark0i//4+1,mark0i%4)
            for mark1i in range(mark0i,12):
                mark1p = piece.Piece(mark1i//4+1,mark1i%4)
                sys = System([mark0p,mark1p],state.onmove)
                creates.append(event.Creation(sys,ship))
    return creates


def getActions(state,c=None,sys=None):
    '''
    Returns a list of Actions that could be performed by current player
    getActions()
        Free actions in any system (using colors available in the system)
    getActions(c)
        Actions of type c in any system
        Color should be available from a sacrifice or as a tech in the system
    getActions(sys=sys)
        Actions in the system sys using any available technology in sys
    getActions(c,sys)
        Actions of type c in the system sys
        Color should be available from a sacrifice or as a tech in the system
    '''
    actions = []
    ##############################################
    # Color not specified: find all free actions #
    ##############################################
    if c is None:
        if sys is None:
            # System not specified: try all systems
            for sys in state.systems:
                for c in sys.getTech(state.onmove):
                    actions.extend(getActions(state,c,sys))
        else:
            # System specified: try all available colors
            for c in sys.getTech(state.onmove):
                actions.extend(getActions(state,c,sys))
        return actions
    ###################################
    # Color specified: find all ships #
    ###################################
    if sys is None:
        # System not specified: iterate over all systems
        systems = state.systems
    else:
        # Iterate over just specified system
        systems = [sys]
    for sys in systems:
        if not sys.hasPresence(state.onmove):
            continue
        if c == RED:
            largest = sys.getLargestShip(state.onmove)
            targets = set([s for s in sys.ships if s.player != state.onmove
                                         and s.piece.size <= largest.piece.size])
            attacks = [event.RedAction(s,state.onmove,sys) for s in targets]
            actions.extend(attacks)
        elif c == YELLOW:
            destinations = state.getConnections(sys)
            for s in sys.ships:
                if s.player != state.onmove:
                    continue
                moves = [event.YellowAction(s,sys,d) for d in destinations]
                actions.extend(moves)
        elif c == GREEN:
            techs = set([s.piece.color for s in sys.ships
                           if s.player == state.onmove])
            for tech in techs:
                smallSize = state.stash.querySmallest(tech)
                if smallSize is None:
                    continue
                p = piece.Piece(smallSize,tech)
                ship = Ship(p,state.onmove)
                actions.append(event.GreenAction(ship,sys))
        elif c == BLUE:
            ships = set([s for s in sys.ships if s.player == state.onmove])
            for ship in ships:
                for cnew in colors:
                    if cnew == ship.piece.color:
                        continue
                    if state.stash.isAvailable(cnew,ship.piece.size):
                        actions.append(event.BlueAction(ship,cnew,sys))
        # End of color cases
    # End of loop over systems
    return actions

def getSacrifices(state):
    sacs = []
    for sys in state.systems:
        for ship in sys.ships:
            if ship.player != state.onmove:
                continue
            if not ship.piece.color in allowedSacColors:
                continue
            sacs.append(event.Sacrifice(ship,sys))
    return sacs

if __name__=='__main__':
    import hwstate
    from text2turn import applyTextTurn,getSystem,getShip
    state = hwstate.HWState()
    # 1
    applyTextTurn('homeworld b1 r2 g3 Wunderland',state)
    applyTextTurn('homeworld g3 r1 b3 Jome',state)
    # 2
    applyTextTurn('build g1 Wunderland',state)
    applyTextTurn('build b1 Jome',state)
    # 3
    applyTextTurn('trade g1 b1 Wunderland',state)
    applyTextTurn('build b2 Jome',state)
    # 4
    applyTextTurn('build b2 Wunderland',state)
    applyTextTurn('trade b2 y2 Jome',state)
    '''
    # 5
    applyTextTurn('trade b1 y1 Wunderland',state)
    applyTextTurn('discover b1 Jome y2 HSOJ',state)
    # 6
    applyTextTurn('discover b2 Wunderland g3 Pepperland',state)
    applyTextTurn('build b1 Jome',state)
    # 7
    applyTextTurn('build b2 Pepperland',state)
    applyTextTurn('discover b1 Jome g2 JOHS',state)
    # 8
    applyTextTurn('trade b2 y2 Pepperland',state)
    applyTextTurn('build b2 JOHS',state)
    # 9
    applyTextTurn('build y1 Wunderland',state)
    applyTextTurn('build b2 Jome',state)
    # 10
    applyTextTurn('build b3 Pepperland',state)
    applyTextTurn('sacrifice y2 Jome move b1 JOHS Pepperland move b1 HSOJ Pepperland catastrophe Pepperland b',state)
    # 11
    applyTextTurn('trade y1 b1 Wunderland',state)
    applyTextTurn('build b1 JOHS',state)
    # 12
    applyTextTurn('move b1 Wunderland Pepperland',state)
    applyTextTurn('trade b2 y2 Jome',state)
    # 13
    applyTextTurn('build b2 Pepperland',state)
    applyTextTurn('build b2 Jome',state)
    # 14
    applyTextTurn('discover b2 Pepperland y2 Narnia',state)
    applyTextTurn('trade b2 r2 Jome',state)
    # 15
    applyTextTurn('trade b1 r1 Pepperland',state)
    applyTextTurn('build b1 Jome',state)
    # 16
    applyTextTurn('build g1 Wunderland',state)
    applyTextTurn('discover b1 Jome g2 J?',state)
    # 17
    applyTextTurn('build g1 Wunderland',state)
    applyTextTurn('trade b2 g2 JOHS',state)
    # 18
    applyTextTurn('discover g1 Wunderland y3 Neverland',state)
    applyTextTurn('build b2 JOHS',state)
    # 19
    applyTextTurn('build g1 Neverland',state)
    applyTextTurn('sacrifice g2 JOHS build b2 Jome build b3 J?',state)
    # 20
    applyTextTurn('sacrifice g3 Wunderland build g2 Neverland build b3 Narnia build g3 Wunderland',state)
    applyTextTurn('trade b3 y3 Jome',state)
    # 21
    applyTextTurn('trade b3 y3 Narnia',state)
    applyTextTurn('move y2 Jome J?',state)
    # 22
    applyTextTurn('sacrifice g3 Wunderland build g3 Wunderland build y1 Wunderland build y1 Pepperland',state)
    applyTextTurn('move b3 J? Pepperland',state)
    # 23
    applyTextTurn('sacrifice y2 Pepperland discover y1 Pepperland y2 MiddleEarth move r1 Pepperland MiddleEarth',state)
    applyTextTurn('build b3 Pepperland',state)
    # 24
    applyTextTurn('sacrifice g3 Wunderland build g3 Wunderland build r1 MiddleEarth build b3 Narnia',state)
    applyTextTurn('trade b3 r3 Pepperland',state)
    # 25
    applyTextTurn('discover y1 Wunderland b3 Pern',state)
    applyTextTurn('sacrifice y2 J? move r3 Pepperland Wunderland move b3 Pepperland Wunderland',state)
    # 26
    applyTextTurn('sacrifice y3 Narnia move r1 MiddleEarth Jome move r1 MiddleEarth Jome pass catastrophe Jome r',state)
    '''
    # Skip the last move of the game for analysis

    # Apply part of the turn that's creating problems
    print('Starting state')
    print(state)

#    import cProfile
#    cProfile.run('children = state._getChildren()',sort='tottime')
    
    children = state._getChildren()
    children.sort()
    print('%s child states generated'%len(children))
#    for child in children:
#        print(child.tuplify())
#        print(child)
    print('%s unique child states generated'%len(set(children)))

