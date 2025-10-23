# Importing the tkinter library for creating the graphical user interface (GUI)
import tkinter as tk

# Importing the deepcopy function from the copy module to create deep copies of the game board
from copy import deepcopy

# Importing the math module for mathematical functions and constants (e.g., math.inf)
import math

# Importing the time module to measure elapsed time for performance tracking
import time

class GameBoard:
    def __init__(self):
        # Initialize the game board with an 8x8 matrix, set player turn, and piece counts
        self.Matrix = [["---" for _ in range(8)] for _ in range(8)]
        self.PlayerTurn = True  # True for player's turn, False for AI's turn
        self.ComputerPieces = 12  # Number of AI pieces
        self.PlayerPieces = 12  # Number of player pieces
        self.SelectedPiece = None  # Currently selected piece by the player
        self.PlayerPoints = 0  # Points scored by the player
        self.ComputerPoints = 0  # Points scored by the AI
        self.position_computer()  # Position AI pieces on the board
        self.position_player()  # Position player pieces on the board

    def position_computer(self):
        # Place AI pieces ("C") on the top 3 rows of the board
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:  # Only place pieces on dark squares
                    self.Matrix[i][j] = "C"

    def position_player(self):
        # Place player pieces ("B") on the bottom 3 rows of the board
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:  # Only place pieces on dark squares
                    self.Matrix[i][j] = "B"

    def is_valid_move(self, old_x, old_y, new_x, new_y):
        # Check if a move from (old_x, old_y) to (new_x, new_y) is valid
        if 0 <= new_x < 8 and 0 <= new_y < 8:  # Ensure the new position is within the board
            dx, dy = new_x - old_x, new_y - old_y
            # Prevent player pieces from moving backward
            if self.Matrix[old_x][old_y] == 'B' and dx >= 0:
                return False
            # Prevent AI pieces from moving backward
            if self.Matrix[old_x][old_y] == 'C' and dx <= 0:
                return False
            # Check for normal moves (1 square diagonally)
            if abs(dx) == 1 and abs(dy) == 1 and self.Matrix[new_x][new_y] == "---":
                return True
            # Check for capture moves (2 squares diagonally)
            if abs(dx) == 2 and abs(dy) == 2:
                mid_x, mid_y = (old_x + new_x) // 2, (old_y + new_y) // 2
                if self.Matrix[new_x][new_y] == "---" and self.Matrix[mid_x][mid_y] in ("C" if self.Matrix[old_x][old_y] == "B" else "B"):
                    return True
        return False

    def move_piece(self, old_x, old_y, new_x, new_y):
        # Move a piece from (old_x, old_y) to (new_x, new_y) if the move is valid
        if self.is_valid_move(old_x, old_y, new_x, new_y):
            dx, dy = new_x - old_x, new_y - old_y
            capture = abs(dx) == 2 and abs(dy) == 2  # Check if the move is a capture
            self.Matrix[new_x][new_y] = self.Matrix[old_x][old_y]
            self.Matrix[old_x][old_y] = "---"
            if capture:
                # Remove the captured piece and update scores
                mid_x, mid_y = (old_x + new_x) // 2, (old_y + new_y) // 2
                self.Matrix[mid_x][mid_y] = "---"
                if self.PlayerTurn:
                    self.ComputerPieces -= 1
                    self.PlayerPoints += 1
                else:
                    self.PlayerPieces -= 1
                    self.ComputerPoints += 1
                print(f"Move executed from ({old_y}, {old_x}) to ({new_y}, {new_x})")
            print(f"Points Won by Player: {self.PlayerPoints}")
            print(f"Points Won by Computer: {self.ComputerPoints}")
            self.PlayerTurn = not self.PlayerTurn  # Switch turns
            self.check_game_over()  # Check if the game is over
            return True
        return False

    def get_valid_moves(self, maximizing_player):
        # Get all valid moves for the current player (AI or player)
        jump_moves = []  # Capture moves
        normal_moves = []  # Normal moves
        player_piece = "C" if maximizing_player else "B"  # Determine which player's moves to calculate
        for i in range(8):
            for j in range(8):
                if self.Matrix[i][j] == player_piece:
                    # Check all possible moves (normal and capture)
                    for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        new_x, new_y = i + dx, j + dy
                        if abs(dx) == 2 and abs(dy) == 2:  # Capture move
                            mid_x, mid_y = (i + new_x) // 2, (j + new_y) // 2
                            if self.is_valid_move(i, j, new_x, new_y):
                                new_board = deepcopy(self)
                                new_board.move_piece(i, j, new_x, new_y)
                                jump_moves.append((new_board, (i, j, new_x, new_y)))
                        elif abs(dx) == 1 and abs(dy) == 1:  # Normal move
                            if self.is_valid_move(i, j, new_x, new_y):
                                new_board = deepcopy(self)
                                new_board.move_piece(i, j, new_x, new_y)
                                normal_moves.append((new_board, (i, j, new_x, new_y)))
        return jump_moves + normal_moves  # Return all valid moves

    def check_game_over(self):
        # Check if the game is over (one player has no pieces left)
        if self.PlayerPieces == 0:
            print("Game Over! The AI wins.")
            exit()
        elif self.ComputerPieces == 0:
            print("Game Over! You win.")
            exit()

    def evaluate_board(self):
        # Evaluate the board state for the AI (higher score is better for the AI)
        player_score = sum((7 - x if y % 2 == 0 else x) for x in range(8) for y in range(8) if self.Matrix[x][y] == 'B')
        computer_score = sum((x if y % 2 == 0 else 7 - x) for x in range(8) for y in range(8) if self.Matrix[x][y] == 'C')
        return computer_score - player_score  # Return the difference in scores

