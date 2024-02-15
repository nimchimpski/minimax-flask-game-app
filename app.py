from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
import sys
import time
import json
import uuid
import os

import tictactoe as ttt

# app = Flask(__name__, static_folder='../sharedstatic')
app = Flask(__name__)
app.secret_key = "supermofustrongpword"

# Configure ProxyFix with the correct parameters
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_ECHO'] = True

# Set the app to debug mode
environment = os.environ.get('FLASK_ENV', 'production')
app.config['ENV'] = 'environment'
if environment == 'development':
    app.config['DESBUG'] = True
else:
    app.config['DEBUG'] = False
# app.debug = False
# app.config['ENV'] = 'production'

X = "X"
O = "O"
EMPTY = None

#####    THE DATABASE MODEL    #####
# Gamedb is actually a row in the database ? TODO change name
class Gamedb(db.Model):
    dbid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dbsessionid = db.Column(db.String, nullable=False)
    boardstate = db.Column(db.String, nullable=False)
    human = db.Column(db.String, nullable=False)  # Store human as a string

    def saveboard(self, sessionid, board, human=None):
        # print(f'+++SAVEBOARD---')
        self.dbsessionid = sessionid
        self.boardstate = json.dumps(board)  # Store board as a string
        if human is not None:
            self.human = json.dumps(human)
        # Commit the changes to the database
        db.session.commit()
        return board


    def getboard(self, sessionid):
        # print(f'+++GETBOARD---')
        sessionrow = Gamedb.query.filter_by(dbsessionid=sessionid).first()
        if sessionrow:
            print(f'---sessionrow found= {sessionrow}')
            return json.loads(sessionrow.boardstate)
        else:
            print('+++getboard: no sessionrow in db---')
            return None

    def __repr__(self):

        return f"<Gamedb(dbid={self.dbid}, dbsessionid={self.dbsessionid}, boardstate={self.boardstate}, human={self.human})>"

with app.app_context():
    db.create_all()

# sessionrow = Gamedb()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/', methods=['GET'])
def index():
    print('>>>INDEX ROUTE GET')
    # if no sessionid, create one
    sessionid = session.get('sessionid')
    if not sessionid:
        print('---no sessionid in session---')
        session['sessionid'] = str(uuid.uuid4())
        sessionid = session['sessionid']
    print(f'---sessionid={sessionid}')


    return render_template('index.html')

@app.route('/play', methods=['POST', 'GET'])
def play():
    print('>>>PLAY ROUTE GET')

     # define gameover check function
    def gameovercheck(num, board):
        game_over = ttt.terminal(board)
        if game_over:
            # print(f'---game over{num}={game_over}')
            #### detrmine winner
            winner = ttt.winner(board)
            #  IF TIE
            if winner is None:
                winner = 'TIE'
            return winner

    sessionid = session.get('sessionid')
    #### CHECK IF SESSION ROW EXISTS
    sessionrow = Gamedb.query.filter_by(dbsessionid=sessionid).first()

    if sessionrow == None:
        print(f'---no sessionrow= {sessionrow}')

    #########      POST     #########
    if request.method == 'POST':
        print('>>>PLAY ROUTE POST')

        ####    print all json
        # print(f"\n--- request.json= {request.json} ---") 

        #### CHECKC IF NEW GAME + INITIALISE
        if request.json.get('newgame') == True:
            print('--- NEW GAME ---')

            #### DEAL WITH CHOSEN PLAYER
            human = request.json.get('human')
            # print(f"--- human chose to be : {human} ---")

            ####   RESET BOARD
            board = ttt.initial_state()
            print(f'---board initialised--{board}-')


            # if no row in db for this sessionid, create one
            print('---queried sessionrow---')
            print(f'---existing sessionrow= {sessionrow}')
            if not sessionrow:
                print('---MAKING NEW SESSIONROW---')

                sessionrow = Gamedb(dbsessionid=sessionid, boardstate=json.dumps(board), human=json.dumps(human))
                db.session.add(sessionrow)

            # INITIALISE BOARD IN DATABASE
            sessionrow.saveboard(sessionid, board, human)
            print(f'---sessionrow= {sessionrow}')
            print(f'---initialised board saved---{sessionrow}')

        ####     HUMAN MOVE
        humanmove = request.json.get('humanmove')
        if humanmove != None:
            humanmove = request.json.get('humanmove')
            human = request.json.get('human')
            # print(f"--- humanMove received: {humanmove} {type(humanmove)}---")
            humanmovetuple = tuple(int(char) for char in humanmove)
            # print(f"--- movetuple= {humanmovetuple} ---")
            #### GET BOARD FROM DB
            board = sessionrow.getboard(sessionid)
            # print(f"+++ board retrieved hm= {board} ---")
            ####  UPDATE BOARD WITH HUMAN MOVE  ####
            board = ttt.result(board, humanmovetuple)
            # print(f"--- board after human mv= {board} ---")
            ####   CHECK FOR GAME OVER
            winner = gameovercheck(human, board)
            if winner is not None:
                # print(f"--- GAMEOVER frm humanmove ={winner} ---")
                return jsonify({'winner': winner})
            #### STORE BOARD IN DB
            sessionrow.saveboard(sessionid, board)
            ####    DETERMINE WHOSE TURN
            player = ttt.player(board)
            # print(f">>>player after human mv= {player} ---")

        ####  AI  MOVE
        print(f"--- AI MOVE")
        # time.sleep(0.5)
        #### GET BOARD FROM DB
        board = sessionrow.getboard(sessionid)
        player = ttt.player(board)
        print(f">>>> player b4 ai mv= {player} ---")
        print(f"board retrieved b4 ai mv= {board} ---")
        #### ai makes move
        aimove = ttt.minimax(board)
        # print(f"\n---aimove={aimove}")
        #### update board
        board = ttt.result(board, aimove)
        print(f"--- board after ai mv= {board} ---")
        ####   CHECK FOR GAME OVER
        winner = gameovercheck('AI', board)
        if winner is not None:
            print(f"--- Ai is winner={winner} ---")
            aimovestr = ''.join(str(e) for e in aimove)
            # print(f"---aimovestr={aimove}{type(aimove)}")
            return jsonify({'winner': winner, 'aimove': aimovestr})
        #### STORE BOARD IN DB
        sessionrow.saveboard(sessionid, board)
        #### prepare response
        aimovestr = ''.join(str(e) for e in aimove)
        # print(f"---aimovestr={aimove}{type(aimove)}")
        # print(f"---aimove={aimove}{type(aimove)}")

        return jsonify({'aimove': aimovestr})
    
    
    

if __name__ == '__main__':
    app.run(debug=True)
