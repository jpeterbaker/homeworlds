var first_turn_skip = 0;
var root = {
text:'',
quality:'',
comment:'',
img:'images/state0.png',
conts:[ {
text:'homeworld b1 r2 g3 Wunderland',
quality:'orig',
comment:'Andy chooses the opening he was known for at the time.',
img:'images/state1.png',
conts:[ {
text:'homeworld g3 r1 b3 Jome',
quality:'orig',
comment:'John\'s choice to start with a blue ship isn\'t something most players prefer in my experience.',
img:'images/state2.png',
conts:[ {
text:'build g1 Wunderland',
quality:'orig',
comment:'',
img:'images/state3.png',
conts:[ {
text:'build b1 Jome',
quality:'orig',
comment:'',
img:'images/state4.png',
conts:[ {
text:'trade g1 b1 Wunderland',
quality:'orig',
comment:'',
img:'images/state5.png',
conts:[ {
text:'build b2 Jome',
quality:'orig',
comment:'',
img:'images/state6.png',
conts:[ {
text:'build b2 Wunderland',
quality:'orig',
comment:'',
img:'images/state7.png',
conts:[ {
text:'trade b2 y2 Jome',
quality:'orig',
comment:'',
img:'images/state8.png',
conts:[ {
text:'trade b1 y1 Wunderland',
quality:'orig',
comment:'',
img:'images/state9.png',
conts:[ {
text:'discover b1 Jome y2 HSOJ',
quality:'orig',
comment:'',
img:'images/state10.png',
conts:[ {
text:'discover b2 Wunderland g3 Pepperland',
quality:'orig',
comment:'',
img:'images/state11.png',
conts:[ {
text:'build b1 Jome',
quality:'orig',
comment:'',
img:'images/state12.png',
conts:[ {
text:'build b2 Pepperland',
quality:'orig',
comment:'',
img:'images/state13.png',
conts:[ {
text:'discover b1 Jome g2 JOHS',
quality:'orig',
comment:'',
img:'images/state14.png',
conts:[ {
text:'trade b2 y2 Pepperland',
quality:'orig',
comment:'',
img:'images/state15.png',
conts:[ {
text:'build b2 JOHS',
quality:'orig',
comment:'',
img:'images/state16.png',
conts:[ {
text:'build y1 Wunderland',
quality:'orig',
comment:'',
img:'images/state17.png',
conts:[ {
text:'build b2 Jome',
quality:'orig',
comment:'',
img:'images/state18.png',
conts:[ {
text:'build b3 Pepperland',
quality:'orig',
comment:'',
img:'images/state19.png',
conts:[ {
text:'sacrifice y2 Jome;move b1 JOHS Pepperland;move b1 HSOJ Pepperland;catastrophe Pepperland b',
quality:'orig',
comment:'',
img:'images/state20.png',
conts:[ {
text:'trade y1 b1 Wunderland',
quality:'orig',
comment:'',
img:'images/state21.png',
conts:[ {
text:'build b1 JOHS',
quality:'orig',
comment:'',
img:'images/state22.png',
conts:[ {
text:'move b1 Wunderland Pepperland',
quality:'orig',
comment:'',
img:'images/state23.png',
conts:[ {
text:'trade b2 y2 Jome',
quality:'orig',
comment:'',
img:'images/state24.png',
conts:[ {
text:'build b2 Pepperland',
quality:'orig',
comment:'',
img:'images/state25.png',
conts:[ {
text:'build b2 Jome',
quality:'orig',
comment:'',
img:'images/state26.png',
conts:[ {
text:'discover b2 Pepperland y2 Narnia',
quality:'orig',
comment:'',
img:'images/state27.png',
conts:[ {
text:'trade b2 r2 Jome',
quality:'orig',
comment:'',
img:'images/state28.png',
conts:[ {
text:'trade b1 r1 Pepperland',
quality:'orig',
comment:'',
img:'images/state29.png',
conts:[ {
text:'build b1 Jome',
quality:'orig',
comment:'',
img:'images/state30.png',
conts:[ {
text:'build g1 Wunderland',
quality:'orig',
comment:'',
img:'images/state31.png',
conts:[ {
text:'discover b1 Jome g2 J',
quality:'orig',
comment:'',
img:'images/state32.png',
conts:[ {
text:'build g1 Wunderland',
quality:'orig',
comment:'',
img:'images/state33.png',
conts:[ {
text:'trade b2 g2 JOHS',
quality:'orig',
comment:'',
img:'images/state34.png',
conts:[ {
text:'discover g1 Wunderland y3 Neverland',
quality:'orig',
comment:'',
img:'images/state35.png',
conts:[ {
text:'build b2 JOHS',
quality:'orig',
comment:'',
img:'images/state36.png',
conts:[ {
text:'build g1 Neverland',
quality:'orig',
comment:'',
img:'images/state37.png',
conts:[ {
text:'sacrifice g2 JOHS;build b2 Jome;build b3 J',
quality:'orig',
comment:'',
img:'images/state38.png',
conts:[ {
text:'sacrifice g3 Wunderland;build g2 Neverland;build b3 Narnia;build g3 Wunderland',
quality:'orig',
comment:'',
img:'images/state39.png',
conts:[ {
text:'trade b3 y3 Jome',
quality:'orig',
comment:'',
img:'images/state40.png',
conts:[ {
text:'trade b3 y3 Narnia',
quality:'orig',
comment:'',
img:'images/state41.png',
conts:[ {
text:'move y2 Jome J',
quality:'orig',
comment:'',
img:'images/state42.png',
conts:[ {
text:'sacrifice g3 Wunderland;build g3 Wunderland;build y1 Wunderland;build y1 Pepperland',
quality:'orig',
comment:'',
img:'images/state43.png',
conts:[ {
text:'move b3 J Pepperland',
quality:'orig',
comment:'',
img:'images/state44.png',
conts:[ {
text:'sacrifice y2 Pepperland;discover y1 Pepperland y2 MiddleEarth;move r1 Pepperland MiddleEarth',
quality:'orig',
comment:'',
img:'images/state45.png',
conts:[ {
text:'build b3 Pepperland',
quality:'orig',
comment:'',
img:'images/state46.png',
conts:[ {
text:'sacrifice g3 Wunderland;build g3 Wunderland;build r1 MiddleEarth;build b3 Narnia',
quality:'orig',
comment:'',
img:'images/state47.png',
conts:[ {
text:'trade b3 r3 Pepperland',
quality:'orig',
comment:'',
img:'images/state48.png',
conts:[ {
text:'discover y1 Wunderland b3 Pern',
quality:'orig',
comment:'',
img:'images/state49.png',
conts:[ {
text:'sacrifice y2 J;move r3 Pepperland Wunderland;move b3 Pepperland Wunderland',
quality:'orig',
comment:'',
img:'images/state50.png',
conts:[ {
text:'sacrifice y3 Narnia;move r1 MiddleEarth Jome;move r1 MiddleEarth Jome;pass;catastrophe Jome r',
quality:'orig',
comment:'',
img:'images/state51.png',
conts:[ {
text:'sacrifice r3 Wunderland;attack g3 Wunderland;attack y1 Wunderland;attack g1 Wunderland',
quality:'orig',
comment:'',
img:'images/state52.png',
conts:[  ]
} ]
} ]
} ]
},{
text:'trade b2 r2 Narnia',
quality:'better',
comment:'Andy is in trouble but would live longer with enough red to capture two simultaneously invaders.',
img:'images/state53.png',
conts:[ {
text:'build r3 Pepperland',
quality:'',
comment:'',
img:'images/state54.png',
conts:[ {
text:'sacrifice g2 Neverland;build g2 Neverland;build r3 Narnia',
quality:'',
comment:'Andy now has a Doomsday machine prepared.',
img:'images/state55.png',
conts:[  ]
},{
text:'sacrifice g3 Wunderland;build g3 Wunderland;build r3 Narnia;build b2 Narnia',
quality:'worse',
comment:'This move doesn\'t look quite as good since it lets John get a b3.',
img:'images/state56.png',
conts:[ {
text:'build b3 J',
quality:'',
comment:'',
img:'images/state57.png',
conts:[  ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
},{
text:'trade b1 y1 JOHS',
quality:'better',
comment:'This blocks Andy\'s teams\' build rather than commiting John\'s team to a catastrophe later',
img:'images/state58.png',
conts:[  ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
} ]
};

