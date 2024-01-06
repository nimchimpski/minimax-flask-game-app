from flask import Flask, render_template, request, jsonify, redirect, url_for, flask_session
from flask_session import Session
from tempfile import mkdtemp
import pygame
import sys
import time
import json

import tictactoe as ttt

app = Flask(__name__)

# Set the app to debug mode
app.debug = True
app.config['ENV'] = 'development'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

human = None
board = ttt.initial_state()
ai_turn = False
X = "X"
O = "O"
EMPTY = None



@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')

@app.route('/chosenplayer', methods=['POST'])
def chosenplayer():
    print('>>>CHOSENPLAYER ROUTE')
    human = request.json.get('chosenplayer')
    print(f"--- human chose to be : {human} ---")
    if human == 'X':
        human = X
    elif human == 'O':
        human = O  
        print('---AI NEEDS TO MOVE NOW')

    print(f"--- human= {human} ---")
    return jsonify(human)
    # return redirect(url_for('play'))
    # returnfromplayer = 'returnfromplayer'

    # return jsonify(returnfromplayer)  

@app.route('/play', methods=['POST', 'GET'])
def play():
    print('>>>PLAY ROUTE')
    global board, ai_turn, human, X, 0, EMPTY
    ####   CHECK FOR GAME OVER
    if ttt.terminal(board):
        print(f'---game over={game_over}')
        #### detrmine winner
        winner = ttt.winner(board)
        return jsonify(winner)
    ####   DETERMINE WHOSE TURN
    # look at board
    # is human x or o

     ####    IF AI - AI MAKES MOVE
    if human != player and not game_over:
        print(f"---human!=player")
        if ai_turn:
            time.sleep(0.5)
            aimove = ttt.minimax(board)
            print(f"---aimove={aimove}")
            #### update board
            board = ttt.result(board, aimove)
            ai_turn = False
            #### prepare response
            aimovestr = ''.join(str(e) for e in aimove)
            print(f"---aimovestr={aimovestr}{type(aimovestr)}")

            
            return jsonify(aimovestr)

    ####     ELSE EXTRACT MOVE FROM REQUEST
    move = request.json.get('move')
    print(f"--- Move received: {move} {type(move)}---")
    movetuple = tuple(int(char) for char in move)
    print(f"--- movetuple= {movetuple} ---")
    
    ####  UPDATE BOARD   ####
    board = ttt.result(board, movetuple)
    print(f"--- board= {board} ---")
    ####    CHECK FOR GAME OVER
    game_over = ttt.terminal(board)
    if game_over:
        print(f'---game over={game_over}')
        #### detrmine winner
        winner = ttt.winner(board)
        return jsonify(winner)
    print(f'---game over={game_over}')
    ####    DETERMINE WHOSE TURN
    player = ttt.player(board)
    print(f"--- player after 1st mv= {player} ---")

        else:
            ai_turn =  True



@app.route('/humansturn', methods=['POST'])
def humansturn():
    print(">>>HUMANSTURN ROUTE")

    return


if __name__ == '__main__':
    app.run(debug=True)
