import re

def load_puzzle_file(file_path: str) -> list:
    collected_puzzles = []
    with open(file_path, "r") as puzzle_file:
        while True:
            puzzle_meta = puzzle_file.readline().strip()
            if not puzzle_meta:  # Stop if we read an empty line indicating the end of the file
                break
            puzzle_position = puzzle_file.readline().strip()
            puzzle_solution = puzzle_file.readline().strip()
            collected_puzzles.append(format_puzzle(puzzle_meta, puzzle_position, puzzle_solution))
            puzzle_file.readline()  # Skip one empty line
            puzzle_file.readline()  # Skip another empty line
    return collected_puzzles

def format_puzzle(meta_data: str, chess_position: str, moves_data: str):
    #input line parsing
    parsed_meta = meta_data.split(',')
    puzzle_meta = {'players': parsed_meta[0], 'location': parsed_meta[1], 'date': parsed_meta[2]}
    #use position line
    puzzle_position = chess_position
    #splitting solution moves by numbered items
    move_entries = filter(None, re.split(r'(\d+\.)', moves_data))
    move_sequence = []
    move_index = 1
    starting_player = True  #assuming first player is white unless first move indicates black
    #iterate over the moves and separate by player
    for entry_num, entry_moves in zip(move_entries, move_entries):
        parsed_moves = entry_moves.strip().split()
        if len(parsed_moves) == 1:
            if move_index == 1:  #first move handling
                starting_player = False
                move_sequence.append({'b': parsed_moves[0]})
            else:
                move_sequence.append({'w': parsed_moves[0]})
        else:
            move_sequence.append({'w': parsed_moves[0], 'b': parsed_moves[1]})
        move_index += 1
    #constructing the final dictionary
    return {
        'meta': puzzle_meta,
        'player': starting_player,
        'position': puzzle_position,
        'mate': len(move_sequence),
        'solution': move_sequence
    }