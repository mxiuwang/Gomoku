import copy
import time

# source: https://www.youtube.com/watch?v=trKjYdBASyQ&vl=en&ab_channel=TheCodingTrain

class Board:

    def __init__(self, rows, cols):
        self.__rows = rows
        self.__cols = cols
        self.__board = []
        for row in range(rows):
            row = []
            for col in range(cols):
                row.append(".")
            self.__board.append(row)
        self.__winner = 'T' # can be X, O or T

    def getBoard(self):
        return self.__board

    def printBoard(self):
        if self.__rows > 10:
            print(end='   ')
        else:
            print(end='  ')

        for i in range(self.__cols):
            print(i, end=' ')

        for row in range(self.__rows):
            if self.__rows > 10:
                print('\n%-2d' % row, end=' ')
            else:
                print('\n%d' % row, end=' ')
            for col in range(self.__cols):
                if col < 10:
                    print(self.__board[row][col], end=' ')
                else:
                    print(self.__board[row][col], end='  ')

        print('\n')

    def getColor(self, row, col):
        return self.__board[row][col]

    def setColorAtPosition(self, row, col, color):
        self.__board[row][col] = color

    def positionIsValid(self, row, col):
        if row<0 or row>=self.__rows or col<0 or col>=self.__cols:
            return False
        return self.__board[row][col] == "."

    def getWinner(self):
        return self.__winner

    def isGameOver(self):

        # check if there's 5 in a row
        for row in range(self.__rows):
            for col in range(self.__cols-4):
                if self.__board[row][col] == self.__board[row][col+1] == self.__board[row][col+2] == self.__board[row][col+3] == self.__board[row][col+4] != '.':
                    self.__winner = self.__board[row][col]
                    return True

        # check if there's 5 in a column
        for row in range(self.__rows-4):
            for col in range(self.__cols):
                if self.__board[row][col] == self.__board[row+1][col] == self.__board[row+2][col] == self.__board[row+3][col] == self.__board[row+4][col] != '.':
                    self.__winner = self.__board[row][col]
                    return True

        # check if there's 5 in diagonal
        # From left top to right bottom
        for row in range(self.__rows-4):
            for col in range(self.__cols-4):
                if self.__board[row][col] == self.__board[row+1][col+1] == self.__board[row+2][col+2] == self.__board[row+3][col+3] == self.__board[row+4][col+4] != '.':
                    self.__winner = self.__board[row][col]
                    return True

        # From right top to left bottom
        for row in range(self.__rows-4):
            for col in range(4, self.__cols):
                if self.__board[row][col] == self.__board[row+1][col-1] == self.__board[row+2][col-2] == self.__board[row+3][col-3] == self.__board[row+4][col-4] != '.':
                    self.__winner = self.__board[row][col]
                    return True

        # check if board is full
        fullBoard = True
        for row in range(self.__rows):
            for col in range(self.__cols):
                if self.__board[row][col] == '.':
                    fullBoard = False
        if fullBoard == True:
            self.__winner = 'T'
            return True

        return False   

    def getBoardSize(self):
        return (self.__rows, self.__cols)

def absearch(board, color):
    rows, cols = board.getBoardSize()
    bestScore = -999
    bestMove = [0,0]

    if color == "X":
        next_color = "O"
    else:
        next_color = "X"

    # temp variables 
    isMaximizing = False # True for max, False for min 

    for row in range(rows):
        for col in range(cols):
            if board.getColor(row, col) == '.':
                board.setColorAtPosition(row, col, color)
                score = minimax(board, isMaximizing, next_color, 0)
                board.setColorAtPosition(row, col, ".")
                if score > bestScore:
                    bestScore = score
                    bestMove = [row, col]
                    if bestScore >= 0:
                        return bestMove

    return bestMove 

