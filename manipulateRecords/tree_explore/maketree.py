'''
As input, provide a text file with log tree and
a directory as where output files can be stored.

Makes a game tree explorer with HTML and JavaScript

All moves will be verified legal
State images will be saved

input tree file should have this structure:

# comment lines have pound as first non-space character

optionally, first non-blank, non-comment line has a string description
of a game state in buildstate.py format

each subsequent line must be a move, blank, comment, or a single parenthesis
(parenthesis lines may have spaces)

move lines have an SDG-style move description (no line breaks between actions)

moves may be followed by more info separated by slashes:
    move-quality tag (orig,better,worse,none)
    comments

an example move line:
sacrifice g1 A;build g1 B / orig / This is the only move that makes sense

Parentheses enclose alternative continuations to the previous move

For example, in the example below, each move string is unique,
and removing the last letter gives the previous move.

a
aa
aaa
(
aab
aaba
aabaa
)
(
aac
)
aaaa

'''

jstemplate = '''{{
text:'{}',
quality:'{}',
comment:'{}',
img:'{}',
conts:[ {} ]
}}'''

class Node:
    def __init__(self,state,parent=None,turntext='',tag='',comment=''):
        self.state = state
        self.parent = parent
        self.turntext = turntext.replace("'","\\'")
        self.tag = tag.replace("'","\\'")
        self.comment = comment.replace("'","\\'")
        self.img = ''
        self.children = []

    def add_child(self,turntext,tag='',comment=''):
        state = self.state.deepCopy()
        # Apply the turn and get standardized turn string
        turn = att(turntext,state)
        child = Node(state,self,str(turn),tag,comment)
        self.children.append(child)
        return child

    def tojs(self):
        # Get JSON-like JavaScript string
        return jstemplate.format(
            self.turntext,
            self.tag,
            self.comment,
            self.img,
            ','.join([c.tojs() for c in self.children])
        )

    def say_history(self):
        if not self.parent is None:
            self.parent.say_history()
        print()
        print(self.turntext)
        print()
        print(self.state.buildStr())

    def call_on_all(self,f):
        # Call the function f on every Node
        f(self)
        for c in self.children:
            c.call_on_all(f)

from sys import argv,path
path.append('../../hwlogic/')
path.append('../')
from os import path as ospath,mkdir

from itertools import chain

from hwstate import HWState
from buildState import buildState
from drawH import drawState
from text2turn import applyTextTurn as att

if len(argv) != 3:
    print('Expected an input file and a directory to write in')
    exit()

###########################################
# Process input file and check for errors #
###########################################

nline = 0
with open(argv[1],'r') as fin:
    for line in fin:
        nline += 1
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue
        if line[0] == '<':
            print('# Starting with initial state')
            print(line)
            state = buildState(line)
            root = Node(state)
            break
        else:
            print('# Starting with blank state')
            state = HWState()
            root = Node(state)
            # I know it's silly, but it's an easy way to put the line back
            fin = chain([line],fin)
            break

    curnode = root
    # Save the place of the last node with an alternative
    nodestack = []

    for line in fin:
        nline += 1
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue
        if line == '(':
            nodestack.append(curnode)
            curnode = curnode.parent
            continue
        elif line == ')':
            curnode = nodestack.pop()
            continue
        else:
            parts = [w.strip() for w in line.split('/')]
            parts = parts[:2] + ['/'.join(parts[2:])]
            try:
                curnode = curnode.add_child(*parts)
            except Exception as e:
                print('\nGot an error while processing line',nline)
                print(line)
                print()
                print(e)
                print('\nMove history')
                curnode.say_history()
                exit()
    if len(nodestack) > 0:
        print('Parentheses did not appear to line up')

##############################
# Prepare output directories #
##############################

fhtml = ospath.join(argv[2],'explore_game.html')
fjs   = ospath.join(argv[2],'game.js')
imgdir = ospath.join(argv[2],'images/')

try:
    mkdir(argv[2])
except FileExistsError:
    print(argv[2],'already exists. Pressing on.')
try:
    mkdir(imgdir)
except FileExistsError:
    print(imgdir,'already exists. Pressing on.')

###################################
# Write images and save the names #
###################################

key = [0]
fimg_template = ospath.join('images/','state{}.png')
fimg_template_root = ospath.join(imgdir,'state{}.png')
def f(node):
    fimg = fimg_template.format(key[0])
    fimg_root = fimg_template_root.format(key[0])
    key[0] += 1
    node.img = fimg
    drawState(node.state,fimg_root)

root.call_on_all(f)

#######################
# Write local JS file #
#######################

with open(fjs,'w') as fout:
    fout.write('var first_turn_skip = {};\n'.format(root.state.onmove))
    fout.write('var root = {};\n\n'.format(root.tojs()))

########################
# Write main html file #
########################

with open('explore_game_master_copy.html','r') as fin:
    with open(fhtml,'w') as fout:
        for line in fin:
            fout.write(line)

