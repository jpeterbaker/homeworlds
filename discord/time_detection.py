'''
Determining if a string (like a Discord message) contains a time reference
Example dynamic timestamp:
<t:1704009600:F>

Formats anticipated, with spaces allowed in places you'd think:
16:00
4:00pm
4pm

NO PLANS TO USE THIS
since Discord doesn't let you detect time zone
'''

import re

hpat = r'\b([01]?\d|2[0-3])'
mpat = r': ?([0-5]\d)'
apat = r'([ap]m)'

fpat = f'{hpat} ?(?:{mpat} ?{apat}|{mpat}|{apat})'


pat = re.compile(fpat,re.I)

def get_time(s):
    # Find the time, if any, in s
    mat = pat.search(s)
    if mat is None:
        print(f'search on "{s}" got nuthin')
        return None

    gs = mat.groups()
    print(gs)
    h = int(gs[0])

    if not gs[1] is None:
        # 4:00pm format
        m = int(gs[1])
        if gs[2].lower().startswith('p'):
            h += 12
    elif not gs[3] is None:
        # 16:00 format
        m = int(gs[3])
    elif not gs[4] is None:
        # 4pm format
        if gs[4].lower().startswith('p'):
            h += 12
        m = 0

    return h,m

if __name__=='__main__':
    print(get_time('3:00'))
