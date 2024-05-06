from enum import Enum
#Other py files in this repository
import load
import search
from state import ChessState, Node, Heuristic

def start_problem(initial_state, solution, search_type):
    initial_node = Node(True, initial_state, 0)
    terminal, expanded = None, 0
    if search_type == 1:  # Minimax
        terminal, expanded = search.minimax(initial_node)
    elif search_type == 2:  # Alpha-Beta Pruning
        terminal, expanded = search.alpha_beta_pruning(initial_node, -1, 1)
    elif search_type == 3:  # Negamax
        terminal, best_value, expanded = search.Negamax.negamax(initial_node, 5, -1, 1, 1, Heuristic.NONE)
    elif search_type == 4:  # Negascout
        terminal, best_value, expanded = search.NegaScout.negascout(initial_node, 5, -1, 1, 1, Heuristic.NONE)
    elif search_type == 5:  # History Heuristic
        terminal, expanded = search.history_heuristic(initial_node, -1, 1, Heuristic.CHECK)
    else:
        print("Invalid Search Algorithm")
        return None, None, None

    model_solution = str(terminal)
    expected_solution = " -> " + ' -> '.join(['{}{}'.format(move.get('w', ''), f" -> {move['b']}" if 'b' in move else '') for move in solution])
    model_moves = set(model_solution.split(" -> "))
    expected_moves = set(expected_solution.split(" -> "))
    solved_correctly = model_moves.issubset(expected_moves)
    return expanded, solved_correctly, expected_solution, model_solution

if __name__ == '__main__':
    puzzles = load.load_puzzle_file('checkmate_testcase/cm_in_2.txt')
    total_cases = len(puzzles)
    passed_cases = 0
    total_expanded_nodes = 0

    print("Select a search algorithm:")
    print("1: Minimax")
    print("2: Alpha-Beta Pruning")
    print("3: Negamax w/ A/B")
    print("4: Negascout w/ A/B")
    print("5: History Heuristic")
    
    choice = int(input("Enter your choice (1-5): "))
    
    if 1 <= choice <= 5:
        for i, puzzle in enumerate(puzzles):
            state = ChessState(puzzle['player'], puzzle['position'], puzzle['mate'])
            expanded, solved_correctly, expected_solution, model_solution = start_problem(state, puzzle['solution'], choice)
            if solved_correctly:
                passed_cases += 1
            total_expanded_nodes += expanded if expanded is not None else 0
            print(f"Test Case {i + 1}")
            print(f"Number of Nodes Expanded: {expanded}")
            print(f"Solved Correctly: {'Yes' if solved_correctly else 'No'}")
            print(f"Expected Solution: {expected_solution}")
            print(f"Model's Solution Path: {model_solution}")
            print("---------------------------------")

        print(f"Total Test Cases: {total_cases}")
        print(f"Passed: {passed_cases} \t Failed: {total_cases - passed_cases}")
        print(f"Success Rate: {passed_cases / total_cases * 100:.2f}%")
        print(f"Total Nodes Expanded Across All Test Cases: {total_expanded_nodes}")
    else:
        print("Invalid choice. Exiting program.")