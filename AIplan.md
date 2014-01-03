Here is the current plan for the AI:
-

We should probably do minimax with alpha-beta pruning, which is a lookahead method.  
The "alpha-beta pruning" is slightly more complex, but it will save a ton of execution time if done correctly.

here is some pseudocode for the algorithm. [source](http://ai-depot.com/articles/minimax-explained/2/)

    MinMax (GamePosition game) {
      return MaxMove (game);
    }
     
    MaxMove (GamePosition game, Integer alpha, Integer beta) {
      if (GameEnded(game) || DepthLimitReached()) {
        return EvalGameState(game, MAX);
      }
      else {
        best_move < - {};
        moves <- GenerateMoves(game);
        ForEach moves {
           move <- MinMove(ApplyMove(game), alpha, beta);
           if (Value(move) > Value(best_move)) {
              best_move < - move;
              alpha <-  Value(move);
           }
     
           // Ignore remaining moves
           if (beta > alpha)
             return best_move;
        }
        return best_move;
      }
    }
     
    MinMove (GamePosition game) {
      if (GameEnded(game) || DepthLimitReached()) {
        return EvalGameState(game, MIN);
      }
      else {
        best_move < - {};
        moves <- GenerateMoves(game);
        ForEach moves {
           move <- MaxMove(ApplyMove(game), alpha, beta);
           if (Value(move) > Value(best_move)) {
              best_move < - move;
              beta <- Value(move);
           }
     
           // Ignore remaining moves
           if (beta < alpha)
             return best_move;
        }
        return best_move;
      }
    }
    
Now, there are a few things that have to be worked out.

First there is the `GenerateMoves()` function.  This will create a list of valid moves for a player during the game.
Basically, this is simulating the future of the game by listing through every possible imput and determining
the validity of the move.
Note: it must keep track of whose turn it is (this isn't shown as an argument, but probably should be).

Next, there is the `EvalGameState()` function.  This is the thing that drives the AI.
Don't get it wrong, or else the AI won't play the game well.

Here is my proposed function, written in pseudocode:

    EvalGameState (game) {
      if (human number of pieces == 0) 
        return 1337                        #large value so that victory/defeat outweighs anything
      if (cpu number of pieces == 0)
        return -1337
      totalscore = 0
      ForEach piece {
        # this implements that picture I kept posting
        piecescore = max(abs(xpos - 3.5), abs(ypos - 3.5)) + .5  #assumes x and y are measured from 0 to 7
        if (piece is promoted)
          piecescore = 5
        if (piece is human)
          piecescore *= -1
        totalscore += piecescore
      return totalscore
    
The basic idea is that the weight of non-promoted pieces depends on their position on the board.  Pieces either gaurding the back rows or advancing to the very top are worth more.  Also, the weight of promoted pieces does not depend on board position. This is to allow the endgame to function properly, otherwise the pieces will stick to the edges instead of going after the opponent.  It is important to note that large values are good for the AI.