class SearchToolBox:
    @staticmethod
    def minimax(board_obj, depth, alpha, beta, maximizing_player, stats):
        # Minimax algorithm with alpha-beta pruning
        if depth == 0 or board_obj.ComputerPieces == 0 or board_obj.PlayerPieces == 0:
            return None, board_obj.evaluate_board()  # Base case: return the board evaluation
        
        best_move = None
        valid_moves = board_obj.get_valid_moves(maximizing_player)
        stats['nodes_expanded'] += len(valid_moves)  # Track the number of nodes expanded
        
        if maximizing_player:
            # Maximizing player (AI)
            max_eval = -math.inf
            for move in valid_moves:
                _, eval = SearchToolBox.minimax(move[0], depth - 1, alpha, beta, False, stats)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move[1]
                alpha = max(alpha, eval)
                if beta <= alpha:  # Alpha-beta pruning
                    stats['prunes'] += 1
                    break
            return best_move, max_eval
        else:
            # Minimizing player (human)
            min_eval = math.inf
            for move in valid_moves:
                _, eval = SearchToolBox.minimax(move[0], depth - 1, alpha, beta, True, stats)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move[1]
                beta = min(beta, eval)
                if beta <= alpha:  # Alpha-beta pruning
                    stats['prunes'] += 1
                    break
            return best_move, min_eval

