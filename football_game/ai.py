import random

def computer_move(game):
    moves = game.find_possible_moves()
    sorted_moves = sorted(moves, key=lambda x: x[1])
    best = sorted_moves[0][1]
    filtered_moves = [move for move in sorted_moves if move[1] == best]
    move = random.choice(filtered_moves)
    return move
