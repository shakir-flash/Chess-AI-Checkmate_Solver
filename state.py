import queue
from enum import Enum
from random import choice
import chess, random


class Heuristic(Enum):
    NONE = 0
    CHECK = 1

class Node:
    def __init__(self, is_max_node: bool, state: 'ChessState', depth: int, parent: 'Node' = None, action: str = None):
        #initialising values
        self.is_max_node = is_max_node
        self.state = state
        self.depth = depth
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.total_score = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_actions())

    def __str__(self):
        #returns path to variable
        if self.parent is None:
            return ""
        return str(self.parent) + " -> " + str(self.action)


class ChessState:

    def __init__(self, player: bool, position: str, mate: int):
        #initialising values
        self.position = position
        self.player = player
        self.mate = mate
        self.board = chess.Board(position)

    def terminal_test(self) -> bool:
        #terminal check
        return self.board.is_game_over() or self.mate == 0

    def utility(self) -> int:
        #return utility value
        outcome = self.board.outcome()
        if outcome and outcome.winner is not None:  # If white won
            return 1 if outcome.winner == self.player else -1
        else:
            return 0
        
    def get_unexplored_action(self):
        #get unexplored action
        legal_moves = list(self.board.legal_moves)
        if legal_moves:
            action = random.choice(legal_moves)
            return action
        else:
            return None
    
    def get_next_state(self, move):
        #get next game state after making move
        if not self.board.is_pseudo_legal(move):
            raise ValueError(f"Attempted to make a non-pseudo-legal move: {move} on board {self.board.fen()}")
        
        self.board.push(move)  # Make the move
        new_position = self.board.fen()
        new_mate = self.mate if self.board.turn else self.mate - 1
        return ChessState(self.player, new_position, new_mate)

    def get_legal_actions(self):
        return list(self.board.legal_moves) #get legal actions

    def __str__(self) -> str:
        return self.position

    def __eq__(self, __value) -> bool:
        return self.position == __value.position

    def find_successors(self, heuristic: Heuristic = Heuristic.NONE) -> queue.PriorityQueue:
        successors = queue.PriorityQueue()  # It is just a simple list if heuristic=0
        for move in self.board.legal_moves:  # chess library helps with all legal moves
            action = self.board.san(move)  # Get string representation of the move
            self.board.push(move)  # Make a temporary move to get the new position
            new_position = self.board.fen()  # Get the FEN of the new position
            new_mate = self.mate if self.board.turn else self.mate - 1  # decrement mate only if Black moves
            state = ChessState(self.player, new_position, new_mate)  # Create the successor State
            successors.put((self.heurist(heuristic), (action, state)))  # Add to the PriorityQueue
            self.board.pop()  # Undo the temporary move

        return successors 

    def heurist(self, heuristic: Heuristic) -> int:
        if heuristic == Heuristic.NONE:  # No Heuristic
            return 0
        elif heuristic == Heuristic.CHECK:  # History Heuristic: Check move first
            if self.board.is_check():
                return 0
            else:
                return 1 