def minimax(board, isMaximizing, color, depth):
    rows, cols = board.getBoardSize()

    if depth >= 4:
        return 0

    bestScore = 0
    if board.isGameOver():
        winner = board.getWinner()
        if winner == color:
            bestScore = 1
        elif winner == "T":
            bestScore = 0
        else:
            bestScore = -1
        return bestScore

    if color == "X":
        next_color = "O"
    else:
        next_color = "X"

    if isMaximizing:
        bestScore = -999
        for row in range(rows):
            for col in range(cols):
                if board.getColor(row, col) == '.':
                    board.setColorAtPosition(row, col, color)
                    score = minimax(board, False, next_color, depth+1)
                    board.setColorAtPosition(row, col, ".")
                    if score > bestScore:
                        bestScore = score
                        if bestScore >= 0:
                            return bestScore
        # print("Maximizing", bestScore)
        return bestScore
    else: # isMaximizing is False 
        bestScore = 999
        for row in range(rows):
            for col in range(cols):
                if board.getColor(row, col) == '.':
                    board.setColorAtPosition(row, col, color) 
                    score = minimax(board, True, next_color, depth+1)
                    board.setColorAtPosition(row, col, ".")
                    if score < bestScore:
                        bestScore = score
                        if bestScore == -1:
                            return bestScore
        # print("Minimizing", bestScore)
        return bestScore

    return bestScore

class Player:

    def __init__(self, color, is_human):
        self.color = color
        self.is_human = is_human

    def makeMove(self, board):
        row, col = self.decideMove(board)
        board.setColorAtPosition(row, col, self.color)

    def decideMove(self, board):
        if self.is_human:
            row, col = self.askMove(board)
        else:
            row, col = absearch(board, self.color)
        return row, col

    def askMove(self, board):
        move = input("Enter move 'row# col#': ")
        if move == 'q':
            print("Thank you for playing")
            exit()

        try:
            row, col = move.split(" ")
            row = int(row)
            col = int(col)
        except:
            row = 101
            col = 101

        while not board.positionIsValid(row, col):
            print("Invalid move")
            move = input("Enter move 'row# col#': ")
            if move == 'q':
                print("Thank you for playing")
                exit()
            try:
                row, col = move.split(" ")
                row = int(row)
                col = int(col)
            except:
                row = 101
                col = 101

        print()
        return row, col

    def getColor(self):
        return self.color

def get_input():
    print("Welcome to Gomoku (Enter 'q' to quit at anytime)")
    valid = False
    while not valid:
        print("Enter size of board")
        try:
            rows = input("Enter number of rows (5-100): ")
            if rows == 'q':
                print("Thank you for playing")
                exit()
            rows = int(rows)

            cols = input("Enter number of cols (5-100): ")
            if cols == 'q':
                print("Thank you for playing")
                exit()
            cols = int(cols)
        except Exception:
            print("Invalid input, try again")
        else:
            if rows >= 5 and rows <= 20 and cols >= 5 and cols <= 20:
                valid = True
                board = Board(rows, cols)
            else:
                print("Invalid size, try again")
        print()

    valid = False
    while not valid:
        option = input("Enter game mode 1,2,3 (1 = player vs player, 2 = player vs ai, 3 = ai vs ai): ")
        if option == 'q':
            print("Thank you for playing")
            exit()
        if option in ["1", "2", "3"]:
            valid = True
            player1 = Player("X", option != "3")
            player2 = Player("O", option == "1")
        else:
            print("Invalid input, try again")
        print()

    if option == "2":
        valid = False
        while not valid:
            player = input("Would you like to be player '1' or '2': ")
            if player == 'q':
                print("Thank you for playing")
                exit()

            if player == "1":
                valid = True
            elif player == "2":
                valid = True
                player1 = Player("X", False)
                player2 = Player("O", True)
            else:
                print("Invalid input, try again")
            print()

    return board, player1, player2

class Game:

    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2

    def play(self):
        current = self.player1
        self.board.printBoard()
        while not self.board.isGameOver():
            print("{0} to make move\n".format(current.getColor()))
            current.makeMove(self.board)
            if current == self.player1:
                current = self.player2
            else:
                current = self.player1
            self.board.printBoard()

        winner = self.board.getWinner() # X, O, or T
        return winner

if __name__ == "__main__":
    board, player1, player2 = get_input()

    game = Game(board, player1, player2)
    winner = game.play()
    print("The Winner is", winner)

    input("Enter to escape")
