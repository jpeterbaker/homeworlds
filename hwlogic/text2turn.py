
# takes string inputs and provides fully developed Event objects

import color,event,system,piece,ship
import re

wordre = re.compile(r'\w+')

char2color = {'r':color.RED,'y':color.YELLOW,'g':color.GREEN,'b':color.BLUE}

buildTerms = set(['build','b'])
tradeTerms = set(['trade','t'])
attackTerms = set(['attack','a','capture','conquer'])
moveTerms = set(['move','m'])
discoverTerms = set(['discover','d'])
catTerms = set(['catastrophe','c','cat'])
sacTerms = set(['sacrifice','s','sac'])
hwTerms = set(['homeworld','h','hw'])
passTerms = set(['pass','p'])

def getPiece(cs):
    # cs is the color and size of the ship, like 'y3'
    if len(cs) != 2:
        raise Exception('Not a valid piece identifier: "%s"'%cs)
    try:
        return piece.Piece(int(cs[1]),char2color[cs[0].lower()])
    except:
        raise Exception('Not a valid piece identifier: "%s"'%cs)

def getSystem(name,state):
    if len(name) > 15:
        raise Exception('Sorry, system names are limited to 15 characters')
    name = name.upper()
    for sys in state.systems:
        if sys.name.upper() == name:
            return sys
    return None

def getShip(cs,sysName,player,state,opponent=None):
    # If the owner (player) is not known, this function will attempt to infer the ship
    # from a provided opponent. If multiple opponents of "opponent" have a cs ship
    # in the system, this function raises an exception
    sys = getSystem(sysName,state)
    if sys is None:
        raise Exception('No system named {}.'.format(sysName))
    p = getPiece(cs)
    if player is not None:
        for s in sys.ships:
            if s.piece == p and s.player == player:
                return s
        raise Exception('Player {} does not own a {} ship in {}'.format(
            player,cs.lower(),sysName))

    # Player was not specified
    # Find a ship that that is an opponent of "opponent"
    if opponent is None:
        raise Exception('You must specify the player or an opponent.')
    candidate = None
    for s in sys.ships:
        if s.piece == p and s.player != opponent:
            # Found an opponent's ship that matches the description
            if candidate is None:
                candidate = s
            elif candidate.player != s.player:
                # Two opponents have ships of this type
                raise Exception('Multiple opponents have a {} ship in {}'.format(
                    cs,sysName))
    if candidate is None:
        raise Exception('No opponents have a {} ship in {}'.format(
            cs,sysName))
    return candidate

a = ord('A')
alphabet = [chr(a+i) for i in range(26)]
            
def applyTextTurn(s,state):
    # This applies a complete turn to state
    # This does NOT start a new turn or advance the onmove player
    # Returns the resulting turn object
    s = s.strip()
    try:
        textTurnMain(s,state)
    except IndexError as e:
        state.cancelTurn()
        raise Exception('Your gameplay command does not appear to have enough parameters.')
    except Exception as e:
        state.cancelTurn()
        raise e
    state.finishTurn()
    if state.isEnd():
        scores = state.getScores()
        if scores[state.onmove] < 1 and s[-1] != '*':
            # Player who just moved did not win: require confirmation
            state.cancelTurn()
            raise Exception('To confirm that you really want to make a move eliminating yourself, repeat the command with a * at the end.')

    turn = state.curTurn
    if not state.isEnd():
        state.startNewTurn()
    return turn

