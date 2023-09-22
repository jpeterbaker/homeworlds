'''
Read a bunch of BGA records, track pairwise results,
and compute pagerank score
'''

# Read all the files to build matrix?
# Otherwise, just read last result
runit = 1
# Include BGA player ID in printout?
rank_bga_id = 0
# Number of player ranks to reveal
n_to_show = 100
# Use Discord spoiler tags?
spoiler_tag = 0

import pickle
import os
from scipy.sparse import coo_array,csc_array
from scipy.sparse.linalg import eigs
import numpy as np
from bga_basic_read import read_players,opening_results
import networkx as nx
from counter import Counter

root_dir = '/mnt/c/Users/Bakers/Documents/hw_replays/'

if runit:
    ######################################
    # Create win matrix by reading files #
    ######################################

    # lookup_index[x] is the row/column corresponding to player with id x
    lookup_index = {}
    # lookup_id[i] is the id of the player whose row/column is i
    lookup_id = []

    # List of scores, each is 1 or 0.5
    results = []
    # Lists of coordinates for those scores
    # For each k, results[k] is the score of player ii[k] against player jj[k]
    ii = []
    jj = []

    # lookup_name[x] is a set of names used by player with id x
    lookup_name = {}

    limit = np.inf

    print('Reading result files')
    for root,ds,fs in os.walk(root_dir):
        for fname in fs:
            if not fname.endswith('txt'):
                continue
            full_name = os.path.join(root,fname)
            if not os.path.isfile(full_name):
                # Skip directories
                continue
            try:
                n,_,_,_,_,_,_,w = opening_results(full_name)
            except Exception as e:
                print(e)
                print('Had trouble with',fname)
                exit()
                continue
    #        ns.append(min(n,1000))
            if n < 100:
                continue
            players = read_players(full_name)

            # Record names
            for i in range(2):
                try:
                    # Add name used this game to the set for this id
                    lookup_name[players[i][0]].add(players[i][1])
                except KeyError:
                    # This is the first time this player has been seen
                    idi = players[i][0]
                    namei = players[i][1]
                    lookup_index[idi] = len(lookup_index)
                    lookup_name[idi] = set( (namei,) )
                    lookup_id.append(idi)

            # Rows/columns of the players
            ijs = ( lookup_index[players[0][0]] , lookup_index[players[1][0]] )

            if w == 0 or w == 1:
                results.append(1)
                ii.append(ijs[  w])
                jj.append(ijs[1-w])
            elif w == 2:
                # Draw
                results.extend( (0.5,0.5) )
                ii.extend(ijs)
                jj.extend(ijs[::-1])
            else:
                print('Unknown winner:',w)
            limit -= 1
            if limit <= 0:
                break

    n = len(lookup_index)
    print('Total number of players:',n)

    # Put a zero in the corner to make matrix square
    results.append(0)
    ii.append(n-1)
    jj.append(n-1)

    A = coo_array( (results, (ii,jj) ) , dtype=float )
    A = A.tocsc()

    with open('results_mat.pkl','bw') as fout:
        pickle.dump( (A,lookup_id,lookup_index,lookup_name) ,fout )
else:
    ################################################
    # Create win matrix by loading previous result #
    ################################################
    print('Using previously saved results')
    with open('results_mat.pkl','br') as fin:
        (A,lookup_id,lookup_index,lookup_name) = pickle.load( fin )
    n = len(lookup_index)
    print('Total number of players:',n)

######################################
# Find strongly connected components #
# and identify the largest one       #
######################################
G = nx.DiGraph()

for i,j in zip(*A.nonzero()):
    G.add_edge(i,j)

print('Identifying strongly connected components of player victory graph')
comps = list(nx.strongly_connected_components(G))
C = Counter()

big_comp = comps[0]
for comp in comps:
    C.add(len(comp))
    if len(comp) > len(big_comp):
        big_comp = comp
n_big = len(big_comp)

x = list(C.items())
x.sort()
for size,count in x:
    print('  {} components of size {}'.format(count,size))
print('Focusing analysis on a component of size',n_big)
print()

# Prepare to translate between original indexing and big_comp submatrix
big_comp = list(big_comp)
lookup_sub = dict(zip(big_comp,range(n_big)))

B = A[big_comp][:,big_comp]

print('Computing PageRank')
B /= B.sum(0)
w,v = eigs(B)

i = np.argmax(w)
whi = w[i]
vhi = v.T[i]
if vhi.min() < 0:
    vhi *= -1

if not np.all(vhi>=0):
    raise Exception('Eigenvector is not non-negative. Something is very wrong.')

# Sort players by their eigenvector entry
p = np.argsort(vhi)
for place,k in enumerate(p[:-n_to_show-1:-1]):
    orig_index = big_comp[k]
    kid = lookup_id[orig_index]
    if rank_bga_id:
        print('{}. {}: {}'.format(
            place+1,
            kid,
            '/'.join(lookup_name[kid])
        ))
    else:
        if spoiler_tag:
            print('{}. ||{}||'.format(
                place+1,
                '/'.join(lookup_name[kid])
            ))
        else:
            print('{}. {}'.format(
                place+1,
                '/'.join(lookup_name[kid])
            ))

