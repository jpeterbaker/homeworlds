'''
Tools for converting English BGA log into SDG format
See also jpeterbaker.github.io/homeworlds/site/tools/record_convert.js

This isn't done. I'm worried, probably too much, about people with weird usernames.
If there is a player named "restarts their turn" or if
"Bill" plays a game with "Homeworld Bill",
it would be nice if the code could interpret the logs correctly.
'''

import re

bga_pat_restart = re.compile(r'^(.*?) restarts their turn\.$')
bga_pat_end     = re.compile(r'^(.*?) ends their turn\.$')

bga_pat_create = re.compile(r'^(.*?) establishes a homeworld with a (..) ship at (..) and (..) binary stars\.$')

bga_pat_build   = re.compile(r'^(.*?) builds a (..) ship in (.*)\.$')
bga_pat_trade   = re.compile(r'^(.*?) trades a (..) ship for a (..) ship in (.*)\.$')
bga_pat_move    = re.compile(r'^(.*?) moves a (..) ship from (.*?) to (.*)\.$')
bga_pat_capture = re.compile(r'^(.*?) captures a (..) ship in (.*)\.$')

bga_pat_discover    = re.compile(r'^(.*?) discovers a (..) system named (.*)\.$')
bga_pat_fade        = re.compile(r'^(.*?) is forgotten\.$')
bga_pat_sacrifice   = re.compile(r'^(.*?) sacrifices a (..) ship in (.*)\.$')
bga_pat_catastrophe = re.compile(r'^(.*?) triggers a (\w+) catastrophe in (.*)\.$')

bga_victory = re.compile(r'^The end of the game: (.*) wins!$')
bga_tie     = re.compile(r'^End of game \(tie\)$')

