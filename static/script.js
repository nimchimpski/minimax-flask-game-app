function init() {
    // Initialize your board and attach event listeners
}

function play(cell) {
    console.log('---cell=',cell);
    // mark the board with x or o
    cell.innerHTML = 'x';
    // Send the move to the Flask server
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ move: cell.id }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    
    .then(data => {
        console.log('Success:', data);
        // Update your game board here based on the response
    })
    .catch((error) => {
        console.error('Errorrrr:', error);
    });
}


