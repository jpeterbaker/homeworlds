'''
Tools for cooperation with Homeworlds Live site
(pass is denoted by "pass")

Examples of HWL's log and map strings are in
exampleLog.hwl and
exampleMap.hwl
'''

from sys import path
path.append('../hwlogic')

from hwstate import HWState
from text2turn import applyTextTurn,re

class HWLState:
    # A state the way HWL thinks of it with named pieces
    def __init__(self):
        # Underlying state in my own format
        self.state = HWState()
        # Look up ships by piece type and letter
        # keys are strings like 'y2A'
        # values are the name of the system that the piece occupies (as a ship)
        # stars are not tracked
        self.systemMap = {}
        # Name to give to the next-created system
        self.systemIndex = 1
    def apply_HWL_text_turn(self,s):
        # Apply the turn s
        '''
        TODO
        * Replace x with a (for attack)
        * Expand letter-based piece identifiers for ship and system name
        Most of the rest should work pretty well since I ignore commas

        returns the SDG-like version of the command
        '''
        r = ';'.join([self.convert_action(a) for a in s.split(';')])
        applyTextTurn(r,self.state)
        return r

    def convert_action(self,s):
        '''
        s is an atomic action string in HWL format (not a whole turn)
        Specifically, s should describe one of the following
        * a homeworld creation
        * a power action
        * a sacrifice
        * a catastrophe
        * a pass
        returns a string for the same action in my SDG-based format
        '''
        words = s.split(',')
        if words[0] == 'b':
            # BUILD
            # IN
            # b,ship piece with letter,system name
            # OUT
            # b,ship piece,system name
            shipPiece = words[1][:2]
            systemName = words[2]
            s1 = ','.join(['b',shipPiece,systemName])

            self.systemMap[words[1]] = systemName
        elif words[0] == 'd':
            # DISCOVER
            # IN
            # d,ship piece with letter,star piece with letter
            # OUT
            # d,ship piece,origin system name,destination system piece,destination system name
            shipPiece = words[1][:2]
            starPiece = words[2][:2]
            oldName = self.systemMap[words[1]]
            newName = str(self.systemIndex)
            s1 = ','.join(['d',shipPiece,oldName,starPiece,newName])

            self.systemIndex += 1
            self.systemMap[words[1]] = newName
        elif words[0] == 'm':
            # MOVE
            # IN
            # m,ship piece with letter,destination system name
            # OUT
            # m,ship piece,origin system name,destination system name
            shipPiece = words[1][:2]
            oldName = self.systemMap[words[1]]
            newName = words[2]
            s1 = ','.join(['m',shipPiece,oldName,newName])

            self.systemMap[words[1]] = newName
        elif words[0] == 't':
            # TRADE
            # IN
            # t,before ship piece with letter,after ship piece with letter
            # OUT
            # t,before ship piece,after ship piece,system name
            oldPiece = words[1][:2]
            newPiece = words[2][:2]
            systemName = self.systemMap[words[1]]
            s1 = ','.join(['t',oldPiece,newPiece,systemName])

            self.systemMap[words[2]] = systemName
            # Popping the old piece from the map shouldn't be necessary
        elif words[0] == 'x':
            # CAPTURE
            # IN
            # x,target ship piece with letter
            # OUT
            # a,target ship piece,system name
            shipPiece = words[1][:2]
            systemName = self.systemMap[words[1]]
            s1 = ','.join(['a',shipPiece,systemName])
        elif words[0] == 's':
            # SACRIFICE
            # IN
            # s,ship piece with letter
            # OUT
            # s,ship piece,system name
            shipPiece = words[1][:2]
            systemName = self.systemMap[words[1]]
            s1 = ','.join(['s',shipPiece,systemName])
        elif words[0] == 'c':
            # CATASTROPHE
            # IN
            # c,color,system name
            # OUT
            # c,system name,color
            s1 = ','.join(['c',words[2],words[1]])
        elif words[0] == 'h':
            # HOMEWORLD
            # IN
            # h,star piece with letter,star piece with letter,ship piece with letter
            # OUT
            # h,star piece,star piece,ship piece,system name
            starPiece0 = words[1][:2]
            starPiece1 = words[2][:2]
            shipPiece = words[3][:2]
            systemName = str(self.systemIndex)
            s1 = ','.join(['h',starPiece0,starPiece1,shipPiece,systemName])

            self.systemMap[words[3]] = systemName
            self.systemIndex += 1
        elif words[0] == 'pass' or words[0] == 'p':
            s1 = 'p'
        else:
            raise Exception('Unknown command: "{}"'.format(words[0]))
        return s1

def json_2_HWLState(d):
    # d is a dictionary made from the HWL state formatted as a JSON
    raise NotImplementedError('Sorry, not done yet')
    s = HWLState()
    pieceMap = d['map']
    hwNumbers = d['homeworldData']
    for piece,props in pieceMap:
        pass
        

