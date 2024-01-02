
import re

bga_identify_pat = re.compile(r'^(\d*?)=(.*)$')
bga_create_pat = re.compile(r'^(.*?) establishes a homeworld with a (..) ship at (..) and (..) binary stars\.$')

bga_victory_pat = re.compile(r'^The end of the game: (.*) wins!$')
bga_tie_pat     = re.compile(r'^End of game \(tie\)$')

def read_players(full_name):
    '''
    Read early lines of BGA record to identify players
    These records should be in the format I've been downloading with
    the first two lines having the form
        <player number>=<player name>

    Returns a None if the file does not appear formatted correctly
    Otherwise returns ids, which is a pair of pairs
    For i=0,1, ids[i] is the pair (player_number,player_name) of player i,
    where player 0 moves first
    '''

    with open(full_name,'rt') as fin:
        try:
            lines = [next(fin).strip() , next(fin).strip()]
            ps = [None,None]
            for i in range(2):
                match = bga_identify_pat.match(lines[i])
                if match is None:
                    # Lines not formatted correctly
                    return None
                # There is at least one player with a space
                # at the start of their name: " Dionsic"
                # That space doesn't seem to appear in the log, so strip names
                ps[i] = ( int(match.group(1)),match.group(2).strip() )
        except StopIteration:
            # File doesn't have two lines of any kind
            return None
        match = None
        while match is None:
            try:
                line = next(fin).strip()
            except StopIteration:
                # File doesn't have a creation line
                return None
            match = bga_create_pat.match(line)
        name0 = match.group(1)
        if name0 == ps[0][1]:
            # The player listed first moved first, maintain order
            return tuple(ps)
        elif name0 == ps[1][1]:
            # The player listed first moved second, switch the order
            return tuple(ps[::-1])
        # The player name changed between the game and the download
        # Find the other player
        match = None
        while match is None:
            try:
                line = next(fin).strip()
            except StopIteration:
                # File doesn't have a creation line
                return None
            match = bga_create_pat.match(line)
        name1 = match.group(1)
        if name1 == ps[1][1]:
            # The player listed second moved second, maintain order
            return tuple(ps)
        elif name1 == ps[0][1]:
            # The player listed second moved first, switch the order
            return tuple(ps[::-1])
        print('Could not match either player name')
        print(ps)
        print(full_name)

def opening_results(full_name):
    '''
    Read a BGA record for the basics of the opening and the result
    returns a tuple
    (n,star00,star01,ship0,star10,star11,ship1,w)
    n: number of lines in the file
    sstar00,sstar01: the stars of player 0 as strings, e.g. r3
    sstar10,sstar11: the stars of player 1 as strings, e.g. r3
    ship0,ship1: the ships of the players as strings
    w: index of winner (0 or 1 for those players, or 2 if it was a draw)

    everything but n will be None if either player did not complete creation phase
    '''
    n = 0
    s00 = None
    s01 = None
    s10 = None
    s11 = None
    w = None

    # Player names
    p0 = None
    p1 = None
    with open(full_name,'rt') as fin:
        #################
        # Find creation #
        #################
        for line in fin:
            n += 1
            line = line.strip()
            match = bga_create_pat.match(line)
            if match is None:
                continue
            if p0 is None:
                # This is player 0
                p0,ship0,s00,s01 = match.groups()
            else:
                # This is player 1
                p1,ship1,s10,s11 = match.groups()
                break
        if p1 is None:
            return (n,None,None,None,None,None,None,None)
        # Skip to the end
        for line in fin:
            n += 1
        line = line.strip()
        # Analyze last line
        match = bga_victory_pat.match(line)
        if not match is None:
            wname = match.group(1)
            if wname == p0:
                w = 0
            else:
                if wname != p1:
                    print(wname,'is neither',p0,'nor',p1)
                w = 1
        else:
            match = bga_tie_pat.match(line)
            if not match is None:
                w = 2
            else:
                print(f'Last line not understood: "{line}"')
    return (n,s00,s01,ship0,s10,s11,ship1,w)

if __name__=='__main__':
    # Test identification of players
    fname = '/mnt/c/Users/Bakers/Documents/hw_replays/bga398113113.txt'
    p = read_players(fname)
    print(p)
