

var ticTacToeGame;


class TicTacToeGame {
    constructor() {
        this.human = null;
        this.ai = null;
        this.newgameatrib = false;
        this.message1 = document.getElementById("message1");
        this.message2 = document.getElementById("message2");
        this.init();
    }

    init() {
        document.querySelectorAll('.cell').forEach(item => {
            item.addEventListener('click', event => {
                this.play(event.target.id);
            })
        });
        document.getElementById('message2').addEventListener('click', event => {
            this.chooseplayer();
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
        var x = document.getElementById(element);
        x.disabled = false;
    }

    disableElement(element) {
        var x = document.getElementById(element);
        x.disabled = true;
    }

    chooseplayer() {
        console.log('...+++chooseplayer()');
        this.showElement("chooseplayer");
        this.hideElement("board");
        this.message1.innerHTML = "Choose your player";
        this.message2.innerHTML = "X plays first";
        this.message2.style.border = "None";
        this.disableElement('message2');
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

        this.hideElement("chooseplayer");
        this.showElement("board");

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
                this.enableElement('message2');
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



