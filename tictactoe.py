import sys
if sys.version_info.major < 3 or sys.version_info.minor < 12:
    raise RuntimeError("This script should be run by Python 3.12 or higher.")

import pyxel

class TicTacToe:
    def __init__(self):
        # Initialize Pyxel window (160x160) and enable mouse
        pyxel.init(160, 160, title="Tic Tac Toe")
        pyxel.mouse(True)

        # 3x3 board: each cell is None, "X", or "O"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.turn = "X"  # X always starts
        self.game_over = False

        # Run the Pyxel application with update and draw functions.
        pyxel.run(self.update, self.draw)

    def update(self):
        # On left mouse click, determine which cell is clicked
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y

            # Define board drawing parameters:
            # The board is drawn in a 150x150 area starting at offset (5,5) 
            cell_size = 50
            offset = 5

            # Check if click is within the board area.
            if offset <= mx < offset + cell_size * 3 and offset <= my < offset + cell_size * 3:
                col = (mx - offset) // cell_size
                row = (my - offset) // cell_size

                # Place mark if cell is empty and game is not over.
                if self.board[row][col] is None and not self.game_over:
                    self.board[row][col] = self.turn

                    # Check if current move wins the game.
                    if self.check_win(self.turn):
                        self.game_over = True
                    # If board is full, also end game.
                    elif all(cell is not None for row in self.board for cell in row):
                        self.game_over = True
                    else:
                        # Switch turn.
                        self.turn = "O" if self.turn == "X" else "X"

        # Restart game if 'R' key is pressed.
        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()

    def check_win(self, player):
        # Check rows and columns.
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
            if all(self.board[j][i] == player for j in range(3)):
                return True

        # Check the two diagonals.
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            return True
        if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
            return True

        return False

    def reset_game(self):
        # Reset board, turn, and game over flag.
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.turn = "X"
        self.game_over = False

    def draw(self):
        pyxel.cls(0)  # Clear screen with black.

        cell_size = 50
        offset = 5

        # Draw the grid lines.
        for i in range(4):
            x = offset + i * cell_size
            pyxel.line(x, offset, x, offset + cell_size * 3, 7)
        for j in range(4):
            y = offset + j * cell_size
            pyxel.line(offset, y, offset + cell_size * 3, y, 7)

        # Draw the marks on the board.
        for row in range(3):
            for col in range(3):
                mark = self.board[row][col]
                if mark:
                    # Calculate the center of the cell.
                    center_x = offset + col * cell_size + cell_size // 2
                    center_y = offset + row * cell_size + cell_size // 2
                    if mark == "X":
                        size = cell_size // 2 - 5
                        pyxel.line(center_x - size, center_y - size,
                                   center_x + size, center_y + size, 8)
                        pyxel.line(center_x - size, center_y + size,
                                   center_x + size, center_y - size, 8)
                    else:  # mark == "O"
                        radius = cell_size // 2 - 5
                        pyxel.circ(center_x, center_y, radius, 10)

        # If game over, display a message.
        if self.game_over:
            pyxel.text(20, 160 - 10, "Game Over! Press R to restart.", 7)

# Start the game.
TicTacToe()
