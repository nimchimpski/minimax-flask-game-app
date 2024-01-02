from flask import Flask, render_template, request
import pygame
import sys
import time

import tictactoe as ttt

app = Flask(__name__)


app = Flask(__name__)

@app.route('/tictactoe/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def make_move():
    board = request.json['board']
    move = ttt.minimax(board)
    return jsonify({'move': move})

if __name__ == '__main__':
    app.run(debug=True)
