#
# Author: Mounceph Morssaoui
# Github: Mounceph99
# Created May 16, 2020
# Last modified: May 18, 2020
#
# Description:
# This program offers an API for Tic Tac Toe (TTT) with an AI with traditional TTT rules. The AI is implemented 
# using an algorithm called Minimax. To reduce the number of computation, the Minimax algorithm is paired 
# with alpha-beta pruning, this allows the AI to make a decision faster.

################################################
# Imports body section
################################################

# Import os package to clear sceen
from os import system, name

# Import random for dumb ai implementation
from random import choice

# Import math for alpha-beta pruning implementation
from math import inf

#############################################
# Function body section
################################################

# This function will clear the console
def cls():
    # Windows OS
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


# This function prints a dashed line to separate between each row
def print_line():
    print("-----------")

#This function prints the TTT board to the console
def printTTT(board):
    print()
    for row,y in zip(board, range(0,len(board))):
        for col,i in zip(row, range(0,len(row))):
            if i == len(row)-1:
                print(" " + str(col))
            else:
                print(" " + str(col) + " |",end= "")
        if y != len(board)-1:
            print_line()
        

#This function initializes a 3x3 TTT empty board and returns it
#Creates and returns a 2D list
def initTTT():

    empty_board = []
    for row in range(3):
        empty_board.append([])
        for _ in range(3):
            empty_board[row].append(" ")

    return empty_board

#This function verifies if the current state of the board
#For player and the dumb AI
#returns true if there is a winner or a tie
#else return false as the game is not over
#For smart AI and minimax implementation
#returns score: 
#{O:1,X:-1,Tie:0}
def hasWon(board, minimax = False, isMaximizing = False):
    won = check_horizontal(board) or check_vertical(board) or check_diagonal(board)
    if not minimax:
        return won
    else:
        if won:
            if not isMaximizing:
                return 1
            else:
              return -1
        else:
            return 0     


#This function checks if the TTT board is full, implying that there is likely a tie
def is_full_TTT(board):
    for row in board:
        for pos in row:
            if pos == " ":
                return False

    return True

#This function returns whether the game is over of not
def game_over(board, turn, minimax = False):
    if not minimax:
        visualTTT(board)

    if hasWon(board):                  
        return True
    
    if is_full_TTT(board):    
        return True

    return False

#This function checks if the current move wins horizontally
#returns true if move wins
#return false if move does not win
def check_horizontal(board):
    
    for row in board:
        #Check if a row have all the same symbol, check any item of 
        #the row to make sure its not an empty space
        if (row[0] == row[1] == row[2]) and row[0] != " ":
            # A winning row has been found
            return True

    #No rows have proven to win
    return False

#This function checks if the current move wins vertically
#returns true if move wins
#return false if move does not win
def check_vertical(board):
    
    for i in range(0,len(board)):
        #Check if a col have all the same symbol, check any item of 
        #the row to make sure its not an empty space
        if (board[0][i] == board[1][i] == board[2][i]) and board[0][i] != " ":
            # A winning col has been found
            return True

    #No col have proven to win
    return False

#This function checks if the current move wins diagonally
#returns true if move wins
#return false if move does not win
def check_diagonal(board):
    
    left_diagonal = (board[1][1] == board[2][2] == board[0][0] and board[0][0] != " ")
    right_diagonal = (board[1][1] == board[2][0] == board[0][2] and board[0][2] != " ")
    #Returns True atleast one diagonal is True
    return (left_diagonal or right_diagonal)

# This function changes the turn to the next play
def change_turn(myturn):
    return not myturn
    

# This function updates the TTT board if the last move made is valid, 
# a valid move is one that has not been played yet
# return true and update TTT board if valid,
# else return false without updating the board
def updateTTT(board, row, col, move, minimax = False):
    # Move cannot be played since it has already been played
    if board[row][col] != " ":
        if not minimax:
            visualTTT(board)
        return False

    # Move can be played, update board
    board[row][col] = move

    if not minimax:
            visualTTT(board)
    return True


#This function plays a move for a dumb AI.
#The dumb AI plays a random move, it doesn't take any board state into account
def dumb_AI(board):
    ai_finish = False
    #All possible move stored into a list
    moves = []
    for i in range(0,len(board)):
        for y in range(0,len(board)):
            if board[i][y] == " ":
                moves.append([i,y])

    #If there are no longer any moves left, simply return
    if len(moves) == 0:
            return
    
    #while not ai_finish:
    play_move = moves.pop(choice(range(0,len(moves))))
    row = play_move[0]
    col = play_move[1]
    #ai_finish = updateTTT(board,row,col,"O")
    updateTTT(board,row,col,"O")
    #The return is for the GUI, in order to update the GUI
    #Note that it could be done another way, (copy the board list) but this is faster
    return [row, col]

