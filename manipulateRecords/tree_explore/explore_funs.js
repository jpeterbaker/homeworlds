/*
Stuff that should exist before this script is loaded:
    JS variables
        root: a nested array with the tree structure exemplified in trial/game.js
        first_turn_skip: 0 or 1
            If this is 1, even-indexed turns are displayed in right column
    HTML objects
        a table with id 'display_table'
        a list with id 'sidebar_list'
        a cell with id 'table_header'
*/

dtable = document.getElementById('display_table');
header_cell = document.getElementById('table_header');
sidebar_list = document.getElementById('sidebar_list');
state_display = document.getElementById('state_display');
comment_display = document.getElementById('comment');

// Most recently clicked turn number in the table
last_ply = -1;

// Get the next turn object following default choice
function get_next(turn){
    if(turn.conts.length == 0)
        return null
    if(turn.hasOwnProperty('child_choice'))
        return turn.conts[turn.child_choice]
    return turn.conts[0]
}
    
function get_turn(n){
    // Get the turn object with index n
    // n < 0 will return the root
    turn = root
    for(i=-1;i<n;i++)
        turn = get_next(turn)
    return turn
}

function get_siblings(n){
    // Following the game choices described by descent,
    // get the array of options available on the nth turn
    if(n==-1)
        return [root]
    return get_turn(n-1).conts
}

// Set or clear highlight for ply n
function highlight(n,light){
    if(n == -1)
        cell = header_cell;
    else{
        ri = Math.floor((n+first_turn_skip)/2)+1
        row = dtable.rows[ri]
        if((n+first_turn_skip)%2 == 0)
            cell = row.cells[0]
        else
            cell = row.cells[1]
    }
    // The anchor node should be the only child
    anode = cell.children[0]
    if(light)
        anode.style.fontWeight = 'bold'
    else
        anode.style.fontWeight = 'normal'
}

/*
cell is the table cell just clicked
it should have a "ply" attribute to make updating the table easier
*/
function table_click(cell){
    // Put the siblings of the cell in the sidebar so a different move can be chosen
    // Show the image of this position 

    // Change highlight from previously selected to current
    highlight(last_ply,0);
    highlight(cell.ply,1);

    last_ply = cell.ply;

    // Clear the current alternatives list
    children = sidebar_list.childNodes
    for(i=children.length-1;i>=0;i--)
        sidebar_list.removeChild(children[i])
    // Display state image, if any
    show_state()

    // Find the siblings of selected turn
    siblings = get_siblings(cell.ply)
    if(siblings.length == 1)
        // No need to put single-item list in sidebar
        return
    // Add list items to the sidebar
    for(i=0;i<siblings.length;i++){
        sib = siblings[i]
        linode = document.createElement('li');
        anode = document.createElement('a');
        textnode = document.createTextNode(sib.text);
        anode.appendChild(textnode);
        linode.appendChild(anode);
        sidebar_list.appendChild(linode)

        anode.order = i;
        //anode.href='#ply'+last_ply
        anode.href='javascript:void(0)'+last_ply
        anode.onclick = function(){sidebar_click(this)}
    }
}

function show_state(){
    turn = get_turn(last_ply);
    if(turn.hasOwnProperty('img'))
        state_display.src = turn.img
    else
        state_display.src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png'
    if(turn.hasOwnProperty('comment'))
        comment_display.innerHTML = turn.comment
    else
        comment_display.innerHTML = ''
}

function trim_table(n){
    // Remove table cells corresponding to ply number n and later

    // Number of rows with at least one good cell
    ngood_rows = Math.floor((n+1+first_turn_skip)/2)
    while(dtable.rows.length > ngood_rows+1)
        dtable.deleteRow(-1)
    if((n+first_turn_skip)%2 == 1)
        // Remove one cell from last row
        dtable.rows[dtable.rows.length-1].deleteCell(-1)
}

