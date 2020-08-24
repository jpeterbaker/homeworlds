
# takes string inputs and provides fully developed Event objects

import color,event,system,piece,ship
import re

wordre = re.compile(r'[\w]+')

char2color = {'r':color.RED,'y':color.YELLOW,'g':color.GREEN,'b':color.BLUE}

buildTerms = set(['build','b'])
tradeTerms = set(['trade','t'])
attackTerms = set(['attack','a'])
moveTerms = set(['move','m'])
discoverTerms = set(['discover','d'])
catTerms = set(['catastrophe','c','cat'])
sacTerms = set(['sacrifice','s','sac'])
hwTerms = set(['homeworld','h','hw'])
passTerms = set(['pass','p'])
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
    print(state)
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
    print(s)
    w = wordre.findall(s)
    n = len(w)

    player = state.onmove

    i = 0

    while i < n:
        w[i] = w[i].lower()
        if w[i] in buildTerms:
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
        elif w[i] in moveTerms:
            # move ship fromSystem toSystem
            fromSystem = getSystem(w[i+2],state)
            s = getShip(w[i+1],w[i+2],player,state)
            toSys = getSystem(w[i+3],state)
            state.addEvent(event.YellowAction(s,fromSystem,toSys))
            i += 4
        elif w[i] in discoverTerms:
            # discover ship fromSystem newStar newName
            fromSystem = getSystem(w[i+2],state)
            s = getShip(w[i+1],w[i+2],player,state)
            newSys = system.System([getPiece(w[i+3])],None,w[i+4])
            state.addEvent(event.YellowAction(s,fromSystem,newSys))
            i += 5
        elif w[i] in tradeTerms:
            # trade oldShip newShip inSystem
            sys = getSystem(w[i+3],state)
            s = getShip(w[i+1],w[i+3],player,state)
            newColor = char2color[w[i+2][0].lower()]
            if int(w[i+2][1]) != s.piece.size:
                state.cancelTurn()
                raise Exception('Traded piece must be the same size')
            state.addEvent(event.BlueAction(s,newColor,sys))
            i += 4
        elif w[i] in attackTerms:
            # attack ship owner inSystem
            sys = getSystem(w[i+3],state)
            s = getShip(w[i+1],w[i+3],int(w[i+2]),state)
            state.addEvent(event.RedAction(s,player,sys))
            i += 4
        elif w[i] in sacTerms:
            # sacrifice ship inSystem
            sys = getSystem(w[i+2],state)
            s = getShip(w[i+1],w[i+2],player,state)
            state.addEvent(event.Sacrifice(s,sys))
#            print('after sacrifice')
#            print(state.stash)
            i += 3
        elif w[i] in catTerms:
            # catastrophe inSystem color
            sys = getSystem(w[i+1],state)
            c = char2color[w[i+2].lower()]
            state.addEvent(event.Catastrophe(sys,c))
            i += 3
        elif w[i] in passTerms:
            # pass
            state.addEvent(event.Pass())
            i += 1
        elif w[i] in hwTerms:
            # homeworld star1 star2 ship name
            sys = system.System(
                [
                    getPiece(w[i+1]),
                    getPiece(w[i+2])
                ],
                player,
                w[i+4]
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
    turn = state.curTurn
    state.startNewTurn()
    return turn

if __name__=='__main__':
    import hwstate

    state = hwstate.HWState(2)
    history = []
    with open('looneyVcooper.txt','r') as fin:
        for line in fin:
            line = line.strip()
            if len(line) == 0:
                continue
            history.append(applyTextTurn(line,state))

    assert(state._isEnd())
    print('GAME OVER')

#    toprint = set([1,5,9,10,15,19,20,23,24,25])
#    # Now try undoing it all
#    for i in range(26,0,-1):
#        if i in toprint:
#            print(i)
#            print(state)
#            print(state.stash)
#        print('Undoing',i)
#        for j in [0,1]:
#            history.pop().undoAll()
    while len(history) > 0:
        print(state)
        history.pop().undoAll()
    print(state)


