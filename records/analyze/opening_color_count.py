# Like opening_count.py but with color included

import os
from numpy import zeros
from bga_basic_read import opening_results

root_dir = '/mnt/c/Users/Bakers/Documents/hw_replays/'

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
            n,s00,s01,ship0,s10,s11,ship1,w = opening_results(full_name)
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
