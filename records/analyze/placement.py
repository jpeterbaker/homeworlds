# Tools for arranging pieces nicely on the board
# It's important to me that the result is predictable
# and could be reached by hand if desired
# This is all for Binary Homeworlds

def shipKey(ship):
    return ship.piece.size*4+ship.piece.color

def shipSort(ships):
    # Sort ships for nice placement by the system marker
    # Sort by color (red to blue), then size (large to small)

    # Make sure we don't mess with the system's ship list order
    ships.sort(key=shipKey)
    return ships

def sysKey(system):
    # Sort by pip advantage, player zero's advantage first
    k = 0
    for ship in system.ships:
        k += (2*ship.player-1)*ship.piece.size
    return (k,system.name)

def systemSort(systems):
    '''
    Automatic star towing
    Returns a list of up to 5 lists (rows) of systems
    Each row is intended to be displayed together horizontally as rows

    The row order emphasizes connectivity

    First (top) row is always just the home of player 0
    Bottom row is just the home of player 1
    '''
    homes = [None]*2
    rows = [[] for i in range(3)]
    for sys in systems:
        if sys.home is not None:
            homes[sys.home] = sys
        else:
            rows[sys.markers[0].size-1].append(sys)
    p = optPermute(homes)
    rows = [rows[p[i]] for i in range(3)]

    # Delete empty rows
    rows = [r for r in rows if len(r)>0]

    # Rearrange systems within rows to emphasize player control
    for row in rows:
        row.sort(key=sysKey)
    
    if homes[0] is not None:
        rows = [[homes[0]]] + rows
    if homes[1] is not None:
        rows.append([homes[1]])

    return rows

def optPermute(homes):
    # Returns a permutation for the (possibly empty) rows to emphasize connectivity to homes
    # The returned permutation uses 0,1,2 (not 1,2,3)
    homeConnects = [set((1,2,3)),set((1,2,3))]
    for i in range(2):
        if homes[i] is None:
            continue
        for m in homes[i].markers:
            try:
                homeConnects[i].remove(m.size)
            except KeyError:
                # Gemini star tries to remove same size twice
                pass
    # Number of sizes to which each home connects
    nHC = [len(x) for x in homeConnects]

    # Make it so home 0 connects to no more stars than home 1
    if nHC[0] > nHC[1]:
        return optPermute(homes[::-1])[::-1]

    if nHC[0] == 1:
        s0 = next(iter(homeConnects[0]))
        if nHC[1] == 1:
            # Both systems connect to just one size
            s1 = next(iter(homeConnects[1]))
            if s0 == s1:
                # They connect to the same size
                # Put that size in the middle, the others don't really matter
                return [(s0-2)%3,s0-1,s0%3]
            # Systems connect to different sizes
            # The sum of all three sizes is 6, so the last one is 6-s0-s1
            s2 = 6-s0-s1
            return [s0-1,s2-1,s1-1]
        # The largest size connected to home 1 that does not connect to home 0
        s1 = max(homeConnects[1] - homeConnects[0])
        # The other size
        s2 = 6-s0-s1
        return [s0-1,s2-1,s1-1]

    # Both homes connect to at least two sizes
    i = homeConnects[1]&homeConnects[0]
    if len(i) == 1:
        # The homes connect to two systems each with one in common
        s0 = next(iter(homeConnects[0]-i))
        s2 = next(iter(i))
        s1 = 6-s0-s2
        return [s0-1,s2-1,s1-1]

    if nHC[1] == 2:
        # Both homes connect to the same two sizes
        s0 = min(homeConnects[0])
        s1 = max(homeConnects[0])
        s2 = 6-s0-s1
        return [s0-1,s2-1,s1-1]

    # At least one home is destroyed
    if nHC[0] == 3:
        # Both homes are destroyed
        return [0,1,2]
    # home 1 is destroyed, home 0 is connected to two sizes
    d = homeConnects[1]-homeConnects[0]
    s1 = next(iter(d))
    s0 = min(homeConnects[0])
    s2 = 6-s0-s1
    return [s0-1,s2-1,s1-1]

if __name__=='__main__':
    class Spam:
        def __init__(self,size):
            self.size = size
    class Foo:
        def __init__(self,sizes):
            self.markers = [Spam(x) for x in sizes]
        def __str__(self):
            return '('+','.join([str(x.size) for x in self.markers])+')'

    print("This is bad style, but if you aren't me (the programmer) this file doesn't work as a script")
    import sys
    sys.path.append('/home/jonathan/whome/GoogleDrive/ProjectEuler/lib/')
    from powerset import powerset
    for m0 in powerset(range(1,4),b=2):
        h0 = Foo(m0)
        for m1 in powerset(range(1,4),b=2):
            h1 = Foo(m1)
            p = optPermute([h0,h1])
            print(h0,[x+1 for x in p],h1)

