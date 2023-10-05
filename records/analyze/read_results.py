'Get HW results from BGA files or from pickled results'

import pickle
import os
from scipy.sparse import coo_array
import numpy as np
from bga_basic_read import read_players,opening_results

root_dir = '/mnt/c/Users/Bakers/Documents/hw_replays/'

def results_array(runit):
    if runit:
        return file_array()
    return pickle_array()

def file_array():
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

    # Put a zero in the corner to make matrix square
    results.append(0)
    ii.append(n-1)
    jj.append(n-1)

    A = coo_array( (results, (ii,jj) ) , dtype=float )
    A = A.tocsc()

    with open('results_mat.pkl','bw') as fout:
        pickle.dump( (A,lookup_id,lookup_index,lookup_name) ,fout )

    return (A,lookup_id,lookup_index,lookup_name)

def pickle_array():
    ################################################
    # Create win matrix by loading previous result #
    ################################################
    print('Using previously saved results')
    with open('results_mat.pkl','br') as fin:
        (A,lookup_id,lookup_index,lookup_name) = pickle.load( fin )
    return (A,lookup_id,lookup_index,lookup_name)

