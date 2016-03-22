from utils import *


def compute_utility(state):
    if state.utility != 0:
        return state.utility * infinity
    "If X wins with this move, return 1; if O return -1; else return 0."
    for move in state.moves:
        x = (k_in_row(state.board, move, state.to_move, (0, 1)) +
             k_in_row(state.board, move, state.to_move, (1, 0)) +
             k_in_row(state.board, move, state.to_move, (1, -1)) +
             k_in_row(state.board, move, state.to_move, (1, 1)))
        player = if_(state.to_move == 'X', 'O', 'X')
        x -= (k_in_row(state.board, move, player, (0, 1)) +
              k_in_row(state.board, move, player, (1, 0)) +
              k_in_row(state.board, move, player, (1, -1)) +
              k_in_row(state.board, move, player, (1, 1)))
    return x


def k_in_row(board, move, player, (delta_x, delta_y)):
    x, y = move
    distancia = 1
    h = 0
    while 0 <= x < 6 and 0 <= y < 5:
        if board.get((x, y)) == player:
            h += 50 * distancia
        if board.get((x, y)) is None:
            h += 25 * distancia
        distancia += 1
        x, y = x + delta_x, y + delta_y
    return h
