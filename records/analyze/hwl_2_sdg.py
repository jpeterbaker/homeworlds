#!/usr/bin/python3.9
# Convert HWL style game log to modified SDG format
import hwl
from sys import argv

helpstr = '''
Useage
./hwl_2_sdg.py <input file> <output file>
'''

if len(argv) != 3:
    print(helpstr)
    exit()

hwlState = hwl.HWLState()
with open(argv[1],'r') as fin:
    with open(argv[2],'w') as fout:
        for line in fin:
            line = line.strip()
            if len(line) == 0:
                continue
            after = hwlState.apply_HWL_text_turn(line)
#            print(line)
#            print('   ',after)
            fout.write(after)
            fout.write('\n')
        fout.write('\n')
        



