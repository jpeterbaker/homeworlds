var first_turn_skip = 0;
var root = {
text:'',
quality:'',
comment:'',
img:'images/state0.png',
conts:[ {
text:'homeworld g1 b3 y3 Babamots',
quality:'',
comment:'Welcome to Homeworlds! In this game, you are the ruler of a space-faring civilization. You are at war with an alien race who will not stop until they destroy you, and you have no choice but to destroy them first. You will build a fleet a of spaceships and spread it across the stars in defense of your homeworld.<br>This game takes place in the shapeless emptiness of space. There is no board. The *ships and stars* will be represented by *pyramids* taken from the bank.<br>It\'s your first turn, so it\'s time to establish your homeworld! Start by selecting a *small red* piece for your first homestar.<br>Good! When a pyramid becomes a star, it stands up and looks like a square from above. Homeworlds are established at binary star systems, so you get to pick a second star now. Select a *large blue* star this time.<br>Now you\'ll need a ship to occupy your homeworld. Select a *large green* ship as your first defender.<br>Congratulations! You\'ve established a homeworld for your civilization. You must keep a defending ship at your homeworld at all times or you will *lose the game*! You win if you destroy or capture all enemy ships at *their* homeworld.<br>Notice that when a pyramid is used as a ship, it lies on its side and looks like a triangle from above.<br>After every turn, you need to finalize your choice by passing the turn token to your opponent. Until you pass the token, you have the option to restart your turn in case you made a mistake. For now, just *select the token* to end your turn.<br>Now it\'s your opponent\'s turn to make a homeworld.',
img:'images/state1.png',
conts:[ {
text:'homeworld b1 g2 y3 Alien',
quality:'',
comment:'They didn\'t have to, but your opponent picked the same colors for their stars and ship as you did. Their ship is also yellow, but color doesn\'t indicate ownership. You can tell who controls a ship because ships always "face" the same direction as their owner: *your ships point up* and your opponent\'s ships point down.<br>Each color provides a different technology. In each system where you have a ship, you can use the technologies provided by the stars and by your ships. In your homeworld, you have access to yellow, blue, and green technologies. We\'ll talk about each of the technologies later.',
img:'images/state2.png',
conts:[ {
text:'build y1 Babamots',
quality:'',
comment:'Now that it\'s your turn again, it\'s time to start building your fleet. Fortunately, *green* technology is the power to *build*, and you have a green star.<br>To order your ship to build another ship, start by selecting your ship to activate it.<br>Now select your green star to give green building technology to your ship.<br>You\'ve just built your first ship! Notice that the new ship is yellow like your original ship, not green like the star. When you build a ship, it will always be the *same color as the ship* used to build it. Also, you can\'t choose just any size for the new ship. The built ship is always the *smallest available* piece of the correct color from the bank.&lt;br&gt;Now pass the token to finish your turn.',
img:'images/state3.png',
conts:[ {
text:'build y1 Alien',
quality:'',
comment:'Your opponent also built a ship. There\'s not really another choice until you get a second ship.<br>Now let\'s see the blue technology in action. *Blue* gives the power to *trade* a ship for another color. To change the color of your large ship, first you need to activate it.',
img:'images/state4.png',
conts:[ {
text:'trade y3 g3 Babamots',
quality:'',
comment:'Now select your blue star to give blue power to your ship.<br>Now you get to select a new color for your ship, though it will stay the same size. Change your ship to green by selecting a large green ship from the bank.<br>Good! You\'ve got ships of two colors now. Time to end your turn.',
img:'images/state5.png',
conts:[ {
text:'build y1 Alien',
quality:'',
comment:'Your opponent built another small yellow ship, and the small yellow pieces are all in play. If you build a yellow ship now, you will get a medium. Select your yellow ship to activate it...<br>...and now select green: either your green ship or your green star (the effect is the same).',
img:'images/state6.png',
conts:[ {
text:'build y2 Babamots',
quality:'',
comment:'The sizes of ships will matter later, and your medium-size ship will have advantages over small ships. For now, just finish your turn.',
img:'images/state7.png',
conts:[ {
text:'trade y1 g1 Alien',
quality:'',
comment:'You\'re probably wondering how to move ships to other places, so it\'s time to learn. *Yellow* is the power of *movement*. To move your medium yellow ship select it...<br>...and then give it movement power by selecting a yellow piece. Either of your yellow ships will do.<br>Now you need a place for your ship to go, so you need to know a little about system connections. You *cannot* move a piece from one system to another if those systems have any *star sizes in common*. Your homeworld and your opponent\'s homeworld each have a small star, so your homeworlds are not connected.<br>There are no existing systems for your ship to visit, so you\'ll just have to find a new one. You can make a new system by selecting a new star from the bank. It cannot be a small or large star since those sizes are in your homeworld, so it must be a medium. Select a medium green piece to continue.',
img:'images/state8.png',
conts:[ {
text:'discover y2 Babamots g2 A',
quality:'',
comment:'You\'ve discovered a new star! The green piece you chose came out of the bank and marks the new system that you moved your ship into. End your turn to continue.',
img:'images/state9.png',
conts:[ {
text:'discover g1 Alien r3 B',
quality:'',
comment:'Your opponent also discovered a new star. It had to be a large star since their homeworld has small and medium stars.<br>This looks like a good time to go on the offensive. Move your ship to the "Bleb" system by selecting your medium yellow ship...<br>...and select it again to give it movement power...<br>...and select the Bleb system to move your ship there. Notice that Alti and Bleb systems are connected because their stars are *not* the same size.',
img:'images/state10.png',
conts:[ {
text:'move y2 A B',
quality:'',
comment:'You\'ve just invaded your opponent\'s colony! Notice that the Alti system disappeared when your ship left. Systems with no ships are immediately forgotten, and their stars are returned to the bank. End your turn to continue.',
img:'images/state11.png',
conts:[ {
text:'discover y1 Alien g3 C',
quality:'',
comment:'Now it\'s time to learn about red. The power of *red* is to *capture* an enemy ship. The attacking ship must be *at least as large* as the ship it captures. (Your opponent couldn\'t capture your yellow ship because your ship is larger.)',
img:'images/state12.png',
conts:[ {
text:'attack g1 B',
quality:'',
comment:'Give your medium yellow ship capturing power by selecting it...<br>...and selecting the red star...<br>...and finally select the enemy ship to capture it.<br>You\'ve won the first encounter with the enemy! End your turn to find out what they do next.',
img:'images/state13.png',
conts:[ {
text:'build y1 C',
quality:'',
comment:'You\'ve seen all of the technologies now, so there are only a few more things to know.<br>Next, let\'s talk about sacrifice, which is a different turn option. You can spend your turn sacrificing one ship--returning it to the bank--and then activating one or more ships (anywhere) with the power of the sacrificed ship. The number of activations depends on the size of the ship: 1 for a small, 2 for a medium, 3 for a large.',
img:'images/state14.png',
conts:[ {
text:'sacrifice g3 Babamots;build y2 B;build y2 B;build y3 Babamots',
quality:'',
comment:'Try it now with your large green ship. First, select the ship...<br>...and use the sacrifice button.<br>You now have 3 build actions that can be used anywhere. Use them to build a yellow ship in Bleb...<br>...and another yellow in Bleb...<br>...and a yellow at your home.<br>Notice that, once the medium yellow pieces ran out, you got to build a large ship. End your turn to finalize your choice.',
img:'images/state15.png',
conts:[ {
text:'build y3 Alien',
quality:'',
comment:'There\'s one last principle to learn: overpopulation and catastrophe. It\'s not safe for too much of a single technology to be in the same system. If 4 piecesof the same color--counting *ships and stars*--are ever in a system together, those pieces are "overpopulated."<br>On their turn, *either* player may turn an overpopulation into a "catastrophe" as a *free action* at any point during their turn. In a catastrophe, all ships of the overpopulated color explode and are returned to the bank. If the star of an ordinary system is destroyed in a catastrophe, any remaining ships in that system are also returned to the bank.<br>One of the most common ways to win is to destroy your opponent\'s homestars in catastrophes. Another way to win is to use a catastrophe to destroy all of the defending ships in their home. You have that opportunity now.<br>Your opponent has nothing but two yellow ships in their home. If you move two more yellow ships there, they will be overpopulated and you can trigger the catastrophe.',
img:'images/state16.png',
conts:[ {
text:'sacrifice y2 B;move y2 B Alien;move y2 B Alien;catastrophe Alien y',
quality:'',
comment:'In order to move two ships to their home before they can react, you\'ll need to sacrifice. Select a medium yellow to sacrifice...<br>...and hit the "sacrifice" button.<br>Now select a ship...<br>...and move it to your opponent\'s hom.<br>Then select another ship...<br>...and move it to your opponent\'s home.<br>Now, a new button has appeared to let you trigger a catastrophe. Press the "catastrophe" button.<br>Now select any of the overpopulated pieces to destroy them.<br>End your turn to complete your victory.<br>Congratulations! You\'ve destroyed the defenses of the evil aliens and peace is assured!',
img:'images/state17.png',
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
};

