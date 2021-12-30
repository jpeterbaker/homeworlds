
RED    = 'r'
YELLOW = 'y'
GREEN  = 'g'
BLUE   = 'b'

colors = [RED,YELLOW,GREEN,BLUE]

function Piece(size,color){
    this.size  = size
    this.color = color
}

function Ship(piece,player){
    this.piece  = piece
    this.player = player
}

// Number of systems that weren't given custom names
nNameless = 0;

function System(markers,home,name){
    this.markers = markers
    // Player for whom this system is home
    this.home = home
    this.ships = []
    if(name == null){
        nNameless += 1
        name = nNameless
    }
    this.name = name
    this.concentration = {RED:0,YELLOW:0,GREEN:0,BLUE:0}
    for(m of markers)
        this.concentration[m.color] += 1
}

System.prototype.getTech = function(player){
    // Get a set of technology colors available to player
    tech = new Set()
    for(m of this.markers)
        tech.add(m.color)
    for(s of this.ships)
        if(s.player == player)
            tech.add(s.piece.color)
    return tech
}

System.prototype.connectsTo = function(other){
    for(m1 of this.markers)
        for(m2 of other.markers)
            if(m1.size == m2.size)
                return false
    return true
}

System.prototype.isEmpty = function(){
    return this.ships.length == 0
}

System.prototype.isVoid = function(){
    // returns true if all this system's markers have been destroyed
    // or all the ships have left
    return this.isEmpty() || (this.markers.length == 0)
}

System.prototype.hasPresence = function(player,c){
    // returns true if given player has at least one ship in this system
    //                 and that ship is the specified color, or a system marker is that color
    // if c=null, a ship of any color counts
    if(c != null)
        // If a specific color is desired, remove that requirement if a system marker has it
        for(m of this.markers)
            if(m.color == c){
                c = None
                break
            }
    for(s of this.ships)
        if(s.player == player)
            if(c == null || s.piece.color == c)
                return true
    return false
}

System.prototype.getLargestShip = function(player){
    hisize = 0
    hiship = null
    for(ship of this.ships)
        if(ship.player == player && ship.piece.size > hisize){
            if(ship.piece.size == 3)
                return ship
            hisize = ship.piece.size
            hiship = ship
        }
    return hiship
}

System.prototype.removeMarker = function(marker){
    // Index of marker in this.markers
    i = this.markers.findIndex( x => Object.is(x,marker))
    this.markers.splice(i,1)
    this.concentration[marker.color] -= 1
}

System.prototype.restoreMarker = function(marker){
    this.markers.push(marker)
    this.concentration[marker.color] += 1
}

System.prototype.addShip = function(ship){
    this.ships.push(ship)
    this.concentration[ship.piece.color] += 1
}

System.prototype.removeShip = function(ship){
    i = this.ships.findIndex( x => Object.is(x,ship))
    this.ships.splice(i,1)
    this.concentration[ship.piece.color] -= 1
}

System.prototype.getCatastrophes = function(){
    cats = []
    for(c of colors)
        if(this.concentration[c] >= 4)
            cats.push(new Catastrophe(this,c))
    return cats
}

System.prototype.getFade = function(){
    // Get the Fade action caused by this system being forgotten
    // If the marker or ships were destroyed or moved away by other events,
    // the pieces should have already been returned to the stash
    // We just need a list of additional things that disappear as a result
    if(!this.isVoid())
        return null
    return new Fade(this)
}

