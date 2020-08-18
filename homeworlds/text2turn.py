
# takes string inputs and provides fully developed Event objects

import color,event,system,piece,ship

char2color = {'r':color.RED,'y':color.YELLOW,'g':color.GREEN,'b':color.BLUE}

# TODO make getShip take a system instead of a name

def getPiece(cs):
    # cs is the color and size of the ship, like 'y3'
    if len(cs) != 2:
        raise Exception('Not a valid ship identifier: "%s"'%cs)
    try:
        return piece.Piece(int(cs[1]),char2color[cs[0].lower()])
    except:
        raise Exception('Not a valid ship identifier: "%s"'%cs)

def getSystem(name,state):
    for sys in state.systems:
        if sys.name == name:
            return sys
    print state
    raise Exception('No such system: "%s"'%name)

def getShip(cs,sysName,player,state):
    sys = getSystem(sysName,state)
    p = getPiece(cs)
    for s in sys.ships:
        if s.piece == p and s.player == player:
            return s
    raise Exception('You do not own a %s ship in %s'%(cs.lower(),sysName))

def applyTextTurn(s,state):
    # This applies a complete turn to state
    # This does NOT start a new turn or advance the onmove player
    # If you want the turn object, take state.curTurn

    # TODO check for duplicate system names
    
    w = s.split(' ')
    n = len(w)

    player = state.onmove

    i = 0

    while i < n:
        if w[i].lower() == 'build':
            # build ship inSystem
            p = getPiece(w[i+1])
            sys = getSystem(w[i+2],state)
            for s in sys.ships:
                if s.player == player and s.piece.color == p.color:
                    e = event.GreenAction(s,sys)
                    break
            else:
                # Loop exited normally: no ship of the right color found
                state.cancelTurn()
                raise Exception('You must already own a piece of that color in that system before building one')

            state.addEvent(e)
            if p.size != e.newship.piece.size:
                state.cancelTurn()
                raise Exception('You cannot build %s while %s is available'%(w[i+1].lower(),e.newship.piece))
            i += 3
        elif w[i].lower() == 'move':
            # move ship fromSystem toSystem
            fromSystem = getSystem(w[i+2],state)
            s = getShip(w[i+1],w[i+2],player,state)
            toSys = getSystem(w[i+3],state)
            state.addEvent(event.YellowAction(s,fromSystem,toSys))
            i += 4
        elif w[i].lower() == 'discover':
            # discover ship fromSystem newStar newName
            fromSystem = getSystem(w[i+2],state)
            s = getShip(w[i+1],w[i+2],player,state)
            newSys = system.System([getPiece(w[i+3])],None,system.Name(w[i+4]))
            state.addEvent(event.YellowAction(s,fromSystem,newSys))
            i += 5
        elif w[i].lower() == 'trade':
            # trade oldShip newShip inSystem
            sys = getSystem(w[i+3],state)
            s = getShip(w[i+1],w[i+3],player,state)
            newColor = char2color[w[i+2][0].lower()]
            if int(w[i+2][1]) != s.piece.size:
                state.cancelTurn()
                raise Exception('Traded piece must be the same size')
            state.addEvent(event.BlueAction(s,newColor,sys))
            i += 4
        elif w[i].lower() == 'attack':
            # attack ship owner inSystem
            sys = getSystem(w[i+3],state)
            s = getShip(w[i+1],w[i+3],int(w[i+2]),state)
            state.addEvent(event.RedAction(s,player,sys))
            i += 4
        elif w[i].lower() == 'sacrifice':
            # sacrifice ship inSystem
            sys = getSystem(w[i+2],state)
            s = getShip(w[i+1],w[i+2],player,state)
            state.addEvent(event.Sacrifice(s,sys))
