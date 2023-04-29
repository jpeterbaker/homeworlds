'''
Elementary analysis of the game logs I've downloaded.
What were the homeworlds like, how many turns took place, and who won.
'''

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
    (n,s00,s01,s10,s11,w)
    n: number of lines in the file
    s00,s01: the stars of player 0 as strings, e.g. r3
    s10,s11: the stars of player 1 as strings, e.g. r3
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
                p0,_,s00,s01 = match.groups()
            else:
                # This is player 1
                p1,_,s10,s11 = match.groups()
                break
        if p1 is None:
            return (n,None,None,None,None,None)
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
    return (n,s00,s01,s10,s11,w)

# Count of game lengths
#ns = []

# Map opening star SIZES to list of results
# For each player, sizes are listed in non-decreasing order
# results[((ss00,ss01),(ss10,ss11))] is a list of three values
# First entry is the number of wins for player 0
# Second entry is the number of wins for player 1
# Third entry is the number of draws
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
            n,s00,s01,s10,s11,w = readit(full_name)
        except:
            print('Had trouble with',fname)
            continue
#        ns.append(min(n,1000))
        if n < 100:
            continue
        if s11 is None or w is None:
            continue
        ss00 = int(s00[1])
        ss01 = int(s01[1])
        ss10 = int(s10[1])
        ss11 = int(s11[1])

        if ss00 > ss01:
            ss00,ss01 = ss01,ss00
        if ss10 > ss11:
            ss10,ss11 = ss11,ss10

        tup = ((ss00,ss01),(ss10,ss11))
        try:
            results[tup][w] += 1
        except KeyError:
            results[tup] = zeros(3,dtype=int)
            results[tup][w] = 1

def winrate(r):
    # Winrate percentage and total number of games
    n = sum(r)
    return (r[0]+r[2]/2)/n , n

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

print('Winrate of first player , number of games played , starsizes')

overall = zeros(3,dtype=int)
large   = zeros(3,dtype=int)
small   = zeros(3,dtype=int)
micro   = zeros(3,dtype=int)

for tup,r in results.items():
    wr,n = winrate(r)
    print('{:0.3f}'.format(wr),'{:6d}'.format(n),*tup)
    overall += r
    if large_test(tup):
        large += r
    if small_test(tup):
        small += r
    if micro_test(tup):
        micro += r

wr,n = winrate(overall)
print('{:0.3f}'.format(wr),'{:6d}'.format(n),'Overall')

wr,n = winrate(large)
print('{:0.3f}'.format(wr),'{:6d}'.format(n),'All large universes')

wr,n = winrate(small)
print('{:0.3f}'.format(wr),'{:6d}'.format(n),'All small universes')

wr,n = winrate(micro)
print('{:0.3f}'.format(wr),'{:6d}'.format(n),'All microverses')

if 0:
    # Looks like 100 is a goo rule of thumb for a real game
    import matplotlib.pyplot as plt

    plt.hist(ns,40)
    plt.show()

