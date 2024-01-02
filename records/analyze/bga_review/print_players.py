
from numpy import argsort

def print_players(scores,names,spoiler=False,show_score=False,pids=None,nshow=None):
    '''
    scores: list of player scores
    names: corresponding list of lists of names by which player has gone
    spoiler: whether to use Discord spoiler tags
    show_score: whether to show the score itself
    pids: corresponding list of player ids (providing it causes PIDs to be printed)
    '''
    n = len(scores)
    p = argsort(scores)

    if nshow is None:
        nshow = n
    if spoiler:
        template = '{}. ||{}||'
    else:
        template = '{}. {}'

    if not pids is None:
        for i in range(-1,-nshow-1,-1):
            j = p[i]
            score = scores[j]
            name  = names[j]
            print('{}. {}: {}'.format(
                -i,
                pids[j],
                '/'.join(name)
            ))
    else:
        for i in range(-1,-nshow-1,-1):
            j = p[i]
            score = scores[j]
            name  = names[j]
            print(template.format(
                -i,
                '/'.join(name)
            ))

if 0:
    for place,k in enumerate(p[::-1]):
        orig_index = big_comp[k]
        kid = lookup_id[orig_index]
        if not pids is None:
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

