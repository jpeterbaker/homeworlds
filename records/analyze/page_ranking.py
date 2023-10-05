'''
Read a bunch of BGA records, track pairwise results,
and compute pagerank score
'''

# Read all the files to build matrix?
# Otherwise, just read last result
runit = 0
# Include BGA player ID in printout?
rank_bga_id = 0
# Number of player ranks to reveal
n_to_show = 100
# Use Discord spoiler tags?
spoiler_tag = 0

from scipy.sparse.linalg import eigs
import numpy as np
import networkx as nx
from counter import Counter

from read_results import results_array

(A,lookup_id,lookup_index,lookup_name) = results_array(runit)

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

