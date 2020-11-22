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
        self.winner = 'T' # can be X, O or T 

    def get_board(self):
        return self.__board

    def print_board(self):
        for row in range(self.__rows):
            for col in range(self.__cols):
                print(self.__board[row][col], end=' ')
            print()

    def get_color(self, row, col):
        return self.__board[row][col]

    def setColorAtPosition(self, row, col, color):
        self.__board[row][col] = color

    def positionIsValid(self, row, col):
        valid = False 
        if self.__board[row][col] == ".":
          valid = True 
          return valid              
        return valid    

    def getWinner(self):
        return self.winner 

    def isGameOver(self):
        
        # check if there's 5 in a row 
        for row in range(self.__rows):
            for col in range(self.__cols-4):
                if self.__board[row][col] == self.__board[row][col+1] == self.__board[row][col+2] == self.__board[row][col+3] == self.__board[row][col+4] != '.':
                    self.winner = self.__board[row][col]
                    return True 

        # check if there's 5 in a column 
        for col in range(self.__cols):
            for row in range(self.__rows-4):
                if self.__board[row][col] == self.__board[row+1][col] == self.__board[row+2][col] == self.__board[row+3][col] == self.__board[row+4][col] != '.':
                    self.winner = self.__board[row][col]
                    return True 

        # check if there's 5 in diagonal 
        for row in range(self.__rows-4):
            for col in range(self.__cols-4):
                if self.__board[row][col] == self.__board[row+1][col+1] == self.__board[row+2][col+2] == self.__board[row+3][col+3] == self.__board[row+4][col+4] != '.':
                    self.winner = self.__board[row][col]
                    return True 
                    
        for row in range(self.__rows-4):
            for col in range(4, self.__cols):
                if self.__board[row][col] == self.__board[row+1][col-1] == self.__board[row+2][col-2] == self.__board[row+3][col-3] == self.__board[row+4][col-4] != '.':
                    self.winner = self.__board[row][col]
                    return True

        # check if board is full 
        fullBoard = True 
        for row in range(self.__rows):
            for col in range(self.__cols):
                if self.__board[row][col] == '.':
                    fullBoard = False 
        if fullBoard == True:
            self.winner = 'T'
            return True 

        return False

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
            row, col = absearchthing(board)
        return row, col

    def askMove(self, board):
        print()
        move = input("Enter move: ")

        row, col = move.split(" ")

        print()
        return int(row), int(col)

def get_input():
    valid = False
    while not valid:
        print("Enter size of board")
        rows = int(input("Enter number of rows (5-100): "))
        cols = int(input("Enter number of cols (5-100): "))
        if rows >= 5 and rows <= 100 and cols >= 5 and cols <= 100:
            valid = True
            board = Board(rows, cols)
        else:
            print("Invalid input, try again")
        print()

    valid = False
    while not valid:
        option = input("Enter game mode 1,2,3(1 = player vs player, 2 = player vs ai, 3 = ai vs ai): ")
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
            if player == "1":
                valid = True
            elif player == "2":
                valid = True
                current = player1
                player1 = player2
                player2 = current
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
        while not self.board.isGameOver():
            self.board.print_board()
            print("{0} to make move".format(current))
            current_player.makeMove(self.board)
            #winner = self.board.winner()
            if current_player == self.player1:
                current_player = self.player2
                current = "Player 2"
            else:
                current_player = self.player1
                current = "Player 1"

        winner = self.board.getWinner() # X, O, or T       
        return winner

def main():
    board, player1, player2 = get_input()

    game = Game(board, player1, player2)
    winner = game.play()
    print("The Winner is", winner)

main()