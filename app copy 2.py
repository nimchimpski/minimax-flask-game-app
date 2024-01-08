from flask import Flask, render_template, request, jsonify, redirect, url_for
# from flask_session import Session
from tempfile import mkdtemp
from flask_sqlalchemy import SQLAlchemy
import pygame
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

with app.app_context():
    db.create_all()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    boardstate = db.Column(db.String, nullable=False)  # Store board as a string
    human = db.Column(db.String, nullable=False)  # Store human as a string

    def __repr__(self):
        return '<Game %r>' % self.id

### maybe not needed
def reset_database():
    # Delete all records in the Board table
    db.session.query(Game).delete()
    # You can add similar lines for other tables if necessary
    # Commit the changes to the database
    db.session.commit()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST', 'GET'])
def play():
    #### SUB FUNCTIONS

    def getboard():
        row1 = Game.query.get(1)
        if row1:
            return row1.board_state
        else:
            return "row1 not found in db"
    

    def saveboard(board):
        game = Game(boardstate=board)
        db.session.add(game)
        db.session.commit()
        print(f"+++ board saved= {board} ---")
        return board

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
            return jsonify(winner)

    if request.method == 'POST':
        print('>>>PLAY ROUTE')
        ####    print all json
        print(f"--- request.json= {request.json} ---") 
        #### CHECKC IF NEW GAME + INITIALISE
        if request.json.get('newgame') == True:
            ####   RESET BOARD
            board = ttt.initial_state()

            #### STORE bOARD
            saveboard(board)

            #### DEAL WITH CHOSEN PLAYER
            # set human variable
            human = request.json.get('chosenplayer')
            print(f"--- human chose to be : {human} ---")
            if human == 'X':
                X = "X"
                game.human = X
            elif human == 'O':
                O = "O"
                game.human = O
            db.session.commit()

        
        ####     HUMAN MOVE
        if 'move' in request.json:
            move = request.json.get('move')
            print(f"--- human Move received: {move} {type(move)}---")
            movetuple = tuple(int(char) for char in move)
            print(f"--- movetuple= {movetuple} ---")
            #### GET BOARD FROM DB
            board = getboard()
            ####  UPDATE BOARD WITH HUMAN MOVE  ####
            board = ttt.result(board, movetuple)
            print(f"--- board= {board} ---")
            #### STORE BOARD IN DB
            saveboard(board)
            ####   CHECK FOR GAME OVER
            board = getboard()
            gameovercheck(1, board)
            ####    DETERMINE WHOSE TURN
            player = ttt.player(board)
            print(f"--- player after 1st mv= {player} ---")
        ####  AI  MOVE
        print(f"--- AI MOVE")
        time.sleep(0.5)
        #### GET BOARD FROM DB
        board = getboard()
        aimove = ttt.minimax(board)
        print(f"---aimove={aimove}")
        ####   CHECK FOR GAME OVER
        gameovercheck(2, board)
        #### update board
        board = ttt.result(board, aimove)
        #### STORE BOARD IN DB
        saveboard(board)
        #### prepare response
        aimovestr = ''.join(str(e) for e in aimove)
        print(f"---aimovestr={aimove}{type(aimove)}")
        aimove = aimovestr
        print(f"---aimove={aimove}{type(aimove)}")
        
        return jsonify(aimove)

if __name__ == '__main__':
    app.run(debug=True)
