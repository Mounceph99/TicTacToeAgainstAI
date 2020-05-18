# TicTacToeAgainstAI by Mounceph Morssaoui

# Description

This program, written in Python, allows its users to play Tic Tac Toe against an AI. This program offers a simple and easy-to-use GUI to ply the game. The AI is offered in two difficulties which are "dumb" and "smart". The smart AI uses an algorithm called MINIMAX. paired up with ALPHA-BETA PRUNING to decide on which move is optimal depending on the current state of the Tic Tac Toe. Have fun!!!!

# Algorithm for Smart AI
The algorithm for the Smart AI is MINIMAX, which is paired up with ALPHA-BETA PRUNING.
## Minimax
Essentially, MINIMAX helps the AI decide what is the optimal decision based on the current state of the Tic Tac Toe. It analyzes all current and future possible decisions and returns a score for the respective outcome. With respect to the AI, the AI wants to maximize its score, while the player wants to minimize its score. An outcome where the AI wins would return a positive score, while an outcome where the player wins would return a negative score. (A Tie is zero). The AI essentially creates a tree of possible game outcome, and selects the outcome with the maximizing score, the optimal move. This algorithm is good for Tic Tac Toe because there is no way of predicting the player's behaviour, there are three ways for the game to end (i.e. Win-Lose-Tie). This algorithm is a recursive algorithm and after each recursive call, alternates between the maximizing and the minimizing player.
## Alpha-Beta Pruning
The MINIMAX algorithm was paired up with ALPHA-BETA PRUNING to drastically reduce the number of computations. The MINIMAX algorithm by itself can be slow as it is naive, it tries all possibilities. ALPHA-BETA PRUNING improves the performance drastically without affecting the results of the algorithm. This add-on will force MINIMAX to stop searching when it evaluated at least one move that was worse, respective of the maximizing/minimizing player. Essentially, pruning the branch or path. 

Function: 


# Algorithm for dumb AI
For this program, the dumd AI simply picks its move randomly. Basically, the AI seems as if it has no notion of the current or future state of the game. 

To make an AI that is slightly smarter than the dumb AI, but dumber than the smart AI. A depth variable could be added to the minimax call tree to limit how far in the "future" the AI can see. The call would be made with a depth of 0, and every recursive call would increase the depth. The base case would have an added case for when the depth has reach MAX_DEPTH.

Function: 

# How to play

Note: Make sure to have cloned the repo

1. Open PlayTTT.exe, which can be found in folder TicTacToeAPI.
2. Click on a square to draw an X
3. Wait for the AI to play
4. Repeat 2-3 until there is a winner or a tie.
5. To play again or restart the game at any time, click on the buttons at the bottom of the GUI. Select desired level for AI.

Good luck against the smart AI ;)
