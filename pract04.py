import games
import heuristic

game = games.ConnectFour()
state = game.initial

player = 'X'

mode = raw_input("1: Multiplayer, 2: vs CPU")


def check_legal_move(y):
    while y < 1 or y > 7:
        y = int(raw_input("Movimiento invalido, por favor vuelva a intentarlo"))
    return y


def single_player():
    global state, player
    col_str = raw_input("Movimiento: ")
    y = check_legal_move(int(col_str))
    coor = int(str(y).strip())
    x = coor
    y = -1
    legal_moves = game.legal_moves(state)
    for lm in legal_moves:
        if lm[0] == x:
            y = lm[1]
    state = game.make_move((x, y), state)
    if player == 'X':
        player = 'O'
    else:
        player = 'X'


while True:
    print "Jugador a mover:", game.to_move(state)
    game.display(state)
    if int(mode) == 1:
        single_player()
    if int(mode) == 2:
        if player == 'O':
            col_str = raw_input("Movimiento: ")
            y = check_legal_move(int(col_str))
            coor = int(str(y).strip())
            x = coor
            y = -1
            legal_moves = game.legal_moves(state)
            for lm in legal_moves:
                if lm[0] == x:
                    y = lm[1]
            state = game.make_move((x, y), state)
            if y >= 0:
                player = 'X'
            else:
                print "Imposible mover alli, pruebe otra columna"
        else:
            print "Thinking..."
            move = games.alphabeta_search(state, game, d=4 , cutoff_test=None, eval_fn=heuristic.best_move_heuristic2)
            state = game.make_move(move, state)
            player = 'O'
        print "-------------------"
        if game.terminal_test(state):
            game.display(state)
            print "Final de la partida"
            break
