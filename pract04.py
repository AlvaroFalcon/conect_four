import games
import heuristic

game = games.ConnectFour()
state = game.initial

player = 'X'

columns = [6, 6, 6, 6, 6, 6]
mode = raw_input("1: Multiplayer, 2: vs CPU")


def check_legal_move(y):
    while y < 0 or y > 5:
        y = int(raw_input("Movimiento invalido, por favor vuelva a intentarlo"))
    return y


def player_move():
    global column, y, x, state, player
    print_board(state)
    column = raw_input("Elija la columna en la que desea jugar (0-5)")
    y = check_legal_move(int(column))
    x = columns[y]
    state = game.make_move((x, y), state)
    columns[y] -= 1
    if player == 'X':
        player = 'O'
    else:
        player = 'X'


def print_board(state):
    game.display(state)
    print "Jugador a mover:", game.to_move(state)


while True:
    if int(mode) == 1:
        player_move()
        print "-------------------"
    if int(mode) == 2:
        if player == 'X':
            player_move()
        else:
            print "Thinking..."
            print_board(state)
            move = games.alphabeta_search(state, game, d=10, cutoff_test=None, eval_fn=heuristic.compute_utility)
            state = game.make_move(move, state)
            player = 'X'
        print "-------------------"
    if game.terminal_test(state):
        game.display(state)
        print "Final de la partida"
        break