#This function plays a move for a smart AI.
#The smart AI plays a move taking into account the current and future state
#of the TTT to play the best move
def smart_AI(board):
    best_score = -inf
    best_row = -1
    best_col = -1
    #Create a temp board that is a copy of the real board for the minimax algo
    TTTBoard = board.copy()
    
    for i in range(0,len(board)):
        for y in range(0,len(board)):
            if (TTTBoard[i][y] == " "):
                TTTBoard[i][y] = "O"
                score = minimax(board,False)
                TTTBoard[i][y] = " "
                if score > best_score:
                    best_score = score
                    best_row = i
                    best_col = y

    #Update real board
    updateTTT(board,best_row, best_col,"O")
    
    #The return is for the GUI, in order to update the GUI
    #Note that it could be done another way, (copy the board list) but this is faster
    return [best_row,best_col]

#This function is a recursive call for an algo called minimax, which assures
#the AI picks the optimal move.
#To reduce computation, minimax is implemented with alpha-beta pruning.
def minimax(board, isMaximizing, alpha = -inf, beta = inf):

    #Return the score of the board when the game is over
    #{O :1, X :-1, Tie :0}
    if game_over(board, isMaximizing, True):
        return hasWon(board,True,isMaximizing)          

    #Note: AI is maximizing, therefore the player is minimizing relatively to the AI

    #Assume it is the AI turn (Maximixing), what would he do?
    #The AI goal is to maximize its own score
    if isMaximizing:
        #Set the optimal move score to the worst it can be relatively
        optimal = -inf
        #Try all possible moves
        for i in range(0,len(board)):
            for y in range(0,len(board)):
                #Available move
                if (board[i][y] == " "):
                    #Update board temporarily with "O"
                    board[i][y] = "O"
                    #Recursive call, switching to MINIMIZING player (player)
                    point = minimax(board, False,alpha,beta) 
                    #Restore board before minimax call
                    board[i][y] = " "
                    #Maximize score, chose the best move relatively
                    optimal = max(optimal, point)
                    #alpha-beta pruning algorithm, if the MAXIMIZING score finds WORSE SCORE board 
                    #Stop the search. Basically cuts branches that cannot influence the final decision
                    #which makes the minimax algorithm faster.
                    alpha = max(alpha,point)
                    if beta <= alpha:
                        break
        return optimal
    #Assume it is the player's turn (Minimizing), what would he do?
    #The AI goal is to minimize the player's score
    else:
        #Set the optimal move score to the worst it can be relatively
        optimal = inf
        #Try all possible moves
        for i in range(0,len(board)):
            for y in range(0,len(board)):
                #Available move
                if (board[i][y] == " "): 
                    #Update board temporarily with "X"
                    board[i][y] = "X"
                    #Recursive call, switching to MAXIMIZING player (AI)
                    point = minimax(board, True,alpha,beta)
                    #Restore board before minimax call
                    board[i][y] = " "
                    #Maximize score, chose the best move relatively
                    optimal = min(optimal, point)
                    #alpha-beta pruning algorithm, if the MINIMIZING score finds BETTER SCORE board 
                    #Stop the search. Basically cuts branches that cannot influence the final decision
                    #which makes the minimax algorithm faster.
                    beta = min(beta,point)
                    if beta <= alpha:
                        break
        return optimal
               



#This function let the user play his move when played on the console
def player_move(board):
    
    #Loop until the player played a valid move
    while True:

        #Loops until a valid row has been inputted by the player
        while True:
            row = int(input("Please enter in which row you'd like to play on: "))
            #A valid row is from 0 to 2 inclusively
            valid_row = (row >= 0 and row <=2)
            if not valid_row:
                visualTTT(board)
                #prompt message for user to enter a good row
                print("Invalid move, please enter a valid move.")
                print("Note: Row values are limited to {0,1,2}")
            else:
                #player entered a valid row, break out of infinite loop
                visualTTT(board)
                break

        while True:
            col = int(input("Please enter in which col you'd like to play on: "))
            #A valid col is from 0 to 2 inclusively
            valid_col = (col >= 0 and col <=2)
            if not valid_col:
                visualTTT(board)
                #prompt message for user to enter a good col
                print("Invalid move, please enter a valid move.")
                print("Note: Column values are limited to {0,1,2}")
            else:
                #player entered a valid col, break out of infinite loop
                visualTTT(board)
                break
        #A valid move cannot be one that has already been played, loop again
        if not updateTTT(board,row,col,"X"):
            print("Please play a move that has not been played already.")
        else:
            #If playing on console, the return statement
            return (3*row + col)

#This function clears the screen and print the TTT for a clean 
#representation of the console the state of the game
def visualTTT(board):
    cls()
    printTTT(board)


#This function incorporates all previous functions in order to play TTT on the console
#Exits when game is over.
def tic_tac_toe(ai = "dumb", playerbegin = True):
    #Declare and Initialize empty TTT game board 
    board = initTTT()

    # Declare and init turn, to change turn call function change_turn()
    # For simplicity, True refers to the user, False to the AI
    #User start
    player_turn = playerbegin #False would have the AI start

    #Play TTT
    while not game_over(board,player_turn):
        if player_turn:
            player_move(board)
        elif ai == "dumb":
            dumb_AI(board)
        elif ai == "smart":
            smart_AI(board)
        else:
            print("ERROR: Dont know whose turn it is")
            exit()
        #Alternate turn
        player_turn = change_turn(player_turn)


#end
