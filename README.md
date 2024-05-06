
# Chess Checkmate Solver

Welcome to the Chess Puzzle Solver project! This application uses advanced search algorithms to solve chess puzzles efficiently. Dive into the world of game theory and AI as you explore implementations of various search algorithms.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation

To set up this project locally, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/shakir-flash/Chess-AI-Checkmate_Solver.git
   ```
2. Navigate to the project directory:
   ```bash
   cd //path
   ```

## Usage

To run the Chess Puzzle Solver, execute the following from the command line:
```bash
python main.py
```
This command initializes the game environment and starts the puzzle solving process using the chosen search algorithm.
Interaction with `main.py` happens through CLI.

You are prompted a UI with list of search algorithms. Please select a number and hit enter.

## Features

- **State Management**: Handles the representation and manipulation of the chessboard states (`state.py`).
- **Data Loading**: Manages loading and initializing game configurations or states (`load.py`).
- **Search Algorithms**: Implements various AI algorithms for decision making (`search.py`):
  - **Minimax Algorithm**: Explore game possibilities to determine the best move.
  - **Alpha-Beta Pruning**: Reduce the number of nodes evaluated in the search tree by 'pruning' unwanted outcomes.
  - **Negamax with Alpha-Beta Pruning**: Negamax with A/B merges maximizing and minimizing functions into a single process, reducing computational load while ensuring optimal outcomes.
  - **Negascout with Alpha-Beta Pruning**: Negascout employs variation search and zero-window searches, differing from Negamax and minimax.
  - **History Heuristic Search**: History heuristic enhances AI by favoring successful past moves, boosting strategic capabilities in algorithms like alpha-beta pruning.
- **Main Application**: Orchestrates the overall program flow and integrates various components (`main.py`).
