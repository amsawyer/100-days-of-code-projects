
class TicTacToeGame:
    def __init__(self):
        self.board = [[" ", " ", " "],
                       [" ", " ", " "],
                       [" ", " ", " "]]

    def display_board(self):
        row1 = self.board[0]
        row2 = self.board[1]
        row3 = self.board[2]
        print("    a   b   c \n")
        print(f"1   {row1[0]} | {row1[1]} | {row1[2]}")
        print("   -----------")
        print(f"2   {row2[0]} | {row2[1]} | {row2[2]}")
        print("   -----------")
        print(f"3   {row3[0]} | {row3[1]} | {row3[2]}")

    def check_if_taken(self, row_idx, col_idx):
        return self.board[row_idx][col_idx] != " "

    def update_board(self, row, col, letter):
        self.board[row][col] = letter

    def check_if_winner(self):
        brd = self.board
        # check for horizontal victory
        for row in brd:
            if row[0] != " " and row[0] == row[1] == row[2]:
                return True
        # check for vertical victory
        for i in range(len(brd[0])):
            if brd[0][i] != " " and brd[0][i] == brd[1][i] == brd[2][i]:
                return True
        # check for diagonal victory
        if brd[0][0] != " " and brd[0][0] == brd[1][1] == brd[2][2]:
            return True
        if brd[0][2] != " " and brd[0][2] == brd[1][1] == brd[2][0]:
            return True
        return False

    def check_if_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == " ":
                    return False
        return True
