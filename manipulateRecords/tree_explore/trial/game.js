var first_turn_skip = 1;
var root = {
text:'',
quality:'',
comment:'',
img:'images/state0.png',
conts:[ {
text:'discover r1 Beta y3 Deneb',
quality:'orig',
comment:'',
img:'images/state1.png',
conts:[ {
text:'sacrifice y2 Betelgeuse;move r1 Betelgeuse Altair;move r2 Castor Altair;catastrophe Altair r',
quality:'orig',
comment:'Alpha won quickly after this.',
img:'images/state2.png',
conts:[  ]
} ]
},{
text:'move r2 Altair Alpha',
quality:'better',
comment:'This is better than the play in the actual game because it forces a draw (or better). However, this game was played on SDG which does not allow draws, so if the best lines are followed by both players from here, the game technically would have continued until one of them resigned. Since Beta was the challenger, it would have made sense for Beta to resign. (For games where SDG allows draws, SDG considers the challenger to be the loser in drawn games.)',
img:'images/state3.png',
conts:[ {
text:'attack r2 Alpha',
quality:'',
comment:'',
img:'images/state4.png',
conts:[ {
text:'sacrifice y2 Altair;move r3 Beta Altair;move r3 Altair Alpha',
quality:'',
comment:'',
img:'images/state5.png',
conts:[ {
text:'sacrifice y3 Betelgeuse;move r1 Betelgeuse Altair;move r3 Castor Altair;move r2 Castor Altair;catastrophe Altair r',
quality:'',
comment:'This is the correct move, but many players in Alpha\'s position would fail to see it. Destroying four of one\'s own ships to get just one of one\'s opponent\'s ships is almost never a good move, but in this case, any other move allows Beta to win.',
img:'images/state6.png',
conts:[ {
text:'attack r2 Alpha',
quality:'',
comment:'There is now nothing better to do than trade the r2 ship back and forth.',
img:'images/state7.png',
conts:[ {
text:'attack r2 Alpha',
quality:'',
comment:'',
img:'images/state8.png',
conts:[ {
text:'attack r2 Alpha',
quality:'',
comment:'',
img:'images/state9.png',
conts:[  ]
} ]
} ]
} ]
} ]
},{
text:'move r2 Altair Alpha',
quality:'',
comment:'',
img:'images/state10.png',
conts:[ {
text:'sacrifice r2 Alpha;attack r2 Alpha;pass',
quality:'',
comment:'',
img:'images/state11.png',
conts:[  ]
} ]
} ]
},{
text:'sacrifice y1 Alpha;move y3 Betelgeuse Alpha',
quality:'worse',
comment:'Reinforcing with y3 is not sufficient since the red catastrophe threat persists.',
img:'images/state12.png',
conts:[ {
text:'sacrifice y2 Altair;move r2 Altair Alpha;discover r1 Beta y3 Deneb',
quality:'',
comment:'Beta will win on their next turn.',
img:'images/state13.png',
conts:[  ]
} ]
} ]
},{
text:'sacrifice y2 Altair;move r3 Beta Altair;move r3 Altair Alpha',
quality:'worse',
comment:'Initially promising, the r3 invasion should lose once Alpha destroys Beta\'s sacrificial reds on one turn and then simultaneously defends and counterattacks in the next.',
img:'images/state14.png',
conts:[ {
text:'sacrifice y2 Betelgeuse;move r1 Betelgeuse Altair;move r2 Castor Altair;catastrophe Altair r',
quality:'',
comment:'',
img:'images/state15.png',
conts:[ {
text:'attack y2 Alpha',
quality:'',
comment:'',
img:'images/state16.png',
conts:[ {
text:'sacrifice y3 Betelgeuse;move r3 Betelgeuse Alpha;move r3 Castor Altair;move r3 Altair Beta',
quality:'',
comment:'',
img:'images/state17.png',
conts:[ {
text:'attack r3 Alpha',
quality:'',
comment:'',
img:'images/state18.png',
conts:[ {
text:'attack r1 Beta',
quality:'',
comment:'',
img:'images/state19.png',
conts:[  ]
} ]
} ]
} ]
} ]
} ]
},{
text:'move y2 Altair Alpha',
quality:'worse',
comment:'With the right yellow sacrifice, Alpha will avoid the double threat of yellow overpopulation and direct assault.',
img:'images/state20.png',
conts:[ {
text:'sacrifice y2 Alpha;move y3 Betelgeuse Alpha;move y1 Alpha Castor',
quality:'',
comment:'',
img:'images/state21.png',
conts:[  ]
} ]
} ]
};

