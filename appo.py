from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sys
import time
import json

import tictactoe as ttt

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# Set the app to debug mode
app.debug = True
app.config['ENV'] = 'development'

# human = None
# board = ttt.initial_state()
# ai_turn = False





@app.route('/', methods=['GET'])
def index():
    print('>>>INDEX ROUTE')

    return render_template('index.html')


@app.route('/play', methods=['POST', 'GET'])
def play():
    print('>>>PLAY ROUTE')
    EMPTY = None
    X = "X"
    O = "O"
    
    # print all json
    print(f"--- request.json= {request.json} ---")

    ####   CHECK IF ITS A NEW GAME
    if request.json.get('newgamex') == True:
        print('>>>NEW GAME')
        ####    RESET BOARD
        board = ttt.initial_state()
        # Store board
        session['board'] = board
        return jsonify({'board': board})
        ####    RESET HUMAN AND AI (O AND X)
    human = request.json.get('human')
    print(f"--- human  from json= {human} ---")
  
   

    ####     ELSE EXTRACT MOVE FROM REQUEST
    move = request.json.get('move')
    # print(f"--- Move received: {move} {type(move)}---")
    movetuple = tuple(int(char) for char in move)
    print(f"--- movetuple= {movetuple} ---")
    if move != None:
        ####  UPDATE BOARD   ####
        board = session.get('board')
        board = ttt.result(board, movetuple)
        print(f"\n--- board after human= {board} ---")

        ####    CHECK FOR GAME OVER
        game_over = ttt.terminal(board)
        print(f'---1game over={game_over}')
        if game_over:
            print(f'---2game over={game_over}')
            #### detrmine winner
            winner = ttt.winner(board)
            #  IF TIE
            if winner is None:
                winner = 'TIE'
            return jsonify({'gameover': game_over, 'winner': winner})
            print(f'---game over={game_over}')

    # ensure human move was stored
    print(f"\n--- board after human 2 = {board} ---")
     ####  AI MAKES MOVE
    # if  not game_over:  
    print(f"--- AI MOVE CODE ---")
    print(f"---player(board) {ttt.player(board)}")
    time.sleep(0.5)
    aimove = ttt.minimax(board)
    print(f"---aimove={aimove}")
    #### update board
    board = ttt.result(board, aimove)
    print(f"\n--- board after AI= {board} ---")
    #### prepare response
    aimovestr = ''.join(str(e) for e in aimove)
    print(f"---aimovestr={aimovestr}{type(aimovestr)}")
    winner = ttt.winner(board)
    # print(f"---winner={winner}")

    ####   CHECK FOR GAME OVER
    if ttt.terminal(board):
        print(f'---terminal True')
        game_over = True
        #### detrmine winner
        if ttt.winner(board) is not None:
            winner = ttt.winner(board)
            print(f"---winner={winner}")
        ### if no winner
        else:
            winner = 'TIE'
            print(f"---winner={winner}")
    session['board'] = board
    print(f"---b4 response :session['board']={session['board']}")
    return jsonify({'aimove': aimovestr, 'gameover': game_over, 'winner': winner})


if __name__ == '__main__':
    app.run(debug=True)
