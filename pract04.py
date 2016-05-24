import games
import heuristic

game = games.ConnectFour()
state = game.initial

mode = raw_input("1: Multiplayer, 2: vs CPU, 3: CPU vs CPU")

while int(mode) > 3 or int(mode) < 1:
    print "Incorrect mode, please try again"
    mode = raw_input("1: Multiplayer, 2: vs CPU, 3: CPU vs CPU")
if int(mode) == 1 or int(mode) == 3:
    player = 'X'
else:
    turn = raw_input("1: First, 2: Second")
    if int(turn) > 2 or int(turn) < 1:
        while int(turn) > 2 or int(turn) < 1:
            print "Incorrect, please try again"
            turn = raw_input("1: First, 2: Second")
    if int(turn) == 1:
        player = 'O'
    else:
        player = 'X'

    difficult = raw_input("1: Easy, 2: Medium, 3: Hard")
    while int(difficult) < 1 or int (difficult) > 3:
        print "Incorrect difficult, please try again"
        difficult = raw_input("1: Easy, 2: Medium, 3: Hard")


def check_legal_move(y):
    while y < 1 or y > 7:
        y = int(raw_input("Invalid move, try again"))
    return y


def multi_player():
    global state, player
    col_str = raw_input("Move: ")
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

def cpu_play():
    global state, player
    if player == 'X':
        print "Thinking..."
        move = games.alphabeta_search(state, game, d=4 , cutoff_test=None, eval_fn=heuristic.best_move_heuristic2)
        state = game.make_move(move, state)
        player = 'O'
    else:
        print "Thinking..."
        move = games.alphabeta_search(state, game, d=1 , cutoff_test=None, eval_fn=heuristic.random_heuristic)
        state = game.make_move(move, state)
        player = 'X'


while True:
    print "Player to move:", game.to_move(state)
    game.display(state)
    if int(mode) == 1:
        multi_player()
        if game.terminal_test(state):
            game.display(state)
            print "Game over"
            break
    if int(mode) == 3:
        cpu_play()
        if game.terminal_test(state):
            game.display(state)
            print "Game over"
            break
    if int(mode) == 2:
        if player == 'O':
            col_str = raw_input("Move: ")
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
                print "Cant move there, try another column"
        else:
            print "Thinking..."
            if int(difficult) == 2:
                move = games.alphabeta_search(state, game, d=4 , cutoff_test=None, eval_fn=heuristic.best_move_heuristic2)
            elif int(difficult) == 3:
                move = games.alphabeta_search(state, game, d=6 , cutoff_test=None, eval_fn=heuristic.best_move_heuristic2)
            else:
                move = games.alphabeta_search(state, game, d=4 , cutoff_test=None, eval_fn=heuristic.random_heuristic)
            state = game.make_move(move, state)
            player = 'O'
        print "-------------------"
        if game.terminal_test(state):
            game.display(state)
            print "Game over"
            break
