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
comment:'John\'s choice to start with a blue ship is a little unusual. Most players seem to prefer starting with a green ship.',
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
comment:'Choosing a yellow star may give John the option to advance his b1 to an aggressive early colony or the ability to discover a large system just when Andy sets up to build a large ship. I would have preferred to discover a green star to better keep up with building blues.',
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
comment:'It\'s very hard to be sure, but John <i>might</i> have been a little better off diversifying, trading either ship in JOHS for some other color.',
img:'images/state18.png',
conts:[ {
text:'build b3 Pepperland',
quality:'orig',
comment:'',
img:'images/state19.png',
conts:[ {
text:'sacrifice y2 Jome;move b1 JOHS Pepperland;move b1 HSOJ Pepperland;catastrophe Pepperland b',
quality:'orig',
comment:'John has spent his only yellow ship, leaving Andy with the mobility and diversity advantages. John\'s material advantage has dwindled significantly.',
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
comment:'If he had discovered a green system instead of yellow, Andy would be better prepared to compete for blue ships.',
img:'images/state27.png',
conts:[ {
text:'trade b2 r2 Jome',
quality:'orig',
comment:'John chooses a good time to get red. If Andy delays getting a red of his own, John\'s y2 can hound Andy\'s ships. To get his first red now, Andy will lose access to some power in in a system.<br><br>I would have preferred to get this r2 in JOHS instead since Jome already has access to red. Later in the game, an r2 in Jome that matches a homestar will be a liability.',
img:'images/state28.png',
conts:[ {
text:'trade b1 r1 Pepperland',
quality:'orig',
comment:'Andy cripples his ability to compete for blue ships. He might have been slightly better off trading the b2 in Narnia for red.',
img:'images/state29.png',
conts:[ {
text:'build b1 Jome',
quality:'orig',
comment:'John presses his blue advantage.',
img:'images/state30.png',
conts:[ {
text:'build g1 Wunderland',
quality:'orig',
comment:'Andy is now prepared to build b3 in Narnia (by sacrifice) if John gives him the opportunity.',
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
comment:'I don\'t like this move. Andy may have thought it was important to keep the last of the yellow away from John, but he passed up a chance to build b3, and Andy\'s Pepperland colony is now a lovely target for John to invade.',
img:'images/state43.png',
conts:[ {
text:'move b3 J Pepperland',
quality:'orig',
comment:'',
img:'images/state44.png',
conts:[ {
text:'sacrifice y2 Pepperland;discover y1 Pepperland y2 MiddleEarth;move r1 Pepperland MiddleEarth',
quality:'orig',
comment:'This new colony is no better defended, but with only two ships, John does not seem to think it is worth his time.',
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
comment:'This was a mistake. Andy doesn\'t have enough red to defend against John\'s direct assault.',
img:'images/state49.png',
conts:[ {
text:'sacrifice y2 J;move r3 Pepperland Wunderland;move b3 Pepperland Wunderland',
quality:'orig',
comment:'',
img:'images/state50.png',
conts:[ {
text:'sacrifice y3 Narnia;move r1 MiddleEarth Jome;move r1 MiddleEarth Jome;pass;catastrophe Jome r',
quality:'orig',
comment:'Andy cannot defend and goes for a moral victory by taking out one of John\'s stars.',
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
comment:'Andy needs to use this turn to deter John\'s double-large invasion.',
img:'images/state53.png',
conts:[ {
text:'build r3 Pepperland',
quality:'',
comment:'John has enough material for a Doomsday machine, but it\'s all out of position. John\'s yellow supply is limited, so it will take time arrange the ships properly.',
img:'images/state54.png',
conts:[ {
text:'sacrifice g2 Neverland;build g2 Neverland;build r3 Narnia',
quality:'',
comment:'Andy has a (1r/3g) Doomsday machine <u>right now</u>. If John doesn\'t take the r2 ship out of his home, sacrificing the y3 lets Andy invade with two small reds for the catastrophe and move a green from Neverland to Narnia. Assuming no interruptions, Andy can then move g1, g3, g1 to Jome on separate turns for the winning catastrophe.<br><br>If John does move the r2, Andy only needs to move a green ship from Neverland closer to Jome to complete the machine. Andy will win if both players blindly go ahead with their Doomsday plans. Because of Andy\'s more complete Doomsday machine and superior mobility, I favor his position. But John has some time for counterplay, so the outcome isn\'t clear.',
img:'images/state55.png',
conts:[  ]
},{
text:'sacrifice g3 Wunderland;build g3 Wunderland;build r3 Narnia;build b2 Narnia',
quality:'',
comment:'This turn also completes Andy\'s Doomsday machine, but it gives John a choice to build a b3 in either in Pepperland (in Doomsday position) or in J (where it is poised to invade Neverland). Andy has little use for a b2 at this point, so giving John another b3 appears counterproductive.',
img:'images/state56.png',
conts:[  ]
} ]
} ]
} ]
},{
text:'sacrifice y2 J;move b3 Pepperland Wunderland;move b3 Pepperland Wunderland',
quality:'worse',
comment:'John could have tried launching his invasion one turn earlier, but Andy could defend by catastrophe.',
img:'images/state57.png',
conts:[ {
text:'sacrifice y3 Narnia;move b2 Narnia Neverland;move b2 Neverland Wunderland;move g2 Neverland MiddleEarth;catastrophe Wunderland b',
quality:'',
comment:'',
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
};

