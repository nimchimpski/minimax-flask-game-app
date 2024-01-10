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
	return [[EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY]]


def player(board):
	"""
	Returns player who has the next turn on a board.
	"""
	d = {'X': 0, 'O': 0, None: 0}
	for i in board:
		for j in i:
			d[j] = d[j] + 1
	if d[X] == d[O]:
		return X
	else:
		return O


def actions(board):
	"""
	Returns set of all possible actions (i, j) available on the board.
	"""
	result = set()
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == EMPTY:
				result.add(tuple([i,j]))
	return result


def result(board, action):
	"""
	Returns the board that results from making move (i, j) on the board.
	"""
	result = copy.deepcopy(board)
	if board[action[0]][action[1]] != EMPTY:
		raise NameError('NotValidAction')
	else:
		result[action[0]][action[1]] = player(board)
	return result


def winner(board):
	"""
	Returns the winner of the game, if there is one.
	"""
	# check rows
	for i in board:
		if i[0] == i[1] == i[2] and i[0] != EMPTY:
			return i[0]
	# check columns
	for i in range(len(board)):
		if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
			return board[0][i]
	if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
		return board[0][0]
	elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
		return board[0][2]
	else:
		return None


def terminal(board):
	"""
	Returns True if game is over, False otherwise.
	"""
    if winner(board) != None:
        return True
    d = {'X': 0, 'O': 0, None: 0}
    for i in board:
        for j in i:
        	d[j] = d[j] + 1
    if d[EMPTY] == 0:
        return True
    return False


def utility(board):
	"""
	Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
	"""
	win = winner(board)
	if win == X:
		return 1
	elif win == O:
		return -1
	else:
		return 0


def max_value(board, alpha, beta):
	"""
	Find maximum value of all possible actions on the board. Recursive.
	"""
	minv = 2
	if terminal(board):
		return utility(board)
	else:
		v = 2
		for action in actions(board):
			v = min(v, min_value(result(board, action), alpha, beta))
			if v < minv:
				minv = v
			if minv <= alpha:
				return minv
			if minv < beta:
				beta = minv
		return v


def min_value(board, alpha, beta):
	"""
	Find minimum value of all possible actions on the board. Recursive.
	"""
	maxv = -2

	if terminal(board):
		return utility(board)
	else:
		v = -2
		for action in actions(board):
			v = max(v, max_value(result(board, action), alpha, beta))
			if v > maxv:
				maxv = v
			if maxv >= beta:
				return maxv
			if maxv > alpha:
				alpha = maxv
		return v


def minimax(board):
	"""
    Returns the optimal action for the current player on the board.
    """
	if terminal(board):
		return None
	array = dict()
	for action in actions(board):
		if player(board) == X:
			value = max_value(result(board, action), -2, 2)
			array[action] = value
		else:
			value = min_value(result(board, action), -2, 2)
			array[action] = value
	if player(board) == X:
		return max(array, key=lambda unit: array[unit])
	else:
		return min(array, key=lambda unit: array[unit])