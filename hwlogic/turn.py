
import event
from itertools import chain,combinations
from hwExceptions import SelfEliminationException,StashOutException

'''
Somehow, the catastrophe loop is removing other events from the turn event list

pass catastrophe Bob g
'''

THEPASS = event.Pass()

def powerset(s,a=0,b=None):
	'''
	s:	iterable
	a:	minimum subset size (default 0)
	b:	maximumsubset size (default len(s))
	Returns all subsets of s with size bewtween a and b
	'''
	s = list(s)
	if b == None:
		b = len(s)
	return chain.from_iterable(combinations(s, r) for r in range(a,b+1))

class Turn:
    def __init__(self,state):
        self.events  = []
        self.state = state

        # Change to True when a sacrifice is made
        #        to False when a free action is made
        self.isSac = None
        # Change to the color of sacrificed ship
        self.colSac = None
        # Change to the number of sacrifice actions available
        self.nSac = None

    def addEvent(self,e):
        # Remember that this event is part of the turn,
        # but its effects are not applied here
        # This method is mostly for tracking whether a sacrifice could occur this turn
        if self.isSac is None:
            # We don't know if this is a sacrifice yet
            if isinstance(e,event.Action):
                # Not a sacrifice
                self.isSac = False
                # Check that this player has access to this color
                if not e.system.hasPresence(self.state.onmove,e.color):
                    raise Exception('In order to take a free action, you must have a ship or system marker of that color.')

            if(
                isinstance(e,event.Pass) or
                isinstance(e,event.Creation)
            ):
                # Not a sacrifice
                self.isSac = False
            elif isinstance(e,event.Sacrifice):
                # Yes a sacrifice
                self.isSac = True
                self.colSac = e.ship.piece.color
                self.nSac = e.ship.piece.size
            # Otherwise, we still don't know if this will be a sacrifice
        elif self.isSac:
            if isinstance(e,event.Pass):
                if self.nSac <= 0:
                    raise Exception('The number of actions (including passes) must be exactly the size of the sacrificed ship.')
                self.nSac -= 1
            elif isinstance(e,event.Action):
                if e.color != self.colSac:
                    raise Exception('Action must correspond to color of sacrificed ship.')
                elif self.nSac <= 0:
                    raise Exception('The number of actions (including passes) must be exactly the size of the sacrificed ship.')
                self.nSac -= 1
        else:
            # This turn is known to be not a sacrifice,
            # so a basic action has been performed,
            # and only a Fade or Catastrophe should be accepted
            if not (
                isinstance(e,event.Catastrophe) or
                isinstance(e,event.Fade) or
                isinstance(e,event.Elimination)
            ):
                raise Exception('You have already used a free action or passed.')
        self.events.append(e)

    def getThreatenedPlayers(self):
        players = set()
        for event in self.events:
            p = event.getThreatenedPlayer()
            if not p is None:
                players.add(p)
        return players

    def enact(self):
        # This should normally only be used for redoing turns
        # Otherwise, Fade and Elimination events
        # (which are only detected by HWState.addEvent)
        # could be missed
        for e in self.events:
            e.enact(self.state)

    def undoLast(self):
        last = self.events.pop()
        last.undo(self.state)
        # Remove all side-effects of last voluntary event
        while (
            len(self.events) > 0
            and (isinstance(last,event.Fade)
                or isinstance(last,event.Elimination)
            )
        ):
            last = self.events.pop()
            last.undo(self.state)
        if self.isSac:
            if isinstance(last,event.Sacrifice):
                # The sacrifice was undone
                # This may not be a sacrifice turn anymore
                self.isSac = None
                self.colSac = None
                self.nSac = None
            elif(
                isinstance(last,event.Action) or
                isinstance(last,event.Pass)
            ):
                # Got a sacrifice action back
                self.nSac += 1
        elif not self.isSac is None:
            if (isinstance(last,event.Action)
                or isinstance(last,event.Pass)
                or isinstance(last,event.Creation)
            ):
                # If a Pass or Action is undone,
                # then we no longer know if this is a sacrifice Turn
                self.isSac = None

    def undoAll(self):
        for i in range(len(self.events)):
            self.events.pop().undo(self.state)
        self.isSac = None
        self.colSac = None
        self.nSac = None

    def isCompleted(self):
        # True if this Turn is not expecting another Event
        if self.isSac is None:
            # No free Action or Sacrifice has been added
            return False
        if self.isSac:
            # This was a turn with a Sacrifice: make sure every point was used
            return self.nSac == 0
        # This was not a sacrifice turn,
        # and a free Action must have been used since self.isSac was set
        return True

    def deepCopy(self):
        # Makes a copy of this list that's deep enough for my purposes
        copy = Turn(None)
        copy.events = list(self.events)
        return copy

    def isEmpty(self):
        return len(self.events) == 0

    def __str__(self):
        if len(self.events) == 0:
            return '[No events have been added to this turn]'
        # Don't list the Eliminations and Fades since they are just side effects
        return '\n   '.join([
            str(e)
            for e in self.events
            if  not isinstance(e,event.Fade)
            and not isinstance(e,event.Elimination)])
        


