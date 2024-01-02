'''
Elementary analysis of the game logs I've downloaded.
What were the homeworlds like, how many turns took place, and who won.
'''

import os
from numpy import zeros
from bga_basic_read import opening_results

root_dir = '/mnt/c/Users/Bakers/Documents/hw_replays/'

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
            (n,s00,s01,ship0,s10,s11,ship1,w) = opening_results(full_name)
        except Exception as e:
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
large   = zeros(3,dtype=int)
small   = zeros(3,dtype=int)
micro   = zeros(3,dtype=int)

# Number templates
wrtemp = '{:0.3f}'
wtemp  = '{: >8.1f}'
ntemp  = '{:8d}'

for tup,r in results.items():
    w,n,wr = wins_games_rate(r)
    print(wrtemp.format(wr),wtemp.format(w),ntemp.format(n),*tup)
    overall += r
    if large_test(tup):
        large += r
    if small_test(tup):
        small += r
    if micro_test(tup):
        micro += r

w,n,wr = wins_games_rate(overall)
print(wrtemp.format(wr),wtemp.format(w),ntemp.format(n),'Overall')

w,n,wr = wins_games_rate(large)
print(wrtemp.format(wr),wtemp.format(w),ntemp.format(n),'All large universes')

w,n,wr = wins_games_rate(small)
print(wrtemp.format(wr),wtemp.format(w),ntemp.format(n),'All small universes')

w,n,wr = wins_games_rate(micro)
print(wrtemp.format(wr),wtemp.format(w),ntemp.format(n),'All microverses')

if 0:
    # Looks like 100 is a good rule of thumb for a real game
    import matplotlib.pyplot as plt

    plt.hist(ns,40)
    plt.show()

