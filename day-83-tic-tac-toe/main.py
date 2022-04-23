from tictactoegame import TicTacToeGame
from tictactoeplayer import TicTacToePlayer

ROW_MAPPING = {
    "1": 0,
    "2": 1,
    "3": 2
}
COL_MAPPING = {
    "a": 0,
    "b": 1,
    "c": 2
}


def check_if_play_valid(play, row=True):
    if row:
        # possible values for row
        if play not in ["1", "2", "3"]:
            return False
    else:
        # possible values for column
        if play not in ["a", "b", "c"]:
            return False
    return True


def get_user_move(player, letter):
    player_row = input(f"Player {player} [you have {letter}s]: Pick a row [1, 2, or 3]: ")
    while not check_if_play_valid(player_row):
        print("Invalid row! Try again.")
        player_row = input(f"Player {player} [you have {letter}s]: Pick a row [1, 2, or 3]: ")
    player_col = input(f"Player {player} [you have {letter}s]: Pick a column [a, b, or c]: ").lower()
    while not check_if_play_valid(player_col, row=False):
        print("Invalid column! Try again.")
        player_col = input(f"Player {player} [you have {letter}s]: Pick a column [a, b, or c]: ").lower()

    row_index = ROW_MAPPING[player_row]
    col_index = COL_MAPPING[player_col]

    return row_index, col_index


def play_turn(game, player):
    if player == 1:
        letter = "O"
    else:
        letter = "X"

    row_index, col_index = get_user_move(player, letter)
    while game.check_if_taken(row_index, col_index):
        print("That spot is already taken! Try again.")
        row_index, col_index = get_user_move(player, letter)
    game.update_board(row_index, col_index, letter)


def computer_turn(computer_player, game):
    row_move, col_move = computer_player.play_turn(game.board)
    game.update_board(row_move, col_move, 'X')
    print("Computer move: ")


def play_game(one_player):
    game = TicTacToeGame()
    if one_player:
        computer_player = TicTacToePlayer()
    game.display_board()
    print("\nPlayer 1: You are Os.")
    print("Player 2 (or computer): You are Xs.")
    game_over = False
    player_turn = 0
    # keep track of whose turn it is, Player 1 or Player 2
    while not game_over:
        player_turn = player_turn % 2 + 1
        if one_player and player_turn == 2:
            computer_turn(computer_player, game)
        else:
            play_turn(game, player_turn)
        game.display_board()

        # winner
        if game.check_if_winner():
            print(f"Player {player_turn} wins! Congratulations!")
            game_over = True
        # draw
        elif game.check_if_board_full():
            print("It's a draw!")
            game_over = True


print("Welcome to Tic Tac Toe!")
need_computer_player = input("How many players? [1 or 2]: ") == "1"
if need_computer_player:
    print("You will be Player 1. The computer will be Player 2.")
keep_playing = True

while keep_playing:
    play_game(need_computer_player)
    play_again = input("Play again? [Y/n]: ")
    if play_again.lower() == "n":
        keep_playing = False
