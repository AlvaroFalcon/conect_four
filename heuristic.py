from utils import *
from random import randint


def compute_utility(state):
    x = 0
    # if state.utility != 0:
    #     return state.utility * 10000000000
    for move in state.moves:
        x -= (calculateValue(state.board, move, state.to_move, (0, 1)) +
              calculateValue(state.board, move, state.to_move, (1, 0)) +
              calculateValue(state.board, move, state.to_move, (1, -1)) +
              calculateValue(state.board, move, state.to_move, (1, 1)))
        player = if_(state.to_move == 'X', 'O', 'X')
        x += (calculateValue(state.board, move, player, (0, 1)) +
              calculateValue(state.board, move, player, (1, 0)) +
              calculateValue(state.board, move, player, (1, -1)) +
              calculateValue(state.board, move, player, (1, 1)))
    # print "valor de X", x
    return x


def calculateValue(board, move, player, (delta_x, delta_y)):
    x, y = move
    distancia = 1
    h = 0
    while 0 <= x < 6 and 0 <= y < 5:
        if board.get((x, y)) == player:
            h += 50 / distancia
        elif board.get((x, y)) is None:
            # print("tolete")
            # print board.get((x+1,y))
            # print board
            if board.get((x + 1, y)) != None and board.get((x + 1, y)) != player:
                if board.get((x - 1, y)) != None and board.get((x - 1, y)) != player:
                    h += 500000000
                    print("holita wey")
            h+=10
        else:
            h += 25 / distancia
        distancia += 5
        x, y = x + delta_x, y + delta_y
    return h


def random_heuristic(state):
    return randint(-200, 200)