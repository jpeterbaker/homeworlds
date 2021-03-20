# Convert an SDG-style log to an table in my usual format

from sys import stdin

print('''<!--
Generated with log2html.py

Use semicolons to separate actions if you want them on separate lines
Type log or enter CTRL-D to cancel and use redirect, as in

python log2html.py  <  logFileName.txt

Also consider redirecting output to a file as in

python log2html.py  <  logFileName.txt  >  table.html
-->
'''

lines = []

for line in stdin:
    line = line.strip()
    if len(line) == 0:
        continue
    lines.append(line)

n = len(lines)

tablestart = '''
<div class="moveTable">
    <div class="headerRow">
        <div class="headerCell">
            Player 1
        </div>
        <div class="headerCell">
            Player 2
        </div>
    </div>'''.strip()
rowstart = '    <div class="moveRow">'
plystart = '        <div class="ply">'
plyend   = '        </div>'
rowend   = '    </div>'
tableend = '</div>'

a_turn_number_template = ' '*12 + '{}.<br>'
b_turn_number_template = ' '*12 + '{}...<br>'
line_template = ' '*12 + '{}'

print(tablestart)
for i in range(n):
    if i%2 == 0:
        print(rowstart)
        print(plystart)
        print(a_turn_number_template.format(i//2+1))
    else:
        print(plystart)
        print(b_turn_number_template.format(i//2+1))
    actions = lines[i].split(';')
    # All but one action get a line break
    for action in actions[:-1]:
        print(line_template.format(action)+'<br>')
    print(line_template.format(actions[-1]))
    print(plyend)
    if i%2 == 1:
        print(rowend)
print(tableend)


