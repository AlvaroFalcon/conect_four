# Connect 4

This is a project we made for a subject. It's very simle and we based our code in [our teacher's source code](https://github.com/cayetanoguerra/fsi/tree/master/Week%204%20-%20Conecta%204).

# Table of contents
* [Features.](#features)
  * [Player vs player](playervsplayer)
  * [Player vs CPU](playervscpu)
  * [CPU vs CPU](cpuvscpu)
  * [Heuristic](#heuristic)  
  * [Memoize]()
* [How does it work?](#howwork)




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

We also had to "split" the playing modes with a decision at the start of the game (mode selection) and it's as simple as:  
```python
mode = raw_input("1: Multiplayer, 2: vs CPU, 3: CPU vs CPU ")
```  
After this, we had to control
With this we allow the user to select the game mode, we just have to detect in our game loop the game mode and use it. We did this with an if:  
```python
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
```  
As you can see, we decide which game mode we're using based on the input number at the start. Our "mode 2" is the vs CPU feature, what we do here is firstly, detect which player is currently playing (X is the CPU, O the player), if the player is 'O', we do the movement with an input number (column) and before doing the movement we check if that was a valid column, in a negative case, the player must select another column.  

When the player is 'X' it means that's the CPU turn's, here we do the movement calling our alphabeta search with our heuristic and a depth (depending on the difficult).

# CPU vs CPU <a name="cpuvscpu"></a>  
## Still not implemented

#Heuristic <a name="heuristic"></a>
