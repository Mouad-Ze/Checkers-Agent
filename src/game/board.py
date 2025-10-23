"""
Checkers Game Board Implementation

This module contains the core game board logic, piece management, and move validation
for the Checkers game.
"""

from copy import deepcopy
from typing import List, Tuple, Optional


class GameBoard:
    """
    Represents the checkers game board and manages game state.
    
    The board is an 8x8 grid where pieces can only occupy dark squares.
    Player pieces ('B') start at the bottom, AI pieces ('C') start at the top.
    """
    
    def __init__(self):
        """Initialize the game board with starting positions."""
        self.Matrix = [["---" for _ in range(8)] for _ in range(8)]
        self.PlayerTurn = True  # True for player's turn, False for AI's turn
        self.ComputerPieces = 12  # Number of AI pieces
        self.PlayerPieces = 12  # Number of player pieces
        self.SelectedPiece = None  # Currently selected piece by the player
        self.PlayerPoints = 0  # Points scored by the player
        self.ComputerPoints = 0  # Points scored by the AI
        self.position_computer()  # Position AI pieces on the board
        self.position_player()  # Position player pieces on the board

    def position_computer(self) -> None:
        """Place AI pieces ('C') on the top 3 rows of the board."""
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:  # Only place pieces on dark squares
                    self.Matrix[i][j] = "C"

    def position_player(self) -> None:
        """Place player pieces ('B') on the bottom 3 rows of the board."""
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:  # Only place pieces on dark squares
                    self.Matrix[i][j] = "B"

    def is_valid_move(self, old_x: int, old_y: int, new_x: int, new_y: int) -> bool:
        """
        Check if a move from (old_x, old_y) to (new_x, new_y) is valid.
        
        Args:
            old_x: Current row position
            old_y: Current column position
            new_x: Target row position
            new_y: Target column position
            
        Returns:
            True if the move is valid, False otherwise
        """
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
                if (self.Matrix[new_x][new_y] == "---" and 
                    self.Matrix[mid_x][mid_y] in ("C" if self.Matrix[old_x][old_y] == "B" else "B")):
                    return True
        
        return False

    def move_piece(self, old_x: int, old_y: int, new_x: int, new_y: int) -> bool:
        """
        Move a piece from (old_x, old_y) to (new_x, new_y) if the move is valid.
        
        Args:
            old_x: Current row position
            old_y: Current column position
            new_x: Target row position
            new_y: Target column position
            
        Returns:
            True if the move was successful, False otherwise
        """
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

    def get_valid_moves(self, maximizing_player: bool) -> List[Tuple['GameBoard', Tuple[int, int, int, int]]]:
        """
        Get all valid moves for the current player (AI or player).
        
        Args:
            maximizing_player: True for AI player, False for human player
            
        Returns:
            List of tuples containing (new_board_state, move_coordinates)
        """
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

    def check_game_over(self) -> bool:
        """
        Check if the game is over (one player has no pieces left).
        
        Returns:
            True if the game is over, False otherwise
        """
        if self.PlayerPieces == 0:
            print("Game Over! The AI wins.")
            return True
        elif self.ComputerPieces == 0:
            print("Game Over! You win.")
            return True
        return False

    def evaluate_board(self) -> int:
        """
        Evaluate the board state for the AI (higher score is better for the AI).
        
        Returns:
            Integer score representing board advantage
        """
        player_score = sum((7 - x if y % 2 == 0 else x) for x in range(8) for y in range(8) 
                          if self.Matrix[x][y] == 'B')
        computer_score = sum((x if y % 2 == 0 else 7 - x) for x in range(8) for y in range(8) 
                           if self.Matrix[x][y] == 'C')
        return computer_score - player_score  # Return the difference in scores

    def get_board_state(self) -> List[List[str]]:
        """
        Get a copy of the current board state.
        
        Returns:
            Copy of the board matrix
        """
        return [row[:] for row in self.Matrix]

    def set_board_state(self, state: List[List[str]]) -> None:
        """
        Set the board state from a given matrix.
        
        Args:
            state: Board state matrix to set
        """
        self.Matrix = [row[:] for row in state]

    def count_pieces(self) -> Tuple[int, int]:
        """
        Count the number of pieces for each player.
        
        Returns:
            Tuple of (player_pieces, computer_pieces)
        """
        player_count = sum(1 for row in self.Matrix for cell in row if cell == 'B')
        computer_count = sum(1 for row in self.Matrix for cell in row if cell == 'C')
        return player_count, computer_count

    def __str__(self) -> str:
        """String representation of the board for debugging."""
        result = "  0  1  2  3  4  5  6  7\n"
        for i, row in enumerate(self.Matrix):
            result += f"{i} "
            for cell in row:
                result += f"{cell} "
            result += "\n"
        return result

    def __copy__(self) -> 'GameBoard':
        """Create a shallow copy of the board."""
        new_board = GameBoard()
        new_board.Matrix = [row[:] for row in self.Matrix]
        new_board.PlayerTurn = self.PlayerTurn
        new_board.ComputerPieces = self.ComputerPieces
        new_board.PlayerPieces = self.PlayerPieces
        new_board.SelectedPiece = self.SelectedPiece
        new_board.PlayerPoints = self.PlayerPoints
        new_board.ComputerPoints = self.ComputerPoints
        return new_board

    def __deepcopy__(self, memo) -> 'GameBoard':
        """Create a deep copy of the board."""
        new_board = GameBoard()
        new_board.Matrix = [row[:] for row in self.Matrix]
        new_board.PlayerTurn = self.PlayerTurn
        new_board.ComputerPieces = self.ComputerPieces
        new_board.PlayerPieces = self.PlayerPieces
        new_board.SelectedPiece = self.SelectedPiece
        new_board.PlayerPoints = self.PlayerPoints
        new_board.ComputerPoints = self.ComputerPoints
        return new_board
