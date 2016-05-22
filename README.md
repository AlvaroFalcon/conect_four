# Connect 4

This is a project we made for a subject. It's very simle and we based our code in [our teacher's source code](https://github.com/cayetanoguerra/fsi/tree/master/Week%204%20-%20Conecta%204).

# Table of contents
* [How does it work?](#howwork)
* [Features.](#features)
  * [Player vs player](#playervsplayer)
  * [Player vs CPU](#playervscpu)
     * [Heuristic](#heuristic)
        * [Random](#random)  
        * [Best move](#best)  
  * [CPU vs CPU](#cpuvscpu)
  * [Memoize]()


# How does it work? <a name="howwork"><a/>  

Well, we've implemented a text-based menu to start the game with the user's preferences (game mode, difficulty, etc...):
```python
mode = raw_input("1: Multiplayer, 2: vs CPU, 3: CPU vs CPU ")

while int(mode) > 3 or int(mode) < 1:
    print "Incorrect mode, please try again"
    mode = raw_input("1: Multiplayer, 2: vs CPU, 3: CPU vs CPU ")
if int(mode) == 1 or int(mode) == 3:
    player = 'X'
else:
    turn = raw_input("1: First, 2: Second ")
    if int(turn) > 2 or int(turn) < 1:
        while int(turn) > 2 or int(turn) < 1:
            print "Incorrect, please try again"
            turn = raw_input("1: First, 2: Second ")
    if int(turn) == 1:
        player = 'O'
    else:
        player = 'X'

    difficult = raw_input("1: Easy, 2: Medium, 3: Hard ")
    while int(difficult) < 1 or int(difficult) > 3:
        print "Incorrect difficult, please try again"
        difficult = raw_input("1: Easy, 2: Medium, 3: Hard ")

```
Here you can see how we initialize all our preferences variable (mode, difficult and turn).  
With this menu you can select the mode you want to play, the difficult (Easy(random heuristic), Medium and Hard(the difference between medium and hard is the depth)), and you also can select if you want to play first or second. After getting the values we check if the user introduced "legal values", for example, if the user enters a 4 in the mode selection, he'll get an error and he'll has to introduce the value again.

After getting correctly all the values, the game starts with its game-loop (while true)
# Features <a name="features"><a/>  
## Player vs player  <a name="playervsplayer"><a/>
We've implemented a feature to allow two players to play.  
This was the easiest way to start because we could understand the code and check it working.  
It's very simple, in our game loop (while true) we call our "multi_player" function:

```python
def multi_player():
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
```  

<a name="endgame"><a/>  

This function ask us for the column we want to play, does the move and changes the player. After this, we must check our game loop if we've reached a final state (4 in row) with our movement, we do it at the end of our game loop:
```python
if game.terminal_test(state):
    game.display(state)
    print "Game over"
    break
```  
This functon checks if we've won or lost and stop the game loop in a positive case.

## Player vs CPU <a name="playervscpu"><a/>  
Once we understood how the Conect Four source code worked, we started implementing a Player vs CPU feature, we just had to create a good [heuristic](#heuristic) for the game and use it on the alphabeta search.

Here is the "mode" of player vs CPU, here we check if the actual turns (player variable) belongs to 'O'(human) or 'X'(machine) and make the movement.   


Here we control the difficult on the CPU, we do it with a variable we ask at the start, "difficult". If the difficult it's 2, then we call our heuristic with depth 4, if it's 3, we call it with depth 5 and if it's 1 (easy) we call our random heuristic.
```python
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
              move = games.alphabeta_search(state, game, d=5 , cutoff_test=None, eval_fn=heuristic.best_move_heuristic2)
          else:
              move = games.alphabeta_search(state, game, d=4 , cutoff_test=None, eval_fn=heuristic.random_heuristic)
          state = game.make_move(move, state)
          player = 'O'
```  



## Heuristic <a name="heuristic"></a>
We've implemented two-type heuristic, firstly we did a random heuristic to understand how it works and then we started implementing and improving our best-move heuristic.

### Random move heuristic <a name="random"><a/>  

Our first version of random heuristic was like:
```python
def random_heuristic(state):
    return randint(-200, 200)
```

But we felt that we could improve it to at least block the enemy and win if possible:
```python
def random_heuristic(state):
    if state.to_move == 'X':
        if state.utility != 0:
            return state.utility * infinity
    else:
        if state.utility != 0:
            return state.utility * -infinity
    return randint(-200, 200)
```
We did it possible adding the state utility, which returns 1 if the player wins, -1 if the enemy wins or 0 in other case. If someone wins, we just return the state.utility value * infinity, giving it the max priority.

### Best move heuristic  <a name="best"><a/>  
Later on, after a lot of failure tries, we did an heuristic that looks for the best move possible in the state. To do this, firstly we got all the legal moves by the legal_moves function declared in game.py, we just copied that into our heuristic.py.
```python
def legal_moves(state):
    "Legal moves are any square not yet taken."
    return [(x, y) for (x, y) in state.moves
            if y == 1 or (x, y-1) in state.board]
```
To calculate the *heuristic-value* we declared two variables (ally and enemy), then with each one we call the calculate_best function to get the total heuristic value for the enemy and the ally depending on the direction (delta_x and delta_y), after that we return the ally value - the enemy, where ally is the machine and enemy the human.(Returning a possitive value means that the movement its good for the machine and a negative means that the movement its good for the human).
```python


def best_move_heuristic(state):
    if state.to_move == 'X':
        if state.utility != 0:
            return state.utility * infinity
    else:
        if state.utility != 0:
            return state.utility * -infinity
    ally = 0
    enemy = 0
    moves = legal_moves(state)
    for move in moves:
        ally += calculate_best(state.board, move, state.to_move, (0,1))
        ally += calculate_best(state.board, move, state.to_move, (1,0))
        ally += calculate_best(state.board, move, state.to_move, (1,-1))
        ally += calculate_best(state.board, move, state.to_move, (1,1))
        ally += calculate_best(state.board, move, state.to_move, (-1,0))
        ally += calculate_best(state.board, move, state.to_move, (0,-1))
        ally += calculate_best(state.board, move, state.to_move, (-1,1))
        ally += calculate_best(state.board, move, state.to_move, (-1,-1))

        player = if_(state.to_move == 'X', 'O', 'X')

        enemy += calculate_best(state.board, move, player, (0,1))
        enemy += calculate_best(state.board, move, player, (1,0))
        enemy += calculate_best(state.board, move, player, (1,-1))
        enemy += calculate_best(state.board, move, player, (1,1))
        enemy += calculate_best(state.board, move, player, (-1,0))
        enemy += calculate_best(state.board, move, player, (0,-1))
        enemy += calculate_best(state.board, move, player, (-1,1))
        enemy += calculate_best(state.board, move, player, (-1,-1))
    return ally - enemy
```
And here is the function to calculate the heuristic value, its very simple, it just looks for a 4 in row in the delta_x,delta_y direcion. For each "player" found, k (this is a variable to control if there is a possible 4 in row on that direction, this variable is only increased if a player or None is found) is being increased by 1 , h (heuristic value) it's increased by 70 and f (a value to multiply later the h, we only increase f if a player is found) by 1. If we find a None, the heuristic value is increased by 20.  


After increasing the variable's value, we check if there is actually a possible 4 in row (k == 4) in a possitive case, we multiply the actual heuristic value (h) by f.


If we find an "enemy", we just return 0 because we can't do a 4 in row on that direction.
```python
def calculate_best(board, move, player, (delta_x, delta_y)):
    h = 0
    k = 0
    f = 1
    x, y = move
    while 0 < x < 8 and 0 < y < 7:
        if board.get((x, y)) == player:
            h += 70
            k += 1
            f+=1
            if k == 4:
                h *= f
                return h
        elif board.get((x, y)) is None:
            h += 20
            k += 1
            if k == 4:
                h *= f
                return h
        else:
            return 0

        x += delta_x
        y += delta_y
    return h
```



# CPU vs CPU <a name="cpuvscpu"></a>  
To implement this we just had to call the "cpu_play" method we created in the "mode" 3:
```python
if int(mode) == 3:
    cpu_play()
    if game.terminal_test(state):
        game.display(state)
        print "Game over"
        break
```

As you can see below, the code of cpu_play it's very simple, we just make a movement with our heuristic first ('X') and then change the turn to the other heuristic to make it's move ('O')
```python
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
```
