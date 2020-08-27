
from hwstate import HWState
from text2turn import applyTextTurn as att

state = HWState()

##################
# Creation tests #
##################
try:
    att('pass',state)
    print('Test failed: allowed first-turn pass')
except Exception as e:
    assert(str(e) == 'You may not pass your first turn.')

try:
    att('build b1 Bob',state)
    print('Test failed: built ship in non-existent system')
except Exception as e:
    # I don't really care which of the many problems with this raises an Exception
    pass
    
att('homeworld r2 b1 g3 Alice',state)

try:
    att('pass',state)
    print('Test failed: allowed first-turn pass')
except Exception as e:
    assert(str(e) == 'You may not pass your first turn.')

try:
    att('homeworld y2 b3 g3 Alice',state)
    print('Test failed: allowed same-named homeworlds')
except Exception as e:
    assert(str(e) == 'The Alice system already exists.')
try:
    att('pass',state)
    print('Test failed: allowed first-turn pass')
except Exception as e:
    assert(str(e) == 'You may not pass your first turn.')
    
att('homeworld y2 b3 g3 Bob',state)

###############
# Build tests #
###############

try:
    att('build g2 Alice',state)
    print('Test failed: built a ship too big')
except:
    pass

att('build g1 Alice',state)
att('build g1 Bob',state)

####################
# Testing whatever #
####################

att('trade g1 y1 Alice',state)
att('trade g1 y1 Bob',state)

att('build g1 Alice',state)
att('build g1 Bob',state)

att('trade g1 r1 Alice',state)
att('trade g1 r1 Bob',state)

att('discover y1 Alice g3 Ferenginar',state)
att('discover y1 Bob g1 Billy',state)

att('move y1 Ferenginar Billy',state)
att('sacrifice r1 Bob attack y1 Billy',state)

