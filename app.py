from flask import Flask, render_template, request, jsonify, redirect, url_for
# from flask_session import Session
from tempfile import mkdtemp
from flask_sqlalchemy import SQLAlchemy
import sys
import time
import json

import tictactoe as ttt

app = Flask(__name__)
# config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
# init session
# Session(app)
# db.init_app(app)



# Set the app to debug mode
app.debug = True
app.config['ENV'] = 'development'



# human = None
# board = ttt.initial_state()
# ai_turn = False
X = "X"
O = "O"
EMPTY = None



class Gamedb(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    boardstate = db.Column(db.String, nullable=False)  # Store board as a string
    human = db.Column(db.String, nullable=False)  # Store human as a string

    def saveboard(self, board, human=None):
        self.boardstate = json.dumps(board)
        if human is not None:
            self.human = json.dumps(human)
        return board

    def getboard(self):
        
        return json.loads(self.boardstate)

    def __repr__(self):
        return '<Gamedb %r>' % self.id

with app.app_context():
    db.create_all()

gamedb = Gamedb()

@app.route('/', methods=['GET'])
def index():
    print('>>>INDEX ROUTE')
    
    return render_template('index.html')

@app.route('/play', methods=['POST', 'GET'])
def play():

    #### SUB FUNCTIONS

     # define gameover check function
    def gameovercheck(num, board):
        #### GET BOARD FROM DB
        
        game_over = ttt.terminal(board)
        if game_over:
            print(f'---game over{num}={game_over}')
            #### detrmine winner
            winner = ttt.winner(board)
            #  IF TIE
            if winner is None:
                winner = 'TIE'
            return winner

    if request.method == 'POST':
        print('>>>PLAY ROUTE')
        ####    print all json
        print(f"\n--- request.json= {request.json} ---") 
        #### CHECKC IF NEW GAME + INITIALISE
        if request.json.get('newgame') == True:
            print('--- new game in json ---')
            #### DEAL WITH CHOSEN PLAYER
            # set human variable
            human = request.json.get('human')
            # print(f"--- human chose to be : {human} ---")
            ####   RESET BOARD
            board = ttt.initial_state()
            # print('---board initialised---')
            #### STORE bOARD and HUMAN IN DB
            gamedb.saveboard(board, human)
            print(f'---initialised board saved---{board}, {human}')
        ####     HUMAN MOVE

        humanmove = request.json.get('humanmove')
        if humanmove != None:
            humanmove = request.json.get('humanmove')
            human = request.json.get('human')
            print(f"--- humanMove received: {humanmove} {type(humanmove)}---")
            humanmovetuple = tuple(int(char) for char in humanmove)
            # print(f"--- movetuple= {humanmovetuple} ---")
            #### GET BOARD FROM DB
            board = gamedb.getboard()
            print(f"+++ board retrieved hm= {board} ---")
            ####  UPDATE BOARD WITH HUMAN MOVE  ####
            board = ttt.result(board, humanmovetuple)
            print(f"--- board after human mv= {board} ---")
            ####   CHECK FOR GAME OVER
            winner = gameovercheck(human, board)
            if winner is not None:
                print(f"--- GAMEOVER frm humanmove ={winner} ---")
                return jsonify({'winner': winner})
            #### STORE BOARD IN DB
            gamedb.saveboard(board)
            ####    DETERMINE WHOSE TURN
            player = ttt.player(board)
            print(f">>>player after human mv= {player} ---")
        
        ####  AI  MOVE
        print(f"--- AI MOVE")
        time.sleep(0.5)
        #### GET BOARD FROM DB
        board = gamedb.getboard()
        player = ttt.player(board)
        print(f">>>> player b4 ai mv= {player} ---")
        print(f"+++ board retrieved  ai= {board} ---")
        #### ai makes move
        aimove = ttt.minimax(board)
        print(f"\n---aimove={aimove}")
        #### update board
        board = ttt.result(board, aimove)
        print(f"--- board after ai mv= {board} ---")
        ####   CHECK FOR GAME OVER
        winner = gameovercheck('AI', board)
        if winner is not None:
            print(f"--- Ai is winner={winner} ---")
            aimovestr = ''.join(str(e) for e in aimove)
            print(f"---aimovestr={aimove}{type(aimove)}")
            return jsonify({'winner': winner, 'aimove': aimovestr})
        #### STORE BOARD IN DB
        gamedb.saveboard(board)
        #### prepare response
        aimovestr = ''.join(str(e) for e in aimove)
        print(f"---aimovestr={aimove}{type(aimove)}")
        print(f"---aimove={aimove}{type(aimove)}")
        
        return jsonify({'aimove': aimovestr})

if __name__ == '__main__':
    app.run(debug=True)
