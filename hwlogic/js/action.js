
/*
From the Python version, Event has been renamed Action
Event is a JS thing

Events are actions, catastrophes, and fadings (caused by a system marker disappearing)

Most of the rule checking is done by these classes or by Turn

ALL STASH REQUESTS HAPPEN HERE

When ships are removed, they continue to remember where they were
This simplifies undoing and redoing
*/

class Action:
    def enact(self,*vargs):
        raise NotImplementedError()
    def undo(self,*vargs):
        raise NotImplementedError()
    # These methods could be variables instead
    def getThreatenedSystem(self):
        # a system (if any) that lost ship(s) or a system marker
        return None
    def getCatThreat(self):
        # a system (if any) that gained a color (and therefore could have a new catastrophe available)
        return None
    def getThreatenedPlayer(self):
        # a list of players that may have just been eliminated
        return None
    def __str__(self):
        raise NotImplementedError()

class Pass(Action):
    def enact(self,state):
        if state.alive[state.onmove] is None:
            raise CreationException('You may not pass your first turn.')
    def undo(self,*vargs):
        pass
    def __str__(self):
        return 'pass'

class Creation(Action):
    # creation of a homeworld
    def __init__(self,markers,ship,name):
        self.ship = ship
        # The markers tracked by the system can change over time, so save the original
        self.markers = list(markers)
        self.system = System(markers,ship.player,name)
    def enact(self,state):
        if state.alive[state.onmove] is not None:
            raise CreationException('Homeworld creation only takes place on your first turn.')
        torequest = [self.ship.piece]+self.system.markers
        try:
            for i in range(len(torequest)):
                p = torequest[i]
                state.stash.request(p)
        except StashOutException as ex :
            # everything up to i was taken
            # put it back and pass the problem up
            for j in range(i):
                p = torequest[j]
                state.stash.putBack(p)
            raise ex

        self.system.addShip(self.ship)
        self.system = self.system
        state.addSystem(self.system)
        state.alive[state.onmove] = True

    def undo(self,state):
        self.system.removeShip(self.ship)
        state.removeSystem(self.system)

        for p in self.system.markers:
            state.stash.putBack(p)
        state.stash.putBack(self.ship.piece)
        state.alive[self.system.home] = None

    def __str__(self):
        return 'homeworld {} {} {} {}'.format(
            self.markers[0],
            self.markers[1],
            self.ship.piece,
            self.system.name
        )

class Action(Action):
    def __init__(self,ship,c,system):
        # the ship that is the subject of this action
        self.ship = ship
        self.color = c
        self.system = system

class RedAction(Action):
    def __init__(self,ship,aggressor,system):
        # aggressor is the attacking player
        Action.__init__(self,ship,color.RED,system)
        self.newShip = Ship(self.ship.piece,aggressor)
    def enact(self,state):
        aggsize = self.system.getLargestShip(self.newShip.player).piece.size
        if aggsize < self.ship.piece.size:
            raise Exception('Attacker must have larger ship in same system.')
        self.system.removeShip(self.ship)
        self.system.addShip(self.newShip)
    def undo(self,state):
        self.system.removeShip(self.newShip)
        self.system.addShip(self.ship)

    def getThreatenedPlayer(self):
        return self.ship.player

    def __str__(self):
        return 'attack {} {}'.format(
            self.ship.piece,
            self.system.name
        )

class YellowAction(Action):
    def __init__(self,ship,system,newsystem):
        Action.__init__(self,ship,color.YELLOW,system)
        self.newsystem = newsystem
        # Home systems may be void without being discoveries
        if not self.system.connectsTo(self.newsystem):
            raise Exception('Systems are not connected.')
    def getThreatenedSystem(self):
        # Player may have abandoned the system
        return self.system
    def getCatThreat(self):
        # Player may have moved into an overpopulation
        return self.newsystem
    def enact(self,state):
        self.newsystem.addShip(self.ship)
        self.system.removeShip(self.ship)
    def undo(self,state):
        self.newsystem.removeShip(self.ship)
        self.system.addShip(self.ship)
    def getThreatenedPlayer(self):
        # This is because you could eliminated yourself by moving away
        return self.ship.player
    def __str__(self):
        return 'move {} {} {}'.format(
            self.ship.piece,
            self.system.name,
            self.newsystem.name
        )
class Discovery(YellowAction):
    def __init__(self,ship,system,markers,name):
        self.markers = list(markers)
        newsystem = System(markers,None,name)
        YellowAction.__init__(self,ship,system,newsystem)
    def enact(self,state):
        YellowAction.enact(self,state)
        # TODO if a multi-star system were ever discovered
        # stashout exceptions would prevent earlier pieces from being returned
        for p in self.newsystem.markers:
            state.stash.request(p)
        state.addSystem(self.newsystem)
    def undo(self,state):
        YellowAction.undo(self,state)
        for p in self.newsystem.markers:
            state.stash.putBack(p)
        state.removeSystem(self.newsystem)
    def __str__(self):
        return 'discover {} {} {} {}'.format(
            self.ship.piece,
            self.system.name,
            self.markers[0],
            self.newsystem.name
        )

