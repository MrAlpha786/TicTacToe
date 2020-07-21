#!/usr/bin/env python3

from time import sleep
from random import choice

# Colors and other constants
R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
B = '\033[1;34m'
C = '\033[1;36m'
N = '\033[0m'
U = '\033[9A'
D = '\033[7B'
UU = '\033[3A'


class TicTacToe:
    """Tic-Tac-Toe"""

    def __init__(self, twoplayers=False):
        """Initialize board and players."""

        # Initialize board and the symbols.
        self.board = [' ' for i in range(9)]
        self.symbols = self.x, self.o = R+'X', B+'O'

        # Randomly choose a symbol to play.
        self.player = choice(self.symbols)

        # Assign second player.
        self.opponentmove = (self.playermove
                             if twoplayers else self.aimove)

        # Initialize move with None as no move is played.
        self.move = None

    def start(self):
        """This start the main game loop."""

        # Game loops until all cells are filled.
        while True:

            # Print Board.
            self.printboard()

            # Check if someone is winning.
            if self.validate():
                print(f"{G}player{self.player}{G} wins.{N}",
                      ' '*10)
                # Current player has won break loop.
                return

            # If no moves left break.
            if ' ' not in self.board:
                print(f"{G}Its a tie.{N}", ' '*20)
                return

            # Swap symbol of the player.
            self.swapplayer()

            # Player chooses cell to be filled.
            print(f"{N}Player{self.player}{N}\'s turn")
            if self.player == self.x:
                self.playermove()
            else:
                self.opponentmove()

            # Reset Cursor
            print(U)

    def help(self):
        """Print Instructions"""

        print(f"\n\n{C}TIC-TAC-TOE")
        print(f"{C}", '='*50, "\n", sep='')
        print(f"{R}How-to-Play:{N}\n")
        print("Enter position to play move: \n")
        print(f"{Y}1{G} | {Y}2{G} | {Y}3")
        print(f"{G}--+---+--")
        print(f"{Y}4{G} | {Y}5{G} | {Y}6")
        print(f"{G}--+---+--")
        print(f"{Y}7{G} | {Y}8{G} | {Y}9{N}\n")
        print(f"{C}", '='*50, "\n", sep='')

    def validate(self):
        """Validate lines one by one."""

        b = self.board  # Assign board to b for readability.

        for i in range(0, 7, 3):
            # Check rows.
            if b[i] == b[i+1] == b[i+2] != ' ':
                return True

            # Check columns.
            j = i // 3
            if b[j] == b[j+3] == b[j+6] != ' ':
                return True

        # Check diagonal.
        if b[0] == b[4] == b[8] != ' ':
            return True

        # Check anti-diagonal.
        if b[2] == b[4] == b[6] != ' ':
            return True

        # If line is not valid return False.
        return False

    def playmove(self):
        """Fill Player's symbol in cell."""

        self.board[self.move] = self.player + G

    def getmoves(self):
        """Return index of empty cells."""

        return [i for i in range(9)
                if self.board[i] == ' ']

    def swapplayer(self):
        """Change player symbol."""

        if self.player == self.x:
            self.player = self.o
        else:
            self.player = self.x

    def printboard(self):
        """Print Board."""

        b = self.board  # Assign board to b for readability.

        print(f"{G}{b[0]} | {b[1]} | {b[2]}")
        print("--+---+--")
        print(f"{b[3]} | {b[4]} | {b[5]}")
        print("--+---+--")
        print(f"{b[6]} | {b[7]} | {b[8]}{N}\n")

    def playermove(self):
        """Registers Player's Move"""

        # Loop until correct move
        while True:
            print(' '*40, end="\r")

            try:
                self.move = int(input(
                        "Enter Position: ")) - 1

                # Raise error if move is not in board or
                # already filled.
                if (self.move not in range(9) or
                        self.board[self.move] != ' '):
                    raise ValueError

                self.playmove()
                return

            except ValueError:
                print(f"{R}Enter a valid position.{N}",
                      end="\r")

                sleep(1.5)
                print(' '*40, UU)  # Return Cursor
                continue

    def aimove(self):
        """Register AI's Move"""

        print("AI is moving...       ")
        sleep(0.5)

        if self.board.count(' ') == 9:
            # AI always choose first cell on very first move.
            # This is just for some optimization as
            # minimax is called 549946 times recursively
            # on very first move.
            self.move = 0
        else:
            # Below line calls minimax function which
            # returns two values, we only need move.
            _, self.move = self.minimax()
        self.playmove()

    def minimax(self, depth=0):
        """Recursively finds the best playable move."""

        # This function plays the game for both player
        # and AI and assign a score to each game. Then
        # return the best move based on that score.

        # AI will try to minimize the best score
        if self.player == self.o:
            best = -10
        else:
            best = 10

        # Base cases
        # Return best score if anyone is winning.
        # Best Score is 10 - depth of the recursion.
        if self.validate():
            if self.player == self.x:
                # Return best score for non-AI player.
                return 10 - depth, None
            else:
                # Return best score for AI player.
                return -10 + depth, None

        # Return 0 if game ends with tie.
        if ' ' not in self.board:
            return 0, None

        # Get a list of available moves and play those moves.
        moves = self.getmoves()
        for move in moves:
            self.move = move
            self.playmove()
            # Swap players before the recursive call.
            self.swapplayer()
            # Calls itself with depth increased by 1.
            val, _ = self.minimax(depth+1)
            # Swap back to current player.
            self.swapplayer()
            # Undo the played move.
            self.board[move] = ' '

            if self.player == self.x:
                # For non-AI player new best score is the
                # val return by above recursive call and
                # best move is the move played above, if
                # val is less than the current best score.
                if val < best:
                    best, bestmove = val, move
            else:
                # For AI new best score is the val return
                # by above recursive call and best move is
                # the move played above, if val is greater
                # than the current best score.
                if val > best:
                    best, bestmove = val, move

        # Return best score and move.
        return best, bestmove


if __name__ == '__main__':
    # Create TicTacToe object as game.
    game = TicTacToe()
    # Call help() to print instructions.
    game.help()
    # Start game.
    game.start()
