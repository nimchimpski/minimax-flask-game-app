"""
Tic Tac Toe Player
"""
import math
import copy
import random

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    # print('+++INITIAL_STATE FN+++')
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def initial_state_end():
    """
    Returns starting state of the board.
    """
    # print('+++INITIAL_STATE_END FN+++')
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
    # return [[O, X, X], [X, EMPTY, EMPTY], [X, O, O]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # print('+++PLAYER FN+++')
    if terminal(board) == True:
        return None
    emptycount = sum(row.count(EMPTY) for row in board)
    if emptycount % 2 == 0:
        # print('>>>#EMPTY',emptycount)
        # print('player = ', O)
        return O
    else:
        # print('player = ', X)
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # print('+++ACTIONS FN')
    if terminal(board) == True:
        # print('>>>terminalboard?>', terminal(board))
        return None
    actions = set()
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            if board[i][j] not in [O, X]:
                # print(f'>>>[i][j] loop> ', (i,j))
                actions.add((i, j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # print('+++RESULT FN+++')
    # print('+++action> ', action)
    if terminal(board) == True:
        # if player(board) == X:
            # print('>>>terminalboard')
        return None
    # print(f'\n>>>results player  {player(board)}, action  {action}')
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("ai trying to overwrite a move")
    else:
        newboard = copy.deepcopy(board)
        # if player(board) == X:
            # print(f'---player(board) {player(board)}')
        newboard[action[0]][action[1]] = player(board)
        # if player(board) == X:
            # print('---newboard> ', newboard)
    
    return newboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # for X
    if any(all(cell == X for cell in row) for row in board):
        winner = X
    elif any(all(row[j] == X for row in board) for j in range(3)):
        winner = X
    elif all(board[i][i] == X for i in range(len(board))):
        winner = X
    elif all(board[i][len(board) - 1 - i] == X for i in range(len(board))):
        winner = X
    # for O
    elif any(all(cell == O for cell in row) for row in board):
        winner = O
    elif any(all(row[j] == O for row in board) for j in range(3)):
        winner = O
    elif all(board[i][i] == O for i in range(len(board))):
        winner = O
    elif all(board[i][len(board) - 1 - i] == O for i in range(len(board))):
        winner = O
    else:
        winner = None
    return winner

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    elif sum(row.count(EMPTY) for row in board) == 0:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # print('+++MINMAX FN+++')
    if terminal(board):
    	return None
    actionsdict = {}
    for action in actions(board):
        if player(board) == X:
            ####  IF BOARD IS EMPTY, PICK A CORNER
            if sum(row.count(X) for row in board) == 0:
    	        print('>>>X picks a corner')
    	        return random.choice([(0, 0), (0, 2), (2, 0), (2, 2)])
          
            ####   STORE MIN VALS IN DICT
            actionsdict[action] = minvalue(result(board, action))
        else:
        	####   STORE MAX VALS IN DICT
            actionsdict[action] = maxvalue(result(board, action) )
    
    if player(board) == X:
    	####   PICK MAX OF THESE MINS 
    	maxval = max(actionsdict.values())
    	for key, val in actionsdict.items():
    	    if val == maxval:
    	        return key
    else:
    	#### 	 PICK MIN OF THESE MAXS
    	minval = min(actionsdict.values())
    	for key, val in actionsdict.items():
    	    # print('>>>minval>', minval)
    	    if val == minval:
    	        # print(f">>> O chooses > ", {key}, {val})
    	        return key

def maxvalue(board):
    v = -math.inf
    if terminal(board) == True:
        return utility(board)
    for action in actions(board):
        v = max(v, minvalue(result(board, action)))
   
    return v


def minvalue(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, maxvalue(result(board, action)))

    return v

# def maxvalue(board, alpha, beta):
#     vmax = -math.inf
#     if terminal(board) == True:
#         return utility(board)
#     for action in actions(board):
#         vmax = max(vmax, minvalue(result(board, action), alpha, beta))
#         if vmax > beta:
#             return vmax
#         alpha = max(vmax, alpha)
#     return vmax


# def minvalue(board, alpha, beta):
#     vmin = math.inf
#     if terminal(board) == True:
#         return utility(board)
#     for action in actions(board):
#         vmin = min(vmin, maxvalue(result(board, action), alpha, beta))
#         if vmin < alpha:
#             return vmin
#         beta = min(vmin, beta)
#     return vmin


