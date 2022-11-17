from tkinter import *
import copy
from operator import itemgetter
from tkinter import font
import time

# The tic-tac-toe grid will have the following numbering convention
# 0 | 1 | 2
# ---------
# 3 | 4 | 5
# ---------
# 6 | 7 | 8

temp_button = ''

class TicTacToe:
    winningCombinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                            [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    buttons = []

    def __init__(self):
        self.board = [" "] * 9
        # List comprehension is needed so that each StringVar will not point to the same object
        self.moves = [StringVar() for _ in range(0, 9)]
        self.x_wins = 0
        self.o_wins = 0
        self.currPlayer = "O"
        self.moveNumber = 0
        self.winningSquares = []
        self.gameOver = False
        self.startTime = ''
        self.endTime = ''

        self.applyToEach(lambda x: x.set(" "), self.moves)
                
    # Call this to make a move
    def makeMove(self, move):
        if self.startTime == '':
            self.startTime = time.time()

        self.moveNumber += 1
        if self.currPlayer == "X":
            self.board[move] = "X"
            self.currPlayer = "O"
            self.ai_mm_init()
        else:
            self.board[move] = "O"
            self.currPlayer = "X"
                        

        # Check so that the win will not be counted twice for in AI mode
        if self.gameOver:
            return

        self.buttons[move].config(state="disabled")

        # Check for a win
        winner = self.checkWhichMarkWon(self.board)
        if winner is not None:
            self.whoWon(winner)
            self.gameOver = True
        # Check for a Cat's game
        elif self.moveNumber == 9 and self.boardFull(self.board):
            infoText.set("Cat's game!")
            self.applyToEach(lambda x: x.config(disabledforeground="red"), self.buttons)
            self.gameOver = True

        self.updateBoard()

    # Apply the given function to each element in the given list
    # Like map but does not return anything
    def applyToEach(self, func, some_list):
        for l in some_list:
            func(l)

    # Just like the function any, but returns the element instead of True
    def anyReturn(self, iterable):
        for e in iterable:
            if e:
                return e
        return False

    # Check who won the game, and change the GUI state accordingly
    def whoWon(self, winner):
        self.endTime = time.time()
        
        if winner == "X":
            infoText.set("You wins!!" + '\tEvaluation time: {}s'.format(round(self.endTime - self.startTime, 7)))
            self.x_wins += 1
        else:
            infoText.set("Bot wins!!" + '\tEvaluation time: {}s'.format(round(self.endTime - self.startTime, 7)))
            self.o_wins += 1
        
        restartButtonText.set("Play Another Round")
        countText.set("You: " + str(self.x_wins) + "\tBot: " + str(self.o_wins))

        self.applyToEach(lambda x: x.config(disabledforeground="red"),
                           [self.buttons[s] for s in self.winningSquares])

        for b in self.buttons:
            b.config(state="disabled")

    # Reset the game to its base state
    def reset(self):
        self.currPlayer = "O"
        self.moveNumber = 0
        self.gameOver = False

        infoText.set("Let\'s Go!")
        restartButtonText.set('Restart')
        self.board = [" " for _ in self.board]
        self.updateBoard()

        for b in self.buttons:
            b.config(state="normal")
            b.config(disabledforeground="black")
        
        buttons()
        

    # Update the GUI to reflect the moves in the board attribute
    def updateBoard(self):
        for i in range(0, 9):
            self.moves[i].set(self.board[i])

    # Check each of the winning combinations to check if anyone has won
    def checkWhichMarkWon(self, gameboard):
        # Check if any of the winning combinations have been used
        check = self.anyReturn([self.threeIn_a_Row(gameboard, c) for c in TicTacToe.winningCombinations])
        if check:
            return check
        else:
            return None

    # Check if the three given squares are owned by the same player
    def threeIn_a_Row(self, gameboard, squares):
        # Get the given squares from the board are check if they are all equal
        combo = set(itemgetter(squares[0], squares[1], squares[2])(gameboard))
        if len(combo) == 1 and combo.pop() != " ":
            self.winningSquares = squares
            return gameboard[squares[0]]
        else:
            return None

    # Get the opposite player
    def getEnemy(self, currPlayer):
        if currPlayer == "X":
            return "O"
        else:
            return "X"

    # Returns true if the board is full
    def boardFull(self, board):
        for s in board:
            if s == " ":
                return False

        return True

    # Call this to start the minimax algorithm
    def ai_mm_init(self):
        player = "O"
        a = -1000
        b = 1000

        boardCopy = copy.deepcopy(self.board)

        bestOutcome = -800

        best_move = None

        for i in range(0, 9):
            if boardCopy[i] == " ":
                boardCopy[i] = player
                val = self.minimax(self.getEnemy(player), boardCopy, a, b)
                boardCopy[i] = " "
                if player == "O":
                    if val > bestOutcome:
                        bestOutcome = val
                        best_move = i
                else:
                    if val < bestOutcome:
                        bestOutcome = val
                        best_move = i

        self.makeMove(best_move)

    # The minimax algorithm, with alpha-beta pruning
    def minimax(self, player, board, alpha, beta):
        boardCopy = copy.deepcopy(board)

        # Check for a win
        winner = self.checkWhichMarkWon(boardCopy)

        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif self.boardFull(boardCopy):
            return 0

        bestOutcome = -800 if player == "O" else 800

        for i in range(0, 9):
            if boardCopy[i] == " ":
                boardCopy[i] = player
                val = self.minimax(self.getEnemy(player), boardCopy, alpha, beta)
                boardCopy[i] = " "
                if player == "O":
                    bestOutcome = max(bestOutcome, val)
                    alpha = min(alpha, bestOutcome)
                else:
                    bestOutcome = min(bestOutcome, val)
                    beta = max(beta, bestOutcome)

                if beta <= alpha:
                    return bestOutcome

        return bestOutcome

# GUI Buttons
def buttons():
    for square in range(0, 9):
        temp_button = Button(root, 
                            textvariable=game.moves[square], 
                            font=font.Font(size=36, weight="bold"),
                            fg="black",
                            width=3,
                            height=2,
                            highlightbackground="lightblue",
                            command=lambda s=square: game.makeMove(s))
        # Divide by 3 to get row number, modulus by 3 to get column number
        temp_button.grid(row=int((square / 3)) + 3, column=int((square % 3)), sticky=NSEW)
        game.buttons.append(temp_button)
        if(square == 0):
            temp_button.invoke()
        
# -------------------------------------
#             Game GUI Setup
# -------------------------------------

if __name__ == "__main__":
    root = Tk()
    root.title("Tic-Tac-Toe Game")
    root.geometry('400x670')
    root.configure(padx=10, pady=10)
    game = TicTacToe()
    
    # Welcome Label
    welcome_text = StringVar()
    welcome_text.set("Welcome to Tic-Tac-Toe Game!")
    welcome = Label(root, textvariable=welcome_text, font=("Arial", 18))
    welcome.grid(row=0, column=0, columnspan=3, pady=20, ipadx=20)

    # Label used to display the current scores
    countText = StringVar()
    countText.set("You: " + str(game.x_wins) + "\tBot: " + str(game.o_wins))
    count = Label(root, textvariable=countText, font=("Arial"))
    count.grid(row=1, column=0, columnspan=3)

    # Label used to give the user information
    infoText = StringVar()
    infoText.set("Let\'s Go!")
    info = Label(root, textvariable=infoText)
    info.grid(row=2, column=0, columnspan=3)

    # Create buttons
    buttons()

    # Button for resetting the game
    restartButtonText = StringVar()
    restartButtonText.set("Restart")
    restart_button = Button(root, textvariable=restartButtonText, command=game.reset, bg="blue", fg='white', width=21, font=("Arial", 15))
    restart_button.grid(row=6, column=0, columnspan=3, pady=20)

    # Set the size of the rows and columns
    root.columnconfigure(0, minsize=100)
    root.columnconfigure(1, minsize=100)
    root.columnconfigure(2, minsize=100)
    root.rowconfigure(3, minsize=100)
    root.rowconfigure(4, minsize=100)
    root.rowconfigure(5, minsize=100)

    # Start the GUI loop
    root.mainloop()