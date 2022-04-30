"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math


X = "X"
O = "O"
EMPTY = None
INFINITY = 100000000


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
    x_count = 0
    o_count = 0

    # For each O or X entry in the board add one to the o or x counter
    for row in board: 
        for field in row:
            if field == X:
                x_count += 1

            if field == O:
                o_count += 1

    if x_count == o_count:
        return X

    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for row in range(len(board)):
        for column in range(len(board[0])):

            if board[row][column] == EMPTY:
                possible_actions.add((row, column))

    return possible_actions


def validate_action(board, action):

    if board[action[0]][action[1]] == EMPTY:
        return True

    else:
        return False
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Get the current player
    current_player = player(board)

    if not validate_action(board, action):
        print("---------------------")
        print("not a valid action")
        print("Action : ", action)
        print("Board : \n", board)
        raise ValueError

    deep_copy_of_board = deepcopy(board)
    
    deep_copy_of_board[action[0]][action[1]] = current_player

    return deep_copy_of_board

def evaluate_diagonals(board):
    if board[0][0] == board[1][1] == board[2][2]:
        return (0, 0)

    if board[2][0] == board[1][1] == board[0][2]:
        return (2, 0)

    return None

def evaluating_horizontals(board):
    for row_index in range(len(board)):
        if board[row_index][0] != EMPTY and same_field_values(board[row_index]):
            return (row_index, 0)

    return None

def evaluating_verticals(board):
    for column_index in range(len(board)):
        colum_values = []
        for row_index in range(len(board)):
            colum_values.append(board[row_index][column_index])

        if board[0][column_index] != EMPTY and same_field_values(colum_values):
            return (0, column_index)

    return None

def get_winner(board, coordinates):
    winner = board[coordinates[0]][coordinates[1]]
    return winner

def same_field_values(array):
    return all(x == array[0] for x in array)

def get_winner_coordinates(board):
    coordinates = ()

    # Evaluating horizontals
    if evaluating_horizontals(board) != None:
        coordinates = evaluating_horizontals(board)

    # Evaluating verticals
    if evaluating_verticals(board) != None:
        coordinates = evaluating_verticals(board)

    # Evaluating diagonals
    if evaluate_diagonals(board) != None:
        coordinates = evaluate_diagonals(board)

    return coordinates if len(coordinates) != 0 else None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None
    winner_coordinates = get_winner_coordinates(board)
    if winner_coordinates != None:
        winner = get_winner(board, winner_coordinates)

    return winner
    
    
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    game_is_over = False

    # If winner != None, there is a winner and the game is over
    if winner(board) != None:

        game_is_over = True
        return game_is_over

    # If there is no winner, the game has either ended in a tie or is still 
    # in progress
    else:

        # Check if there are empty fields in the board
        empty_fields_in_board = any(EMPTY in row for row in board)

        # If there are no empty fields the game has ended in a tie
        if not empty_fields_in_board:
            game_is_over = True
            return game_is_over

        # If there are empty fields left in the board, the game is not over
        else:

            return game_is_over

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # We assume that utility will only be called on a terminal board
    winner_of_game = winner(board)

    if winner_of_game == X:
        return 1

    elif winner_of_game == O:
        return -1
    
    elif winner_of_game == None:
        return 0

    else:
        raise ValueError





def min_value(board):
    v = INFINITY

    # If the game is over return the utility (1, 0 -1)
    if terminal(board):
        return utility(board)

    # Get all the possible actions
    possible_actions = actions(board)

    for action in possible_actions:
        resulting_board_for_action = result(board, action)
        v = min(v, max_value(resulting_board_for_action))
    return v

def max_value(board):
    v = -INFINITY

    # If the game is over return the utility (1, 0 -1)
    if terminal(board):
        return utility(board)

    # Get all the possible actions
    possible_actions = actions(board)

    for action in possible_actions:
        resulting_board_for_action = result(board, action)
        v = max(v, min_value(resulting_board_for_action))
    
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check if the game is over
    if terminal(board):
        return None

    values_of_actions =  {}

    if player(board) == X:
        for action in actions(board):
            temp = min_value(result(board, action))
            values_of_actions[action] = temp
            values_of_actions = dict(sorted(values_of_actions.items(), key=lambda item: item[1]))
    else:
        for action in actions(board):
            temp = max_value(result(board, action))
            values_of_actions[action] = temp
            values_of_actions = dict(sorted(values_of_actions.items(), key=lambda item: item[1], reverse=True))

    keys_of_dict = list(values_of_actions.keys())
    best_move = keys_of_dict[-1]
    return best_move



    
