# Play through a game that demonstrated a bug

# Here's the game itself
'''
homeworld b1 y2 g3 wil

homeworld r2 b3 g3 Babamots

build g3 wil

build g3 Babamots

trade g1 b1 wil

trade g1 b1 Babamots

build b1 wil

build b1 Babamots

trade b2 g2 wil

trade b2 y2 Babamots

build b1 wil

build b1 Babamots

trade b2 r2 wil

discover b2 Babamots g1 Risa

build b1 wil

sacrifice g3 Babamots
build b2 Risa
build b2 Risa
build b1 Babamots

discover b2 wil y3 y3

trade b2 r2 Risa

discover b1 wil y3 why3

trade b2 y2 Risa

build g3 wil

build r2 Risa

trade g2 b2 wil

build y2 Risa

build r2 wil

move y2 Risa why3

discover b1 why3 y2 y2
'''
#movestrs = s.split('\n\n')

# I think I'll try to just start at the position

from buildState import buildState
from text2turn import applyTextTurn as att

s = '''
<0>;
wil(0,y2b1)r1g1r2b2g3-;
Babamots(1,b3r2)-b3y2b1
y3(y3)b2-;
why3(y3)b1-y2;
Risa(g1)-b3r2y1r1
'''
state = buildState(s)
try:
    att('discover b1 why3 y2 y2',state)
    print('FAILED stashout on discovery test')
except Exception as e:
    print('had an error as expected:',e)

print(str(state))


