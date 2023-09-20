# Debugging power_ranking

import pickle 
import networkx as nx
from counter import Counter

# Load the result

with open('results_mat.pkl','br') as fin:
    A = pickle.load( fin )

# Examine the strongly connected components

G = nx.DiGraph()

for i,j in zip(*A.nonzero()):
    G.add_edge(i,j)

comps = list(nx.strongly_connected_components(G))

C = Counter()

for comp in comps:
    C.add(len(comp))
x = list(C.items())
x.sort()

for size,count in x:
    print('{} components of size {}'.format(count,size))


