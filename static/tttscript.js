

var ticTacToeGame;


class TicTacToeGame {
    constructor() {
        this.human = null;
        this.ai = null;
        this.newgameatrib = false;
        this.message1 = document.getElementById("message1");
        this.message2 = document.getElementById("message2");
        this.message2enabled = false;
        this.boardenabled = true;
        this.init();
        this.cells = document.querySelectorAll('.cell');
    }

    init() {
        document.querySelectorAll('.cell').forEach(item => {
            item.addEventListener('click', event => {
                if (this.boardenabled)
                this.play(event.target.id);
            })
        // make message2 clickable
        document.getElementById("message2").addEventListener('click', event => {
            if (this.message2enabled)
            this.chooseplayer();
        })
        });
       
    }

    hideElement(element) {
        var x = document.getElementById(element);
        x.style.display = "none";
    }

    showElement(element) {
        var x = document.getElementById(element);
        x.style.display = "block";
    }

    enableElement(element) {
        // console.log('...+++enableElement()');
        var x = document.getElementById(element);
        console.log('...+++enableElement(), x=', x);
        x.enabled = false;
    }

    disableElement(element) {
        var x = document.getElementById(element);
        console.log('...+++disableElement(), x=', x);
        x.disabled = true;
    }

    // Define a function to remove event listeners
    removeEventListeners() {
        console.log('...+++removeEventListeners()');    
        this.cells.forEach(cell => {
            // remove event listener
            cell.removeEventListener('click', event => {
                this.play(event.target.id);
            })
        });
    }

    chooseplayer() {
        console.log('...+++chooseplayer()');
        this.showElement("chooseplayer");
        this.hideElement("board");
        this.message1.innerHTML = "Choose your player";
        this.message2.innerHTML = "X plays first";
        this.message2.style.border = "None";
        this.message2enabled = false;
        console.log('...message2enabled=', this.message2enabled )
    }

    startGame(chosenplayer) {
        console.log('...+++startGame()');
        // define new game
        //clear board
        document.querySelectorAll('.cell').forEach(item => {
            item.innerHTML = "";
        });
        this.newgameatrib = true;
        this.human = chosenplayer;
        this.ai = (chosenplayer === 'X') ? 'O' : 'X';
        if (chosenplayer === 'X'){
            this.message2.innerHTML = "Your turn " };
        this.message1.innerHTML = "You are playing as " + this.human;
        this.message2enabled = false;
        console.log('...message2enabled=', this.message2enabled )

        this.hideElement("chooseplayer");
        this.showElement("board");
        this.boardenabled = true;

        if (this.human === 'O') {
            this.play( );
        }
    }

    play(humanmove) {
        console.log('...+++play(), newgameatrib=' , this.newgameatrib,  'human=', this.human, 'ai=', this.ai, 'humanmove=', humanmove);
        // check if this call if from board
        
        if (humanmove) {
            // mark the board
            document.getElementById(humanmove).innerHTML = this.human;
            
        }
        this.message2.innerHTML = "Computer thinking...";
        var newgame
        if (this.newgameatrib) {
            console.log('...newgameatrib was true')
            newgame = true
            console.log('...newgame2= ',newgame)
            this.newgameatrib = false
            console.log('...newgameatrib set to =false? =',this.newgameatrib)
        }
        fetch('/play', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'newgame': newgame, 'human': this.human, 'humanmove': humanmove }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response for playfn was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('playfn data:', data, typeof data);
            // define not new game
            this.newgameatrib = false;
            // check if aimove in data
            if ('aimove' in data) {
                console.log('...aimove in data', data.aimove)
                var aimove = data.aimove;
                // mark board with ai move
                document.getElementById(aimove).innerHTML = this.ai;
            }
             // check for winner
            if ('winner' in data) {
                // is it a tie?
                if (data.winner === 'TIE')
                    var result = 'FOOLS. You both lost.'
                else {
                    var result = (data.winner === this.human ? "You win!" : "You lose!");}

                this.message1.innerHTML = 'GAME OVER   '+ result;
                this.message2.style.border = "1px solid white"
                this.message2.innerHTML = "Play again?";
                this.message2enabled = true;
                console.log('...message2enabled=', this.message2enabled )
                // disable baord
                this.boardenabled = false;
                console.log('...disable board, boardenabled=', this.boardenabled )
                // this.removeEventListeners();
            
            } else {
                this.message2.innerHTML = "Your turn - come on";
            }
            
           
        })
        .catch((error) => {
            console.error('playfn Error :', error);
        });
    }
}

window.onload = () => {
    ticTacToeGame = new TicTacToeGame();
   
};