#            print 'after sacrifice'
#            print state.stash
            i += 3
        elif w[i].lower() == 'catastrophe':
            # catastrophe inSystem color
            sys = getSystem(w[i+1],state)
            c = char2color[w[i+2].lower()]
            state.addEvent(event.Catastrophe(sys,c))
            i += 3
        elif w[i].lower() == 'pass':
            # pass
            state.addEvent(event.Pass())
            i += 1
        elif w[i].lower() == 'homeworld':
            # homeworld star1 star2 ship name
            sys = system.System(
                [
                    getPiece(w[i+1]),
                    getPiece(w[i+2])
                ],
                player,
                system.Name(w[i+4])
            )
            s = ship.Ship(getPiece(w[i+3]),player)
            state.addEvent(event.Creation(sys,s))
            i += 5
        else:
            # There's a problem
            state.cancelTurn()
            raise Exception('Invalid command: "%s"'%w[i])
    if not state.curTurn.isCompleted():
        raise TurnNotOverException('Turn is not complete. Did you forget to pass?')

    state.finishTurn()

if __name__=='__main__':
    import hwstate

    state = hwstate.HWState(2)
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
    # 5
    applyTextTurn('trade b1 y1 Wunderland',state)
    applyTextTurn('discover b1 Jome y2 HSOJ',state)
#    print '5'
#    print state
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
#    print '9'
#    print state
    # 10
    applyTextTurn('build b3 Pepperland',state)
    applyTextTurn('sacrifice y2 Jome move b1 JOHS Pepperland move b1 HSOJ Pepperland catastrophe Pepperland b',state)
#    print '10'
#    print state
#    print state.stash
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
#    print '15'
#    print state
    # 16
    applyTextTurn('build g1 Wunderland',state)
    applyTextTurn('discover b1 Jome g2 J?',state)
    # 17
    applyTextTurn('build g1 Wunderland',state)
    applyTextTurn('trade b2 g2 JOHS',state)
    # 18
    applyTextTurn('discover g1 Wunderland y3 Neverland',state)
    applyTextTurn('build b2 JOHS',state)
#    print '18'
#    print state
    # 19
    applyTextTurn('build g1 Neverland',state)
    applyTextTurn('sacrifice g2 JOHS build b2 Jome build b3 J?',state)
#    print '19'
#    print state
    # 20
    applyTextTurn('sacrifice g3 Wunderland build g2 Neverland build b3 Narnia build g3 Wunderland',state)
    applyTextTurn('trade b3 y3 Jome',state)
#    print '20'
#    print state
    # 21
    applyTextTurn('trade b3 y3 Narnia',state)
    applyTextTurn('move y2 Jome J?',state)
    # 22
    applyTextTurn('sacrifice g3 Wunderland build g3 Wunderland build y1 Wunderland build y1 Pepperland',state)
    applyTextTurn('move b3 J? Pepperland',state)
    # 23
    applyTextTurn('sacrifice y2 Pepperland discover y1 Pepperland y2 MiddleEarth move r1 Pepperland MiddleEarth',state)
    applyTextTurn('build b3 Pepperland',state)
#    print '23'
#    print state
    # 24
#    applyTextTurn('build b3 Narnia',state) # Should give an error since there is no green in Narnia
    applyTextTurn('sacrifice g3 Wunderland build g3 Wunderland build r1 MiddleEarth build b3 Narnia',state)
    applyTextTurn('trade b3 r3 Pepperland',state)
#    print '24'
#    print state
    # 25
    applyTextTurn('discover y1 Wunderland b3 Pern',state)
    applyTextTurn('sacrifice y2 J? move r3 Pepperland Wunderland move b3 Pepperland Wunderland',state)
#    print '25'
#    print state
    # 26
    applyTextTurn('sacrifice y3 Narnia move r1 MiddleEarth Jome move r1 MiddleEarth Jome pass catastrophe Jome r',state)
    applyTextTurn('sacrifice r3 Wunderland attack g3 0 Wunderland attack y1 0 Wunderland attack g1 0 Wunderland',state)

    assert(state._isEnd())
    print 'GAME OVER'

    toprint = set([1,5,9,10,15,19,20,23,24,25])
    # Now try undoing it all
    for i in range(26,0,-1):
        if i in toprint:
            print i
            print state
            print state.stash
        print 'Undoing',i
        for j in [0,1]:
            history.pop().undoAll()
    print state


