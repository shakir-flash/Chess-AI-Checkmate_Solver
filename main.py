from enum import Enum
import load
import search
from state import ChessState, Node, Heuristic

def start_problem(initial_state: ChessState, solution, search_type):
    #creating the initial node
    initial_node = Node(True, initial_state, 0)
    
    #dict to call the search function based on user input
    search_methods = {
        'Minimax': lambda node: search.minimax(node),
        'ABP': lambda node: search.alpha_beta_pruning(node, -1, 1),
        'Negamax': lambda node: search.Negamax.negamax(node, 5, -1, 1, 1, Heuristic.NONE),
        'Negascout': lambda node: search.NegaScout.negascout(node, 5, -1, 1, 1, Heuristic.NONE),
        'History': lambda node: search.history_heuristic(node, -1, 1, Heuristic.CHECK)
    }
    
    #checking if the selected search algorithm is valid and execute it
    if search_type in search_methods:
        result = search_methods[search_type](initial_node)
        terminal, expanded = result if len(result) == 2 else result[:2]
        model_solution = str(terminal)
    else:
        print("Invalid Search Algorithm")
        return None, None, None

    #checking if the solution is correct
    expected_solution = " -> " + ' -> '.join(['{}{}'.format(move.get('w', ''), f" -> {move['b']}" if 'b' in move else '') for move in solution])
    model_solution = str(terminal)
    model_moves = set(model_solution.split(" -> "))
    expected_moves = set(expected_solution.split(" -> "))
    solved_correctly = model_moves.issubset(expected_moves)
    return expanded, solved_correctly, expected_solution, model_solution

if __name__ == '__main__':
    puzzles = load.load_puzzle_file('checkmate_testcase/cm_in_2.txt')
    total_cases = len(puzzles)
    passed_cases = 0
    total_expanded_nodes = 0

    #prompting user to select a search method
    print("Select a search algorithm:")
    print("1: Minimax")
    print("2: Alpha-Beta Pruning")
    print("3. Negamax w A/B")
    print("4. NegaScout w A/B")
    print("5: History Heuristic")
    
    search_types = {
        1: 'Minimax',
        2: 'ABP',
        3: 'Negamax',
        4: 'Negascout',
        5: 'History'
    }
    
    choice = int(input("Enter your choice (1-5): "))
    
    #getting the selected search type by choice
    search_type = search_types.get(choice)
    if not search_type:
        print("Invalid choice. Exiting program.")
        exit()

    #running the selected algorithm
    for i, puzzle in enumerate(puzzles):
        state = ChessState(puzzle['player'], puzzle['position'], puzzle['mate'])
        expanded, solved_correctly, expected_solution, model_solution = start_problem(state, puzzle['solution'], search_type)
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