# Check that a log has followed the rules
# and print a standardized version of each turn

from sys import stdin,path
from os import path as ospath
path.append(ospath.join(ospath.dirname(__file__),'../../hwlogic/'))

from hwstate import HWState
from text2turn import applyTextTurn as att
from buildState import buildState

lines = [line.strip() for line in stdin]
nlines = len(lines)
if nlines == 0:
    print('[No input]')
    exit()

for first in range(nlines):
    line = lines[first]
    if len(line) == 0:
        continue
    if line[0] == '#':
        continue
    if line[0] == '<':
        print('# Starting with initial state')
        print(line)
        state = buildState(line)
        break
    else:
        print('# Starting with blank state')
        state = HWState()
        first -= 1
        break

for line in lines[first+1:]:
    if len(line) == 0 or line[0] == '#':
        continue
    try:
        turn = att(line,state)
    except Exception as e:
        print('Got an error while processing the line:')
        print(line)
        print()
        print(e)
        break
    print(turn)
    if state.onmove == 0 or state.isEnd():
        print()
print()
print(state.buildStr())


