#
# Author: Mounceph Morssaoui
# Github: Mounceph99
# Created: May 17, 2020
# Last modified: May 18, 2020
#
# Description:
# This program offers a GUI to play TTT, which uses some functions from TicTacToeAPI.py.
# This GUI is for a User vs AI experience, where the AI level can vary from "dumb" and
# smart from the click of a button. When the game starts the player can play, but the AI
# by default smart. The player and the AI alternate after each game on who starts.
# Have fun :)

################################################
# Imports body section
################################################

# Import Tkinter built-in which is use for Python GUI programming
from tkinter import *
from tkinter import messagebox

# Import builtin GUI programming for Python
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://www.geeksforgeeks.org/python-gui-tkinter/
# Colors: http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png
# Doc on Tkinter Button: https://effbot.org/tkinterbook/button.htm
# Button command function with param: https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
# Obtain text of button: https://stackoverflow.com/questions/26765218/get-the-text-of-a-button-widget
# Lambda button problem: https://stackoverflow.com/questions/16224368/tkinter-button-commands-with-lambda-in-python

#Import my TicTacToeAPI 
from TicTacToeAI import *

################################################
# Function/Class body section
################################################

#This class creates a TTT board GUI. The TTT follows traditional rules and allows a human or player,
#to play against an AI at the desired level by the click of a button. 
#Note: Default level of the AI is smart

