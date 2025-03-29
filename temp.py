import tkinter as tk
from tkinter import messagebox


class ReversiGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Reversi Game")
        self.board = []
        self.current_player = "red"  # red starts the game
        self.game_over = False

        # Create the labels for displaying the piece counts
        self.red_count_label = tk.Label(self.master, text="Red: 2")
        self.red_count_label.grid(row=0, column=0)
        self.blue_count_label = tk.Label(self.master, text="Blue: 2")
        self.blue_count_label.grid(row=0, column=1)

        self.create_board()
        self.setup_initial_pieces()

    def create_board(self):
        """Creates the game board GUI."""
        for row in range(8):
            row_list = []
            for col in range(8):
                button = tk.Button(
                    self.master,
                    width=6,
                    height=3,
                    command=lambda r=row, c=col: self.on_click(r, c),
                )
                button.grid(row=row + 1, column=col)
                button.piece = None  # Set the initial piece to None
                row_list.append(button)
            self.board.append(row_list)

    def setup_initial_pieces(self):
        """Sets up the initial pieces in the center."""
        self.board[3][3].config(bg="blue")
        self.board[3][3].piece = "blue"
        self.board[3][4].config(bg="red")
        self.board[3][4].piece = "red"
        self.board[4][3].config(bg="red")
        self.board[4][3].piece = "red"
        self.board[4][4].config(bg="blue")
        self.board[4][4].piece = "blue"

        self.update_counts()

    def on_click(self, row, col):
        """Handles the logic when a button (board square) is clicked."""
        if self.game_over:
            return  # If the game is over, do nothing

        button = self.board[row][col]
        if button.piece is not None:  # If the square is already occupied
            return

        if not self.is_valid_move(
            row, col, self.current_player
        ):  # If the move is not valid
            return

        # Place the piece
        button.piece = self.current_player
        button.config(bg=self.current_player)

        # Flip the opponent's pieces
        self.flip_pieces(row, col, self.current_player)

        # Update the counts
        self.update_counts()

        # Switch players
        self.switch_player()

        # Check if the game is over
        self.check_game_over()

    def is_valid_move(self, row, col, player):
        """Checks if the move made by the player is valid."""
        if self.board[row][col].piece is not None:
            return False

        opponent = "blue" if player == "red" else "red"

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (1, 1),
            (-1, 1),
            (1, -1),
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            flip_found = False
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c].piece == opponent:
                    flip_found = True
                elif self.board[r][c].piece == player:
                    if flip_found:
                        return True
                    else:
                        break
                else:
                    break
                r += dr
                c += dc
        return False

    def flip_pieces(self, row, col, player):
        """Flips the opponent's pieces after a valid move."""
        opponent = "blue" if player == "red" else "red"
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (1, 1),
            (-1, 1),
            (1, -1),
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            flip_pieces = []
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c].piece == opponent:
                    flip_pieces.append((r, c))
                elif self.board[r][c].piece == player:
                    for fr, fc in flip_pieces:
                        self.board[fr][fc].piece = player
                        self.board[fr][fc].config(bg=player)
                    break
                else:
                    break
                r += dr
                c += dc

    def switch_player(self):
        """Switches the turn to the other player."""
        self.current_player = "blue" if self.current_player == "red" else "red"

    def update_counts(self):
        """Updates the count of red and blue pieces on the board."""
        red_count = 0
        blue_count = 0
        for row in self.board:
            for button in row:
                if button.piece == "red":
                    red_count += 1
                elif button.piece == "blue":
                    blue_count += 1
        self.red_count_label.config(text=f"Red: {red_count}")
        self.blue_count_label.config(text=f"Blue: {blue_count}")

    def check_game_over(self):
        """Checks if the game is over and announces the winner."""
        red_count = 0
        blue_count = 0
        for row in self.board:
            for button in row:
                if button.piece == "red":
                    red_count += 1
                elif button.piece == "blue":
                    blue_count += 1

        # Check if any player has no valid moves
        if red_count + blue_count == 64 or red_count == 0 or blue_count == 0:
            self.game_over = True
            if red_count > blue_count:
                winner = "Red wins!"
            elif blue_count > red_count:
                winner = "Blue wins!"
            else:
                winner = "It's a draw!"
            messagebox.showinfo("Game Over", winner)


# Main loop to run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = ReversiGame(root)
    root.mainloop()