class PlayingTheGame:
    def __init__(self, root):
        # Initialize the game UI and board
        self.Board = GameBoard()
        self.setup_ui(root)
        self.play_tour = []  # Track the sequence of moves
        self.stats = {'nodes_expanded': 0, 'prunes': 0, 'time_spent': 0, 'pruning_gains': 0}  # Track AI performance

    def setup_ui(self, root):
        # Set up the game UI (canvas, scoreboard, buttons, etc.)
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)  # Bind mouse clicks to handle_click method
        self.scoreboard = tk.Label(root, text="Player: 0  AI: 0", font=("Arial", 16))
        self.scoreboard.pack()
        self.status_message = tk.Label(root, text="Your Turn", font=("Arial", 16))
        self.status_message.pack()
        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack()
        self.draw_board()  # Draw the initial board

    def draw_board(self):
        # Draw the game board and pieces on the canvas
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                color = "#D2B48C" if (i + j) % 2 == 0 else "#8B4513"  # Alternate square colors
                self.canvas.create_rectangle(j*50, i*50, (j+1)*50, (i+1)*50, fill=color, outline="black")
                piece = self.Board.Matrix[i][j]
                if piece != "---":
                    piece_color = "red" if piece == "B" else "blue"  # Player pieces are red, AI pieces are blue
                    self.canvas.create_oval(j*50+10, i*50+10, (j+1)*50-10, (i+1)*50-10, fill=piece_color, outline="black")
                    if piece in ("BK", "CK"):  # Kings have a "K" label
                        self.canvas.create_text(j*50+25, i*50+25, text="K", font=("Arial", 20), fill="gold")

    def handle_click(self, event):
        # Handle player clicks on the board
        column, row = event.x // 50, event.y // 50  # Convert pixel coordinates to board coordinates
        print(f"Click registered at: ({row}, {column})")
        if self.Board.SelectedPiece is None:
            # If no piece is selected, select the clicked piece (if it's the player's piece)
            if self.Board.Matrix[row][column] == "B":
                self.Board.SelectedPiece = (row, column)
                self.highlight_valid_moves(row, column)  # Highlight valid moves for the selected piece
        else:
            # If a piece is already selected, attempt to move it to the clicked position
            old_row, old_column = self.Board.SelectedPiece
            print(f"Attempting move from ({old_row}, {old_column}) to ({row}, {column})")
            self.play_tour.append((old_row, old_column, row, column))  # Record the move
            print("Play Tour:", self.play_tour)
            self.Board.move_piece(old_row, old_column, row, column)  # Execute the move
            self.Board.SelectedPiece = None
            self.draw_board()  # Redraw the board
            self.update_scoreboard()  # Update the scoreboard
            if not self.Board.PlayerTurn:
                # If it's the AI's turn, let the AI make a move
                self.status_message.config(text="AI's Turn")
                self.computer_move()
            else:
                self.status_message.config(text="Your Turn")

    def highlight_valid_moves(self, row, column):
        # Highlight valid moves for the selected piece
        for i in range(8):
            for j in range(8):
                if self.Board.is_valid_move(row, column, i, j):
                    self.canvas.create_rectangle(j*50, i*50, (j+1)*50, (i+1)*50, outline="yellow", width=3)

    def computer_move(self):
        # Let the AI make a move using the minimax algorithm
        start_time = time.time()
        best_move, _ = SearchToolBox.minimax(self.Board, 5, -math.inf, math.inf, True, self.stats)
        end_time = time.time()
        self.stats['time_spent'] = end_time - start_time  # Track the time taken for the AI's move
        if best_move:
            old_x, old_y, new_x, new_y = best_move
            self.Board.move_piece(old_x, old_y, new_x, new_y)  # Execute the AI's move
            self.draw_board()  # Redraw the board
            self.update_scoreboard()  # Update the scoreboard
            print(f"AI's Move: from ({old_x}, {old_y}) to ({new_x}, {new_y})")
            print("Current AI Performance Metrics:", self.stats)
            self.status_message.config(text="Your Turn")  # Switch back to the player's turn

    def update_scoreboard(self):
        # Update the scoreboard with the current scores
        self.scoreboard.config(text=f"Player: {self.Board.PlayerPoints}  AI: {self.Board.ComputerPoints}")

    def restart_game(self):
        # Restart the game by resetting the board and stats
        self.Board = GameBoard()
        self.play_tour = []
        self.stats = {'nodes_expanded': 0, 'prunes': 0, 'time_spent': 0, 'pruning_gains': 0}
        self.draw_board()
        self.update_scoreboard()
        self.status_message.config(text="Your Turn")

if __name__ == "__main__":
    # Start the game by creating the main window and running the game loop
    root = tk.Tk()
    root.title("Checkers Game Agent")
    game = PlayingTheGame(root)
    root.mainloop()