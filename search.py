from state import Heuristic, Node  #Py file dependancy
import math
from copy import deepcopy #for recursive appending



def minimax(node: Node) -> (Node, int):
    # teminal heck
    if node.state.terminal_test():  
        return node, 0
    total_expanded = 1
    #initialize the best value to negative or positive infinity
    best_val = -math.inf if node.is_max_node else math.inf
    best_node = None
    #get possible successor states from the current node
    successors = node.state.find_successors()
    while not successors.empty():
        _, (action, state) = successors.get()
        #create a child node
        child_node = Node(not node.is_max_node, state, node.depth + 1, node, action)
        #recursive minmax fn
        terminal, expanded = minimax(child_node)
        total_expanded += expanded
        # update based on utility
        if (node.is_max_node and terminal.state.utility() > best_val) or \
           (not node.is_max_node and terminal.state.utility() < best_val):
            best_val = terminal.state.utility()
            best_node = terminal
    return best_node, total_expanded



def alpha_beta_pruning(node: Node, alpha, beta):
    #terminal checl
    if node.state.terminal_test():
        return node, 0
    total_expanded = 1
    # initiial def
    best_val = -math.inf if node.is_max_node else math.inf
    best_node = None
    #get successors of the current node
    successors = node.state.find_successors()
    while not successors.empty():
        _, (action, state) = successors.get()
        child_node = Node(not node.is_max_node, state, node.depth + 1, node, action)
        # recursive application of fn
        terminal, expanded = alpha_beta_pruning(child_node, alpha, beta)
        total_expanded += expanded
        # update fn
        if (node.is_max_node and terminal.state.utility() > best_val) or \
           (not node.is_max_node and terminal.state.utility() < best_val):
            best_val = terminal.state.utility()
            best_node = terminal
            if node.is_max_node:
                alpha = max(alpha, best_val)
            else:
                beta = min(beta, best_val)
            if beta <= alpha:
                break
    return best_node, total_expanded


class Negamax:
    def negamax(node, depth, alpha, beta, color, heuristic):
        #base case check
        if depth == 0 or node.state.terminal_test():
            return node, color * node.state.utility(), 0
        total_expanded = 1
        best_value = -float('inf')
        best_node = None
        #get all successor states
        successors = node.state.find_successors(heuristic)
        while not successors.empty():
            (priority, (action, state)) = successors.get()
            #recursively do with negated values
            child_node = Node(not node.is_max_node, state, node.depth + 1, node, action)
            #recursive negamax call
            child_result, child_value, expanded = Negamax.negamax(child_node, depth - 1, -beta, -alpha, -color, heuristic)
            #updating total expansions
            total_expanded += expanded
            child_value = -child_value
            #update best values
            if child_value > best_value:
                best_value = child_value
                best_node = child_result
            #update alpha
            alpha = max(alpha, child_value)
            #alpha-beta cutoff
            if alpha >= beta:
                break
        return best_node, best_value, total_expanded



class NegaScout:
    def negascout(node, depth, alpha, beta, color, heuristic):
        #checking base conditions
        if depth == 0 or node.state.terminal_test():
            return node, node.state.utility() * color, 0
        total_expanded = 1
        first_child = True
        best_value = -float('inf')
        best_node = None

        #looping over successors
        successors = node.state.find_successors(heuristic)
        while not successors.empty():
            (priority, (action, state)) = successors.get()
            child_node = Node(not node.is_max_node, state, node.depth + 1, node, action)
            #first child special case
            if first_child:
                first_child = False
                child_result, value, expanded = NegaScout.negascout(child_node, depth - 1, -beta, -alpha, -color, heuristic)
            else:
                #subsequent children adjustment
                child_result, value, expanded = NegaScout.negascout(child_node, depth - 1, -alpha-1, -alpha, -color, heuristic)
                #checking if re-search needed
                if alpha < value < beta:
                    child_result, value, expanded = NegaScout.negascout(child_node, depth - 1, -beta, -value, -color, heuristic)
            total_expanded += expanded
            value = -value
            #updating best result
            if value > best_value:
                best_value = value
                best_node = child_result
            #updating alpha
            alpha = max(alpha, value)
            #early exit check
            if alpha >= beta:
                break
        return best_node, best_value, total_expanded

 
transposition_table: dict[str, Node] = {}

def history_heuristic(node: Node, alpha, beta, heuristic: Heuristic):
    #checking transposition table
    if node.state.position in transposition_table:
        best_node = deepcopy(transposition_table[node.state.position])
        pointer = best_node
        #adjusting parent pointers
        while node.state != pointer.state:
            pointer = pointer.parent
        pointer.parent = node.parent 
        #return cached node
        return best_node, 0
    #terminal check
    if node.state.terminal_test():
        return node, 0
    total_expanded = 1
    best_val = -math.inf if node.is_max_node else math.inf
    best_node = None
    #find successors
    successors = node.state.find_successors(heuristic)
    while not successors.empty():
        #prrocess each successor
        (priority, (action, state)) = successors.get()
        child_node = Node(not node.is_max_node, state, node.depth + 1, node, action)
        #recursive call
        terminal, expanded = history_heuristic(child_node, alpha, beta, heuristic)
        #updating expansion count
        total_expanded += expanded
        #updating best node and value
        if (node.is_max_node and terminal.state.utility() > best_val) or \
           (not node.is_max_node and terminal.state.utility() < best_val):
            best_val = terminal.state.utility()
            best_node = terminal
            #adjusting alpha or beta
            if node.is_max_node:
                alpha = max(alpha, best_val)
            else:
                beta = min(beta, best_val)       
        elif terminal.state.utility() == best_val:
            depth_comparison = terminal.depth < best_node.depth if node.is_max_node else terminal.depth > best_node.depth
            if depth_comparison:
                best_node = terminal       
        #prune condition
        if beta <= alpha:
            break
    #store best node in table
    transposition_table[node.state.position] = best_node
    return best_node, total_expanded