class GreenAction(Action):
    def __init__(self,ship,system):
        # Pass the ship whose color permits the new ship to be built
        Action.__init__(self,ship,color.GREEN,system)
        
    def enact(self,state):
        newpiece = state.stash.request(self.ship.piece.color)
        self.newship = Ship(newpiece,self.ship.player)
        self.system.addShip(self.newship)
    def undo(self,state):
        self.system.removeShip(self.newship)
        state.stash.putBack(self.newship.piece)
    def getCatThreat(self):
        # Player may built into an overpopulation
        return self.system
    def __str__(self):
        return 'build {} {}'.format(
            self.newship.piece,
            self.system.name
        )


class BlueAction(Action):
    def __init__(self,ship,c,system):
        Action.__init__(self,ship,color.BLUE,system)
        self.ship = ship
        self.newship = Ship(Piece(ship.piece.size,c),ship.player)
    def enact(self,state):
        state.stash.request(self.newship.piece)
        state.stash.putBack(self.ship.piece)
        self.system.removeShip(self.ship)
        self.system.addShip(self.newship)
    def undo(self,state):
        state.stash.request(self.ship.piece)
        state.stash.putBack(self.newship.piece)
        self.system.removeShip(self.newship)
        self.system.addShip(self.ship)
    def getCatThreat(self):
        # Player may have traded into an overpopulation
        return self.system
    def __str__(self):
        return 'trade {} {} {}'.format(
            self.ship.piece,
            self.newship.piece,
            self.system.name
        )

class Catastrophe(Action):
    def __init__(self,sys,c):
        self.system = sys
        self.color  = c

        self.ships   = [s for s in sys.ships  if s.piece.color == c]
        self.markers = [m for m in sys.markers if m.color == c]

        if len(self.ships) + len(self.markers) < 4:
            raise MissingOverpopulationException('Catastrophes require overpopulation (four or more pieces of the same color).')

    def enact(self,state):
        for ship in self.ships:
            self.system.removeShip(ship)
            state.stash.putBack(ship.piece)
        for marker in self.markers:
            self.system.removeMarker(marker)
            state.stash.putBack(marker)

    def undo(self,state):
        for ship in self.ships:
            self.system.addShip(ship)
            state.stash.request(ship.piece)
        for marker in self.markers:
            self.system.restoreMarker(marker)
            state.stash.request(marker)
    
    def getThreatenedSystem(self):
        return self.system
    def getThreatenedPlayer(self):
        if self.system.home is None:
            return None
        return self.system.home

    def __str__(self):
        return 'catastrophe {} {}'.format(
            self.system.name,
            color.names[self.color]
        )

class Sacrifice(Action):
    # This event is the act of sacrificing a ship
    # The resulting actions can be represented in the Turn
    def __init__(self,ship,system):
        self.ship = ship
        self.system = system
    def enact(self,state):
        self.system.removeShip(self.ship)
        state.stash.putBack(self.ship.piece)
    def undo(self,state):
        self.system.addShip(self.ship)
        state.stash.request(self.ship.piece)
    def getThreatenedSystem(self):
        return self.system
    def getThreatenedPlayer(self):
        if self.system.home is None or self.system.home != self.ship.player:
            return None
        # Otherwise, player is sacrificing a ship at home, which could be suicide
        return self.ship.player

    def __str__(self):
        return 'sacrifice {} {}'.format(
            self.ship.piece,
            self.system.name
        )

/*************************************
* Elimination and Fade are mandatory *
* side-effects of other events       *
*************************************/

class Fade(Action):
    def __init__(self,system):
        self.system = system

    def enact(self,state):
        # There's no real need for remaining ships or markers to be removed from the System model
        # the system just needs to get removed from the State and each Piece needs to be put back in the stash
        state.removeSystem(self.system)
        for marker in self.system.markers:
            state.stash.putBack(marker)
        for ship in self.system.ships:
            state.stash.putBack(ship.piece)
    def undo(self,state):
        state.addSystem(self.system)
        for marker in self.system.markers:
            state.stash.request(marker)
        for ship in self.system.ships:
            state.stash.request(ship.piece)

    def __str__(self):
        return '({} fades)'.format(self.system.name)

class Elimination(Action):
    # The act of removing a player from a game by removing their presence from the homeworld
    def __init__(self,a,b):
        # a eliminated by b
        self.a = a
        self.b = b
    def enact(self,state):
        self.home = state.findHome(self.a)
        self.home.home = None
        state.alive[self.a] = False
    def undo(self,state):
        self.home.home = self.a
        state.alive[self.a] = True

    def __str__(self):
        return '(player {} is eliminated by player {})'.format(self.a,self.b)

