# Connect 4

### I'm doing this game for a class project and using teacher's source code. I tried to implement it with a visual view but i had a lot of problems and I had to re-start the project so it's still in process.
#### I pretend to make the visual view using the external library "pygame", easy and useful.

#### The current features of the application are:

* Multiplayer (local).
* Vs CPU(with a difficulty selector).
* ~~Hint assistance (Ask the heuristic where you should play).~~
* ~~Tells you the last movement of both players.~~
* Tells you who's actual playing (player turn).
* Game over screen which says who won.
* A good heuristic, still need to be more tested but it works pretty good.

#### The problems I'm having:
For the moment the only problems I had were with the visual view, now that i changed back to the text-view it works pretty good, never had an exception and fixed things like, you cant put more elements in the column when its full, etc...


#### Future features for this project:
* Implementation again of the visual view with all its features.
* X*Y board size
* Maybe some cool background music and/or some more visual effects


For the moment i'll focus on testing the heuristic and make it godlike, then i'll try to make the visual view again and the future features.


### How does the heuristic works?
Well, I'm using my teacher's alpha-beta search source code:
```python

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for (a, s) in game.successors(state):
            v = min(v, max_value(s, alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
```
Where the eval_fn is the heuristic method, which is None if you don't specify it.
This search the best action you can do based on the heuristic you made, you can make it play better my increasing "d" which means depth but it could cost you some time to have an answer.

Now, the heuristic:
```python
def compute_utility(state):
    x = 0
    if state.utility != 0:
        return state.utility * 10000000000000
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
    return x


def calculateValue(board, move, player, (delta_x, delta_y)):
    x, y = move
    distancia = 1
    h = 0
    while 0 <= x <= 6 and 0 <= y <= 5:
        if board.get((x, y)) == player:
            h += 50 / distancia
        elif board.get((x, y)) is None:
            if board.get((x, y + 1)) is not None and board.get((x, y + 1)) != player:
                if board.get((x, y - 1)) is not None and board.get((x, y - 1)) != player:
                    h += 50000000
            h += 10
        else:
            h += 25 / distancia
        distancia += 5
        x, y = x + delta_x, y + delta_y
    return h
```
First of all it checks if the actual state it's in a critic situation (win or lose) with this method:
```python
if state.utility != 0:
    return state.utility * 10000000000000
```
state.utility retuns 1 if its a possitive play (win) or -1 if its a negative (lose), so here we check if its != 0 and return the value * a very high value (best value could be infinity). This high value returned will be the key to block/win the game if we got the chance.

The rest of the heuristic it's simple, first it calculates the enemy heuristic-value(for every possible move) for the state (negative value) and then the player(cpu) heuristic-value (positive) and then return the enemy value plus player value
```python
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
return x
```
Well, here is how to calculate the heuristic-value:
```python
def calculateValue(board, move, player, (delta_x, delta_y)):
    x, y = move
    distance = 1
    h = 0
    while 0 <= x <= 6 and 0 <= y <= 5:
        if board.get((x, y)) == player:
            h += 50 / distance
        elif board.get((x, y)) is None:
            if board.get((x, y + 1)) is not None and board.get((x, y + 1)) != player:
                if board.get((x, y - 1)) is not None and board.get((x, y - 1)) != player:
                    h += 50000000
            h += 10
        else:
            h += 25 / distance
        distance += 5
        x, y = x + delta_x, y + delta_y
    return h
```
This is very simple, it returns a value for the actual move depending of the state, getting a different value if it finds an enemy, a player or a None(every time it finds an enemy or player, it will divide the value by the "distance").

I thought of improving it by adding a random positive number if it finds a None (Still have to test it)

The calculateValue checks too if the board its like:

X-O-O---X

If you have a blank (None) betweens two enemies, it will give a very high value (to block it) because it's probably a play trying to fool the heuristic(The value will be below the winning/losing returned value, to keep it the most important)

### Future changes to the heuristic:
* Memoize to make it faster and better
* Test adding a random possitive value (below the player default value)
* Test dividing the enemy value and multiplying the player value

If you need something or have some tips for me, dont be shy and [contact](http://alvaroulpgc.github.io/contact.html) me
