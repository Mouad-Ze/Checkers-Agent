# Checkers AI Agent

An intelligent Checkers game featuring an AI opponent that uses the **Minimax algorithm with Alpha-Beta pruning** to provide challenging gameplay. The game includes a graphical user interface built with Tkinter and provides real-time performance metrics.

## 🎮 Features

### Core Gameplay
- **Classic Checkers Rules**: Full 8x8 checkers board with standard movement and capture rules
- **Interactive GUI**: User-friendly interface with click-based gameplay
- **Visual Feedback**: Move highlighting and piece selection indicators
- **Score Tracking**: Live scoreboard showing captured pieces

### AI Intelligence
- **Minimax Algorithm**: Advanced decision-making using game tree search
- **Alpha-Beta Pruning**: Optimized search with intelligent branch pruning
- **Configurable Depth**: Adjustable AI difficulty (search depth 3-7)
- **Smart Evaluation**: Position-based board evaluation for strategic gameplay

### Performance Analytics
- **Real-time Metrics**: Track AI performance during gameplay
- **Nodes Expanded**: Number of game states explored by the AI
- **Pruning Efficiency**: Percentage of branches pruned by alpha-beta algorithm
- **Time Analysis**: Time spent on each AI move
- **Move History**: Complete record of all moves made during the game

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/Mouad-Ze/Checkers-Agent.git
cd Checkers-Agent

# Install dependencies
pip install -r requirements.txt
```

### Running the Game
```bash
# Start the game
python main.py
```

## 🎯 How to Play

1. **Select Your Piece**: Click on a red piece to select it
2. **Make a Move**: Click on a highlighted yellow square to move
3. **Capture Opponents**: Jump over blue pieces to capture them
4. **Win the Game**: Capture all AI pieces or block all AI moves

## 🤖 AI Algorithm Details

### Minimax Algorithm
The AI uses the Minimax algorithm to evaluate all possible moves and choose the optimal one:
- **Search Tree**: Explores game states up to a specified depth
- **Evaluation Function**: Scores positions based on piece count, positioning, and strategic advantages
- **Optimal Play**: Assumes both players play optimally

### Alpha-Beta Pruning
Performance optimization through intelligent pruning:
- **Branch Elimination**: Removes branches that won't affect the final decision
- **Memory Efficiency**: Reduces computation time and memory usage
- **Performance Tracking**: Monitors pruning effectiveness in real-time

### Board Evaluation
The AI evaluates board positions using:
- **Piece Count**: Number of pieces for each player
- **Position Value**: Strategic positioning of pieces on the board
- **Capture Opportunities**: Potential to capture opponent pieces
- **Advancement**: Progress toward the opponent's side

## 📊 Performance Metrics

The game tracks various AI performance metrics:

| Metric | Description |
|--------|-------------|
| **Nodes Expanded** | Total game states explored during search |
| **Branches Pruned** | Number of branches eliminated by alpha-beta pruning |
| **Time per Move** | Average time for AI decision-making |
| **Pruning Efficiency** | Percentage of branches pruned |

## 🎛️ AI Configuration

### Adjusting Difficulty
You can modify the AI difficulty by changing the search depth:
- **Depth 3**: Easy (fast moves, basic strategy)
- **Depth 4**: Medium (balanced speed and intelligence)
- **Depth 5**: Hard (recommended for challenging gameplay)
- **Depth 6-7**: Expert (very strong AI, slower moves)

### Performance Settings
- **Alpha-Beta Pruning**: Enabled by default for optimal performance
- **Real-time Stats**: Performance metrics displayed during gameplay
- **Move History**: Complete game log for analysis

## 🏗️ Project Structure

```
Checkers-Agent/
├── main.py                    # Main entry point
├── examples/
│   ├── original_checker_code.py  # Original implementation
│   ├── basic_game.py             # Simple game example
│   └── ai_only_game.py           # AI vs AI demonstration
├── src/
│   ├── game/
│   │   └── board.py              # Game board logic
│   ├── ai/
│   │   └── minimax.py            # AI algorithm implementation
│   └── ui/                       # User interface components
├── tests/
│   └── test_board.py             # Unit tests
├── requirements.txt
└── README.md
```

## 🔧 Technical Implementation

### Core Components
- **GameBoard Class**: Manages game state, piece movement, and rule validation
- **MinimaxAI Class**: Implements the AI decision-making algorithm
- **UI Components**: Tkinter-based interface for user interaction
- **Performance Tracker**: Monitors and displays AI performance metrics

### Key Algorithms
- **Move Generation**: Efficiently generates all valid moves for any board state
- **Move Validation**: Ensures all moves follow checkers rules
- **Board Evaluation**: Strategic assessment of board positions
- **Search Optimization**: Alpha-beta pruning for improved performance

## 🎓 Educational Value

This project demonstrates several important AI and game development concepts:
- **Game Tree Search**: How AI explores possible future game states
- **Heuristic Evaluation**: Strategic assessment of game positions
- **Algorithm Optimization**: Alpha-beta pruning for improved performance
- **GUI Development**: Creating interactive user interfaces
- **Performance Analysis**: Measuring and optimizing algorithm efficiency

## 🚀 Future Enhancements

Potential improvements and extensions:
- [ ] Multiplayer support (human vs human)
- [ ] Different AI difficulty levels
- [ ] Tournament mode with multiple AI strategies
- [ ] Move history and game replay functionality
- [ ] Sound effects and animations
- [ ] Network play support
- [ ] Machine learning-based AI improvements

## 📝 Requirements

- Python 3.7+
- Tkinter (usually included with Python)
- No additional dependencies required for basic functionality

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation


## 🎯 Project Goals

This checkers AI agent was developed to demonstrate:
1. **AI Algorithm Implementation**: Practical application of Minimax and Alpha-Beta pruning
2. **Game Development**: Creating interactive games with intelligent opponents
3. **Performance Optimization**: Balancing AI intelligence with computational efficiency
4. **User Experience**: Providing engaging gameplay with educational value

---

**Enjoy playing against the AI and exploring how artificial intelligence makes strategic decisions in board games!** 🎮🤖