class TTTGui:
    #self is equi to 'this'
    #master is equi to root
    def __init__(self, master):
        self.master = master
        #Set title of window
        self.master.title("Tic Tac Toe Against AI by Mounceph Morssaoui")
        #Set size of window
        self.master.geometry("656x737")
        #Create two white frames, center will hold the Sudoku, bottom will hold the buttons
        self.center = Frame(self.master, bg = 'grey60', padx=10,pady = 10)
        self.bottom = Frame(self.master, bg = 'grey60',padx=30,pady = 0)

        #Configure grid allocation, without the .grid(), the frames do not show up on window
        self.master.grid_rowconfigure(4,weight=1)
        self.master.grid_columnconfigure(3,weight=1)
        self.center.grid(row = 1)
        self.bottom.grid(row = 2)
        self.center.grid_columnconfigure(1,weight=1)
        self.center.grid_rowconfigure(0,weight=1)

        #Create user buttons which will go in the bottom frame
        self.bot_buttons = {"Vs Dumb AI":Button(self.bottom), "Vs Smart AI":Button(self.bottom)}

        #Configure user buttons and display them
        for i,y in zip(self.bot_buttons,range(0,len(self.bot_buttons))):
           self.bot_buttons[i].grid(row = 1, column = y, sticky = "n", padx = 53, pady = 14)
           self.bot_buttons[i].config(text = i, relief = "groove",height = 1, width = 14,font = ("Comic Sans MS", "16","bold"), bg = "white" )
           self.bot_buttons[i].config(command = lambda ai = i: self.restart(ai))
        

        #Declare list for Sudoku tiles
        self.square = []

        #Storing images for TTT game
        #X
        self.photoX = PhotoImage(file = "image/X.png")
        #O
        self.photoO = PhotoImage(file = "image/O.png")
        #empty image
        self.no_image = PhotoImage(file = "image/no_image.png")

        
        #Configure Sudoku tiles as buttons
        for row in range(0,3):
            for col in range(0,3):
                index = row*3 +col
                #Config
                self.square.append(Button(self.center, image =self.no_image, bg = 'black', relief = 'sunken', highlightbackground='black',highlightcolor= "black",borderwidth = 5, height = 200, width = 200, padx = 5, pady = 5))                
                #Set button command which increments the value the respective button holds
                #Notice the lambda: Using this allows for each button to affect itself and NOT the last button
                self.square[index].config(command = lambda row=row,col=col: self.play(row,col))
                self.square[index].grid(row = row, column = col)

        #Tic Tac Toe Variable
        self.board = initTTT()
        #User by default start
        self.player_start = True
        self.turn = "player"
        #AI is smart by default
        self.ai = "smart"
            
        

    #This function is to play TTT.
    #Lets the player play, then the AI plays immediately after
    #This function is called whenever the player chooses a move
    def play(self,row,col, two_players = "False"):
        #set the turn to user
        self.turn = "player"
        #convert 2D into 1D
        index = 3*row +col

        #Update placeholder board and update GUI
        self.updateGUI(index,self.turn)
        updateTTT(self.board,row,col,"X")


        #Check if game is done, return if true with a message box
        if self.game_over():
            return

        #change player turn to AI
        self.change()

        #AI turn to play, and plays according to AI difficulty
        if self.ai == "dumb":
           move = dumb_AI(self.board)
           #Makes sure there is still a vaild move available
           if move != None:
               #Update placeholder board and update GUI
               updateTTT(self.board,move[0],move[1],"O")  
               self.updateGUI(move[0]*3+move[1],self.turn)        
        else:
            move = smart_AI(self.board)
             #Update placeholder board and update GUI
            updateTTT(self.board,move[0],move[1],"O")  
            self.updateGUI(move[0]*3+move[1],self.turn)
            
         #Check if game is done, return if true with a message box
        if self.game_over():
            return
        

    #This function updates the GUI by changing the image on the button respective to
    #the player's/AI turn. Player will always be X, while AI will always be O
    def updateGUI(self,index,move):
        #Is square tile emtpy?
        #Note: that this check is technically useless because buttons are disable as soon
        #as they are pressed. But is keep, in case of future refactoring.
        if (self.square[index].cget('image') == str(self.no_image)):
            #Player's turn, disable tile and draw an X
            if move == "player":
                self.square[index].config(state = "disable", image = self.photoX)
            #AI's turn, disable tile and draw an O
            else:
                self.square[index].config(state = "disable", image = self.photoO)
            
    
    #This function returns whether the game is over of not
    def game_over(self):  
        
        #Disable board once a winner was found
        if hasWon(self.board):
            for button in self.square:
                button.config(state = "disable")
            
            #Depending on winner, display a message to the user
            if self.turn == "player":
                messagebox.showinfo(title = "You won!!!", message = "Good game and congrats!!! Play again!")
            else:
                messagebox.showinfo(title = "You lost :(", message = "It was a close one though, keep it up!!! Try again!")
            return True

        #Game board is full and there are no winners, Game is a Tie
        #Alert the user of the situation
        if is_full_TTT(self.board):   
            messagebox.showinfo(title = "Game Tie!!!", message = "It was a close one!!! Try again!")
            return True
        
        #Game is stil in a playable state
        return False  
    
    #This function restarts the TTT game with the desired AI difficulty
    #This function is called when the AI buttons are pressed
    def restart(self,ai):
        #Empty TTT board place holder
        self.board = initTTT()
        
        #Store the AI level
        if ai == "Vs Dumb AI":
            self.ai = "dumb"
        else:
            self.ai = "smart"

        #Restore GUI to empty board
        for button in self.square:
            button.config(state = "normal",image = self.no_image)
        
        #Alternate who starts the TTT game
        #By default, the player will always start the game
        self.player_start = change_turn(self.player_start)
        
        #Set whos turn to play it is
        if self.player_start:
            self.turn = "player"
        else:
            self.turn = "ai"

        #If the AI starts, have it play a move
        if self.turn != "player":
            if  self.ai == "dumb":
                move = dumb_AI(self.board)
                if move != None:
                    updateTTT(self.board,move[0],move[1],"O")  
                    self.updateGUI(move[0]*3+move[1],self.turn)        
            else:
                move = smart_AI(self.board)
                updateTTT(self.board,move[0],move[1],"O")  
                self.updateGUI(move[0]*3+move[1],self.turn) 
       
    #This function game player's turn
    def change(self):
        if self.turn == "player":
            self.turn = "ai"
        else:
            self.turn = "player"

################################################
# Main body section
################################################

#Code to create and start the Tic Tac Toe GUI
root = Tk()
TTTGui = TTTGui(root)
root.mainloop()

#end