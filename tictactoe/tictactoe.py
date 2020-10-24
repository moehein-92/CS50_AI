"""Tic Tac Toe Player"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """Returns starting state of the board."""
    
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """Returns player who has the next turn on a board."""
    count_x = 0
    count_o = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == X:
                count_x += 1
            elif board[i][j] == O:
                count_o += 1
        
    if count_x > count_o:
        return O
    else:
        return X

def actions(board):
    """Returns set of all possible actions (i, j) available on the board."""
    moves = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves

def result(board, action):
    """Returns the board that results from making move (i, j) on the board."""
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    """Returns the winner of the game, if there is one."""
    for row in range(3):
        if len(set(board[row])) == 1: 
            return board[row][0] 

    for column in range(3):
        if len(set([row[column] for row in board])) == 1:
            return board[0][column]
            
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]: # Diagonals
        return board[1][1]  

def terminal(board):
    """Returns True if game is over, False otherwise."""
    count_empty = 0
    if winner(board) is not None or (not any(EMPTY in sublist for sublist in board) and winner(board) is None):
        return True
    else:
        return False

def utility(board):
    """Returns 1 if X has won the game, -1 if O has won, 0 otherwise."""
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """Returns the optimal action for the current player on the board."""
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_value(board)
            return move

        elif player(board) == O:
            value, move = min_value(board)
            return move

    # X winning = 1. Therefore, X wants to maximize the score.
    # O winning = -1.  Therefore, O wants to minimize the score.

def max_value(board):
    if terminal(board):
        return utility(board), None

    v = float('-inf')
    move = None
    for action in actions(board):
        x, y = min_value(result(board, action))
        if x > v:
            v = x
            move = action
            if v == 1:
                return v, move

    return v, move

def min_value(board):
    if terminal(board):
        return utility(board), None
        
    v = float('inf')
    move = None
    for action in actions(board):
        x, y = max_value(result(board, action))
        if x < v:
            v = x
            move = action
            if v == -1:
                return v, move
    
    return v, move