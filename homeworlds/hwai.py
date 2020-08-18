
'''
TO DEMONSTRATE A BUG:

python hwai.py
load
pass catastrophe Bob g

the Bob system is not removed despite being empty, and the state doesn't match the one produced by typing
see TODO in non-catastrophe section of turn.getContinuations
'''

from numpy import inf
import cPickle
from event import YellowAction,Creation
from hwstate import fromTuple
from sys import path
path.append('../../wordGen/')
from wordGen import genWord

debugging = 1
quietDepth = 2

# This many points for ...
#   every ship you own of that size
sizepts = [0,1,3,7]
#   for every technology you can access at each system
colorpts = 2

def renameSystems(turn):
    # Find discoveries in turn and randomly rename systems
    for event in turn.events:
        if(
            (isinstance(event,YellowAction) and event.isDiscovery)
            or isinstance(event,Creation)
        ):
            pass
#                event.newsystem.setName(genWord())

def save(state,fname):
    tup = state.saveTuple()
    with open(fname,'w') as fout:
        cPickle.dump(tup,fout)

def load(fname):
    with open(fname,'r') as fin:
        stateTuple = cPickle.load(fin)
    return fromTuple(stateTuple)

def staticEval(state):
    scores = [0]*state.nplayers

    if state.isEnd():
        for i in range(state.nplayers):
            if state.alive[i]:
                scores[i] = inf
            else:
                scores[i] = -inf
        return scores

    for sys in state.systems:
        for ship in sys.ships:
            scores[ship.player] += sizepts[ship.piece.size]
        for p in range(state.nplayers):
            if sys.hasPresence(p):
                scores[p] += colorpts*len(sys.getTech(p))

    if state.nplayers == 2:
        scores = [scores[0]-scores[1],scores[1]-scores[0]]

    return scores

def makeAImove(ai):
    computer = ai.root.onmove
    human = 1-computer
    print 'COMPUTER THINKING\n'
    val,state = ai.getGameValBestChild()
    print
    print 'COMPUTER CHOOSES'
    turn = ai.root.getKey(state)
    renameSystems(turn)
    print turn
    print
    ai.advanceByChild(state)
    if val[computer] == inf:
        print 'Computer expects to win'
    elif val[computer] == -inf:
        print 'Computer expects to lose'
    elif val[computer] < val[human]:
        print 'Computer considers itself behind'
    elif val[human] < val[computer]:
        print 'Computer considers itself ahead'
    else:
        print 'Computer considers this an even position'
    print "\nComputer's estimated game value:",val[computer]

def aiOnDemand():
    from sys import path,exit
    from hwstate import HWState
    path.append('..')
    from zeroSum import TwoDepthZeroSumAI as TDZSAI
    import findChoices

    findChoices.allowedSacColors = set([findChoices.RED,findChoices.GREEN])

    root = HWState()
    ai = TDZSAI(root,staticEval,quietDepth=quietDepth)
    over = False
    while not over:
        while not over:
            print ai.root
            print '\nTurn of player',ai.root.onmove
            print """
            'x' to exit
            'save' to save current state to game.pkl
            'load' to load from game.pkl
            'ai' to have AI choose a move
            To make a move, use SDG format"""
            while True:
                c = raw_input().strip()
                if c == 'x':
                    print 'Exiting'
                    exit()
                if c == 'save':
                    save(ai.root,'game.pkl')
                    continue
                if c == 'load':
                    state = load('game.pkl')
                    ai = TDZSAI(state,staticEval,quietDepth=quietDepth)
                    break
                if c == 'ai':
                    makeAImove(ai)
                    break

                if debugging:
                    state = ai.root.getChild(c)
                    ai.advanceByChild(state)
                    break
                # if not debugging
                try:
                    state = ai.root.getChild(c)
                    ai.advanceByChild(state)
                    break
                except Exception as e:
                    print e
                    print 'Try again'
                    continue

            if ai.root.isEnd():
                over = True

    print ai.root
    if ai.root.alive[0] > 0:
        print 'Player 0 wins!'
    elif ai.root.alive[1] > 0:
        print 'Player 1 wins!'
    else:
        print "It's a draw!"
        
if __name__=='__main__':
    aiOnDemand()