// Add default continuations starting with given turn as the given ply number
function add_all(ply,turn){
    if((ply+first_turn_skip)%2 == 1)
        row = dtable.rows[dtable.rows.length - 1]
    while(turn != null){
        if((ply+first_turn_skip)%2 == 0)
            row = dtable.insertRow();
        cell = row.insertCell(-1);
        setup_cell(cell,ply,turn);
        turn = get_next(turn)
        ply += 1
    }
}

/*
anchor is the clicked sidebar anchor
it should have an 'order' attribute indicating its order among siblings
*/
function sidebar_click(anchor){
    // Clear the table rows, starting with the row containing ply (number ply//2)
    // Get the first move from tree
    // For each pair of entries of descent
    // Add a row to the table
    // Add two cells to the row containing the formatted move text
    // add attributes to the cell so it knows what move it corresponds to
    
    // Remember this sibling choice in case an ancestor changes
    // That way, this same line will appear next time our ancestor is chosen
    prev_turn = get_turn(last_ply-1)
    prev_turn.child_choice = anchor.order

    trim_table(last_ply)

    turn = get_next(prev_turn)
    add_all(last_ply,turn)
    // Remaking the cell removes the highlight, so put it back
    highlight(last_ply,1)

    // Display state image, if any
    show_state()
}

/*
anode is a node that needs line-broken text nodes added representing turn
*/
function append_line_broken_turn(anode,text){
    lines = text.split(';');
    textnode = document.createTextNode(lines[0]);
    anode.appendChild(textnode);
    for(i=1;i<lines.length;i++){
        br = document.createElement('br');
        anode.appendChild(br)
        textnode = document.createTextNode(lines[i]);
        anode.appendChild(textnode);
    }
}

function setup_cell(cell,ply_number,turn){
    // Write contents of cell, set ply attribute
    // sibs is list of sibling turns (including this one)
    cell.ply = ply_number;
    row_number = Math.floor(ply_number/2)+1;

    // Remove the old anchor (should be the only child)
    children = cell.childNodes
    if(children.length > 0)
        cell.removeChild(children[0]);

    // Set background color based on move strength
    if(!turn.hasOwnProperty('quality'))
        cell.style.backgroundColor = '#fce8b2';
    else if(turn.quality == 'orig')
        cell.style.backgroundColor = '#a4c2f4';
    else if(turn.quality == 'worse')
        cell.style.backgroundColor = '#f4c7c3';
    else if(turn.quality == 'better')
        cell.style.backgroundColor = '#b7e1cd';
    else if(turn.quality == 'none'){
        // Put nothing in 'none' cell
        cell.style.backgroundColor = '#888888';
        return
    }

    if((ply_number+first_turn_skip) % 2 ==0)
        header = row_number +  '.'
    else
        header = row_number +  '...'
    // Add stars if there are alternatives
    if(get_siblings(ply_number).length > 1)
        header = header + ' **'
    header = header + ';'
    // Set up new anchor child for cell
    anode = document.createElement('a');
    anode.name = 'ply'+ply_number
    //anode.href='#ply'+ply_number
    //anode.href='javascript:void(0)'
    append_line_broken_turn(anode,header + turn.text);
    cell.appendChild(anode)
    //anode.onclick=function(){table_click(cell)}
    cell.onclick=function(){table_click(cell)}
}

//////////////////////
// Initialize table //
//////////////////////
if(first_turn_skip!=0 && first_turn_skip!=1){
    alert('JavaScript error. variable first_turn_skip should be 0 or 1')
}

// Set up the header row cell
header_cell.ply = -1;
anode = document.createElement('a');
anode.href='javascript:void(0)'
textnode = document.createTextNode('Starting position');
anode.appendChild(textnode);
header_cell.appendChild(anode)
header_cell.onclick=function(){table_click(header_cell)}
//anode.onclick=function(){table_click(header_cell)}
show_state()
highlight(-1,1)

// Set up the blank cell representing unseen first player turn, if any
if(first_turn_skip){
    row = dtable.insertRow();
    cell = row.insertCell(-1);
    cell.style.backgroundColor = '#888888';
}
turn = get_next(root);
if(turn != null)
    add_all(0,turn);

