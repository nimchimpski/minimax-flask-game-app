var human
var ai

function init() {
    // Initialize your board and attach event listeners
}

var message1 = document.getElementById
    ("message1");
var message2 = document.getElementById
    ("message2");
(function() {
    message1.innerHTML = "Choose your player";
    message2.innerHTML = "X plays first";
})();
function hideelement(element) {
    var x = document.getElementById(element);
    x.style.display = "none";
}
function showelement(element) {
    var x = document.getElementById(element);
    x.style.display = "block";
}
function chosenplayer(chosenplayer) {
    console.log('---chosenplayer=',chosenplayer.id);
    // update human choice
    if (chosenplayer.id === 'X'){
        human = 'X'
        ai = 'O'
        console.log('---h=x human=',human, 'ai=', ai)
        message2.innerHTML = "Your turn ";
    }
        
    else {
        human = 'O'
        ai = 'X' 
        console.log('---h=0 human=',human, 'ai=', ai)
        message2.innerHTML = "Computer's turn...thinking";
    }
    console.log('---human=',human, 'ai=', ai);
    // Choose your player
  
    message1.innerHTML = "You are playing as " + chosenplayer.id; 
    

    //hide the choose player
    hideelement("chooseplayer");
    
    // display the baord
    showelement("board");

    // Send the chosen player to the Flask server
    fetch('/chosenplayer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chosenplayer: chosenplayer.id }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('choosepl Success:', data)
        if (data.result === 'success') {
            window.location.href = '/play';
        
        }
        
        
     
    })
 
   console.log('---human=',human);
}



function play(humanmove) {
    console.log('---humanmove=',humanmove.id);
    // mark the board with x or o
    console.log('---human=',human);
    humanmove.innerHTML = human;
    // Send the move to the Flask server
    fetch('/play', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ move: humanmove.id }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response for playfn was not ok');
        }
        return response.json();
    })
    
    .then(data => {
        console.log('play Success:', data);
        // Update your game board here based on the response
        aimove = data
        console.log("---aimove=", aimove)
        document.getElementById(aimove).innerHTML = ai
        // update the message

    })
    .catch((error) => {
        console.error('playfn Error :', error);
    });
}