def textTurnMain(s,state):
    # Main routine for applying text turn
    w = wordre.findall(s)
    n = len(w)

    player = state.onmove
    i = 0

    while i < n:
        w[i] = w[i].lower()
        if w[i] in buildTerms:
            # build ship inSystem
            p = getPiece(w[i+1])
            sysName = w[i+2]
            sys = getSystem(sysName,state)
            if sys is None:
                raise Exception('No system named {}.'.format(sysName))
            for s in sys.ships:
                if s.player == player and s.piece.color == p.color:
                    e = event.GreenAction(s,sys)
                    break
            else:
                # Loop exited normally: no ship of the right color found
                state.cancelTurn()
                raise Exception('You must already own a piece of that color in that system before building one.')

            state.addEvent(e)
            if p.size != e.newship.piece.size:
                state.cancelTurn()
                raise Exception('You cannot build %s while %s is available'%(w[i+1].lower(),e.newship.piece))
            i += 3
        elif w[i] in moveTerms:
            # move ship fromSystem toSystem
            fromSystem = getSystem(w[i+2],state)
            s = getShip(w[i+1],w[i+2],player,state)
            sysName = w[i+3]
            toSys = getSystem(sysName,state)
            if toSys is None:
                raise Exception('No system named {}.'.format(sysName))
            state.addEvent(event.YellowAction(s,fromSystem,toSys))
            i += 4
        elif w[i] in discoverTerms:
            # discover ship fromSystem newStar newName
            try:
                newName = w[i+4]
            except IndexError:
                # User did not provide a name. Find one that isn't already on the board
                for newName in alphabet:
                    if getSystem(newName,state) is None:
                        break
                else:
                    # Loop exited normally, we ran out of letters
                    raise Exception('Ran out of letters. You\'ll have to name the system yourself.')
            if getSystem(newName,state) is not None:
                raise Exception('The {} system already exists.'.format(newName))
            fromSystem = getSystem(w[i+2],state)
            s = getShip(w[i+1],w[i+2],player,state)
            state.addEvent(event.Discovery(s,fromSystem,[getPiece(w[i+3])],newName))
            i += 5
        elif w[i] in tradeTerms:
            # trade oldShip newShip inSystem
            sys = getSystem(w[i+3],state)
            s = getShip(w[i+1],w[i+3],player,state)
            newColor = char2color[w[i+2][0].lower()]
            if int(w[i+2][1]) != s.piece.size:
                state.cancelTurn()
                raise Exception('Traded piece must be the same size.')
            state.addEvent(event.BlueAction(s,newColor,sys))
            i += 4
        elif w[i] in attackTerms:
            # attack ship[owner] inSystem
            sys = getSystem(w[i+2],state)
            if len(w[i+1]) == 2:
                # Owner of opposing ship has not been specified
                # getShip will try to infer it
                s = getShip(w[i+1],w[i+2],None,state,opponent=player)
            elif len(w[i+1]) == 3:
                # Owner of ship is specified by an int appended to ship name
                s = getShip(w[i+1],w[i+2],int(w[i+1][2]),state)
            else:
                raise Exception('Bad target ship specifier.')
            state.addEvent(event.RedAction(s,player,sys))
            i += 3
        elif w[i] in sacTerms:
            # sacrifice ship inSystem
            sys = getSystem(w[i+2],state)
            s = getShip(w[i+1],w[i+2],player,state)
            state.addEvent(event.Sacrifice(s,sys))
            i += 3
        elif w[i] in catTerms:
            # catastrophe inSystem color
            sysName = w[i+1]
            sys = getSystem(sysName,state)
            if sys is None:
                raise Exception('No system named {}.'.format(sysName))
            c = char2color[w[i+2].lower()]
            state.addEvent(event.Catastrophe(sys,c))
            i += 3
        elif w[i] in passTerms:
            # pass
            state.addEvent(event.Pass())
            i += 1
        elif w[i] in hwTerms:
            # homeworld star1 star2 ship name
            try:
                name = w[i+4]
            except IndexError:
                raise Exception('You must give a name to your homeworld.')
            if getSystem(name,state) is not None:
                raise Exception('The {} system already exists.'.format(name))
            markers = [ getPiece(w[i+1]), getPiece(w[i+2]) ]
            s = ship.Ship(getPiece(w[i+3]),player)
            state.addEvent(event.Creation(markers,s,name))
            # Forget about checking for other attempted commands
            # This will allow people to name their homeworld if they're clever enough
            break
        else:
            # There's a problem
            state.cancelTurn()
            raise Exception('Invalid command: "%s"'%w[i])

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

    while len(history) > 0:
        print(state)
        history.pop().undoAll()
    print(state)


