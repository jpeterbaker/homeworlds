# Like opening_count.py but with color included

import os
import re
from numpy import zeros

bga_create_pat = re.compile(r'^(.*?) establishes a homeworld with a (..) ship at (..) and (..) binary stars\.$')

bga_victory_pat = re.compile(r'^The end of the game: (.*) wins!$')
bga_tie_pat     = re.compile(r'^End of game \(tie\)$')


root_dir = '/mnt/c/Users/Bakers/Documents/hw_replays/'



def readit(full_name):
    '''
    Read a BGA record for the basics
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

# Map opening stars and ships to list of results
results = {}

for root,ds,fs in os.walk(root_dir):
    for fname in fs:
        if not fname.endswith('txt'):
            continue
        full_name = os.path.join(root,fname)
        if not os.path.isfile(full_name):
            # Skip directories
            continue
        try:
            n,s00,s01,ship0,s10,s11,ship1,w = readit(full_name)
        except:
            print('Had trouble with',fname)
            continue
#        ns.append(min(n,1000))
        if n < 100:
            continue
        if s11 is None or w is None:
            continue

        if s00 > s01:
            s00,s01 = s01,s00
        if s10 > s11:
            s10,s11 = s11,s10

        tup = ((s00,s01,ship0),(s10,s11,ship1))
        try:
            results[tup][w] += 1
        except KeyError:
            results[tup] = zeros(3,dtype=int)
            results[tup][w] = 1

def wins_games_rate(r):
    # Returns a tuple
    # wins by player 0
    # winrate of player 0
    # total number of games
    n = sum(r)
    w = r[0] + r[2]/2
    return w, n, w/n

def gemini_test(tupi):
    # Test just one system for gemini-ness
    return tupi[0]==tupi[1]

def large_test(tup):
    if gemini_test(tup[0]) or gemini_test(tup[1]):
        return False
    if tup[0] == tup[1]:
        return False
    return True

def small_test(tup):
    return not (large_test(tup) or micro_test(tup))
    
def micro_test(tup):
    return len(set(tup[0]) & set(tup[1])) == 0

print('P1 winrate , P1 wins , games, starsizes')

overall = zeros(3,dtype=int)

# Number templates
wrtemp = '{:0.3f}'
wtemp  = '{: >8.1f}'
ntemp  = '{:8d}'

for tup,r in results.items():
    w,n,wr = wins_games_rate(r)
    print(wrtemp.format(wr),wtemp.format(w),ntemp.format(n),*tup)
