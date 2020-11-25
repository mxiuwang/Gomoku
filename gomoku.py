import copy

# source: https://www.youtube.com/watch?v=trKjYdBASyQ&vl=en&ab_channel=TheCodingTrain
SCORES = {
    'X':1,
    'O':-1,
    'T':0
}

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

    def get_color(self, row, col):
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
        for col in range(self.__cols):
            for row in range(self.__rows-4):
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
    board_copy = copy.deepcopy(board) # copy board 
    rows, cols = board_copy.getBoardSize()
    bestScore = -999
    bestMove = [0,0]

    # temp variables 
    depth = 0 # depth of search tree 
    isMaximizing = False # True for max, False for min 

    for row in range(0, rows):
        for col in range(0, cols):
            if board_copy.getBoard()[row][col] == '.':
                score = minimax(board_copy, depth, isMaximizing, color)
                if score > bestScore:
                    bestMove = [row, col]

    return bestMove 

def minimax(board, depth, isMaximizing, color):
    rows, cols = board.getBoardSize()

    bestScore = 0
    gameOver = board.isGameOver()
    if gameOver == True:
        winner = board.getWinner()
        bestScore = SCORES[winner]
        return bestScore 

    if isMaximizing:
        bestScore = -999
        for row in range(0, rows):
            for col in range(0, cols):
                if board.getBoard()[row][col] == '.':
                    board.setColorAtPosition(row, col, color)
                    if color == 'X':
                        color = 'O'
                    elif color == 'O':
                        color = 'X'    
                    score = minimax(board, depth+1, False, color)
                    if score > bestScore:
                        bestScore = score 
        # print("Maximizing", bestScore)
        return bestScore

    else: # isMaximizing is False 
        bestScore = 999
        for row in range(0, rows):
            for col in range(0, cols):
                if board.getBoard()[row][col] == '.':
                    board.setColorAtPosition(row, col, color)
                    if color == 'X':
                        color = 'O'
                    elif color == 'O':
                        color = 'X'    
                    score = minimax(board, depth+1, True, color)
                    if score < bestScore:
                        bestScore = score 
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
        move = input("\nEnter move [row col]: ")
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

        while board.positionIsValid(row, col) == False:
            print("Invalid move")
            move = input("\nEnter move [row col]: ")
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
        return int(row), int(col)

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
            if rows >= 5 and rows <= 100 and cols >= 5 and cols <= 100:
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
        current = "Player 1"
        current_player = self.player1
        self.board.printBoard()
        while not self.board.isGameOver():
            print("{0} to make move".format(current))
            current_player.makeMove(self.board)
            #winner = self.board.winner()
            if current_player == self.player1:
                current_player = self.player2
                current = "Player 2"
            else:
                current_player = self.player1
                current = "Player 1"
            self.board.printBoard()

        winner = self.board.getWinner() # X, O, or T
        return winner

if __name__ == "__main__":
    board, player1, player2 = get_input()

    game = Game(board, player1, player2)
    winner = game.play()
    print("The Winner is", winner)
