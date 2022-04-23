
import random


def convert_to_2d_array_idx(idx):
    row = int(idx / 3)
    col = int(idx % 3)
    return row, col

class TicTacToePlayer:
    def __init__(self):
        # all 8 options for winning the game
        self.options = {
            (0, 1, 2): 0,
            (3, 4, 5): 0,
            (6, 7, 8): 0,
            (0, 3, 6): 0,
            (1, 4, 7): 0,
            (2, 5, 8): 0,
            (0, 4, 8): 0,
            (2, 4, 6): 0
        }

    # Find best move based on available options
    def play_turn(self, board):
        # Represent board as 1d array instead of 2d
        flat_board = []
        for row in board:
            for cell in row:
                flat_board.append(cell)
        # Update available options
        opts = self.options
        for opt_key, opt_val in opts.items():
            opt_selection = [flat_board[idx] for idx in opt_key]
            # Play defense (block Os) if needed
            if opt_selection.count('O') == 2 and opt_selection.count(' ') == 1:
                for idx in opt_key:
                    if flat_board[idx] == " ":
                        return convert_to_2d_array_idx(idx)
            # opponent has taken at least one of the spots in the option
            if 'O' in opt_selection:
                opts[opt_key] = -1
            else:
                opts[opt_key] = opt_selection.count('X')

        # Choose the option(s) with the most Xs as the best option to add X to
        best_opt_keys = [key for (key, val) in opts.items() if val == max(opts.values())]
        # Then if there are multiple choices for the best option, randomly pick one
        best_opt_key = random.choice(best_opt_keys)
        avail_choices = [idx for idx in best_opt_key if flat_board[idx] == " "]
        # Pick random space from the best option
        choice_idx = random.choice(avail_choices)
        # Convert back to 2d array indices to return
        return convert_to_2d_array_idx(choice_idx)
