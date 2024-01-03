from flask import Flask, render_template, request, jsonify
import pygame
import sys
import time
import json

import tictactoe as ttt

app = Flask(__name__)

# Set the app to debug mode
app.debug = True
app.config['ENV'] = 'development'



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def receive_move():
    # extract the move from the request
    move = request.json.get('move')
    print(f"--- Move received: {move} ---")

    # Process the move (you'll replace this with your game logic)
    # response = process_move(move)
    response = 'robots_move'

    # Return the response
    return jsonify(response)

def process_move(move):
    render_template('index.html')
    # Here, insert your Python logic for processing the move
    # For now, let's just return the move
    # return {"status": "success", "move": move}
    return render_template('index.html')
    board = request.json['board']
    move = ttt.minimax(board)
    return jsonify({'move': move})

if __name__ == '__main__':
    app.run(debug=True)
