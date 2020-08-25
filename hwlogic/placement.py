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
    return key

def systemSort(systems):
    '''
    Automatic star towing
    Returns a list of up to 5 lists (rows) of systems
    Each row is intended to be displayed together horizontally

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
    # Delete empty rows
    rows = [r for r in rows if len(r)>0]

    # Rearrange rows to emphasize connectivity
    # TODO Make it good for non-large universes
    for i in range(len(rows)):
        if homes[0] is not None and rows[i][0].connectsTo(homes[0]):
            rows[i],rows[0] = rows[0],rows[i]
        elif homes[1] is not None and rows[i][0].connectsTo(homes[1]):
            rows[i],rows[-1] = rows[-1],rows[i]

    # Rearrange systems within rows to emphasize player control
    for row in rows:
        row.sort(key=sysKey)
    
    if homes[0] is not None:
        rows = [[homes[0]]] + rows
    if homes[1] is not None:
        rows.append([homes[1]])

    return rows

