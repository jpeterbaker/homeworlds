
# Throw-away file for relatively complex debugging

import cPickle

with open('reallyDeepStrs.pkl','r') as fin:
    deep = cPickle.load(fin)
with open('lessDeepStrs.pkl','r') as fin:
    shallow = cPickle.load(fin)

print 'As dicts'
print len(deep)
print len(shallow)

for t in deep:
    if not deep[t] == shallow[t]:
        print '\n'*4
        print 'Discrepency!'
        print '\n'*2
        print t
        print deep[t]
        print shallow[t]

print 'As sets'
deep=set(deep)
shallow=set(shallow)
print len(deep)
print len(shallow)

print 'Sizes of differences'
print len(deep-shallow)
print len(shallow-deep)

