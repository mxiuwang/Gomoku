# Gomoku
## Introduction
Gomoku game is also called Five in a Row. The origin is Japan and it is referred to as gomokunarabe. Traditionally, it is played on 15*15 or 19*19 board with Go pieces (black and white stones). Since the stones are typicall not moved nor removed, people also play it using paper and pencil.

Player alternatively makes moves by placing one of their color's stone on an empty intersection. The first player who form a connected five stones chains that can be horizontally, vertically or diagonally wins the game.
(https://en.wikipedia.org/wiki/Gomoku)
## Play the game
User runs this game by entering python3 gomoku.py in the terminal. User first enter the numbers of rows of the board that is in the range of [5, 100] and then enters the numer of columns of the board that is in the same range. In this game, the board can be a rectangle.

Player then choose the mode 1, 2 or 3 that they want to play. 1 is player vs player. 2 is player vs AI. 3 is AI vs AI.

If the player want to play against AI, they can chose to be player 1 ('X') or player 2 ('O'). Player 1, 'X', always goes first.

When it's the player's turn, they make move by entering 'row, col', such as '0 0' to represent the top left position.
## End the game
The game ends when one player form a connected five stones chains that can be horizontally, vertically or diagonally. The player can also quit the game by entering 'q' at any time of the game.
