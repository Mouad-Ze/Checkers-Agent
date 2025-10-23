#!/usr/bin/env python3
"""
Checkers AI Game - Main Entry Point

This is the main entry point for the Checkers AI Game. It provides both the original
functionality and an organized interface for the game.
"""

# Import the original checker code for backward compatibility
import sys
import os

# Add the examples directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'examples'))

from original_checker_code import PlayingTheGame
import tkinter as tk


def main():
    """Main function to start the Checkers AI Game."""
    print("Checkers AI Game")
    print("================")
    print("Instructions:")
    print("- Click on your red pieces to select them")
    print("- Click on a valid move destination (highlighted in yellow)")
    print("- The AI (blue pieces) will automatically make its move")
    print("- Try to capture all AI pieces to win!")
    print()
    
    # Create the main window
    root = tk.Tk()
    root.title("Checkers Game Agent")
    
    # Start the game
    game = PlayingTheGame(root)
    
    # Run the game loop
    root.mainloop()


if __name__ == "__main__":
    main()
