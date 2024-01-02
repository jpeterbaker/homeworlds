'''
NOTE: with no help given to the optimizer, this is way too slow.
The objective function has to be called 10,000 times just to optimize on A[:10,:10].
Providing the Jacobian would probably be a big help.

Read a bunch of BGA records, track pairwise results, and compute ML Elo scores
If the Elo scores of two players are A and B,
the probability of A beating B is
    1/(1 + 10^((B-A)/400) )

Say p is the probability of A beating B and they play n games.
The probability that A wins exactly k games is
    (n choose k) * p^k * (1-p)^(n-k)

Now consider the probability of the win-counts across all observed pairs
(where the number of times the players meet is exogenous).
That's just the product of all those probabilities.
The MLE Elo scores maximize that product, or equivalently, the log of the product.
When you take the log, all of the log(n choose k) terms are independent of the parameters
(the parameters being the pair-probabilities p as determined by Elo scores).
So, you can just sum up
    k*log(p) + (n-k)*log(1-p)
across all pairs that meet, and maximize.

When you substitute in the Elo score expressions for win probability, you get
    -k*log( 1+10^(A-B)/400 ) - (n-k)*log( 1+10^(B-A)/400)
and if you want to use a minimization routine, you just throw out the negative signs.

You could use a generic optimizer, but you can use your information about
the functional form of your objective (as a sum of a bunch of terms)
to use a more efficient nonlinear least-squares solver.
Since a least squares solver will square each term before adding them up,
you'll want to take the square root first.
Overall, my suggestion is to sic a NLS solver on the vector-valued function
where each entry of the output is
    sqrt( k*log( 1+10^(A-B)/400 ) + (n-k)*log( 1+10^(B-A)/400) )
Conveniently, this formula does not care if k is an integer,
so k can be the total score with draws counting as 1/2
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

from read_results import results_array,largest_component
from scipy.sparse import triu,dok_array,csc_array
from scipy.optimize import least_squares as nls
import numpy as np

(A,lookup_id,lookup_index,lookup_name) = results_array(runit)
A = A[:5,:5]

K = csc_array(triu(A)) # triu makes a coo_matrix
N = csc_array(triu(A+A.T))
# These represent the pairs of players who have played together
ii,jj = K.nonzero()

nplayer = A.shape[0]
npair = ii.size

# Number of games for  each pair of players
ns  = N[ii,jj]
# Number of wins for player whose perspective is used the represent the pair
ks  = K[ii,jj]
# Number of wins for opposite player
nks = ns-ks

# If elo is an array of player Elo scores,
# then (pairD@elo)[k] = elo[ii[k]] - elo[jj[k]]
pairD = dok_array( (npair,nplayer) )
pairD[range(npair),ii] =  1
pairD[range(npair),jj] = -1
pairD = pairD.tocsr()

# This is the MLE objective function
c = [0]
def f(elo):
    c[0] += 1
    if c[0] % 1000 == 0:
        print('f call',c[0])
    dscore = pairD@elo
    return np.sqrt(ks*np.log( 1+10**( dscore/400) )
             + nks*np.log( 1+10**(-dscore/400) ))
elo0 = 1500*np.ones(nplayer)
result = nls(f,elo0,xtol=1)

print(result.message)

name_list = [ lookup_name[lookup_id[i]] for i in lookup_id ]

# Print players sorted by their eigenvector entry
print_players(result.x,name_list)

