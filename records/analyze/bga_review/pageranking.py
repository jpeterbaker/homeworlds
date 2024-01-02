'''
Read a bunch of BGA records, track pairwise results,
and compute pagerank score
'''

# Read all the files to build matrix?
# Otherwise, just read last result
runit = 1
# Include BGA player ID in printout?
rank_bga_id = 0
# Number of player ranks to reveal (None for all)
n_to_show = None
# Use Discord spoiler tags?
spoiler_tag = 0

from scipy.sparse.linalg import eigs
import numpy as np

from read_results import results_array,largest_component
from print_players import print_players

(A,lookup_id,lookup_index,lookup_name) = results_array(runit)

B,big_comp,lookup_sub = largest_component(A)
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

name_list = [ lookup_name[lookup_id[i]] for i in big_comp ]

# Print players sorted by their eigenvector entry
print_players(vhi,name_list,nshow=n_to_show)

