import numpy as np
import requester as req
from copy import deepcopy
import time
from helper import kth_diag_indices


class Game:
    def __init__(self, n, m):
        self.n = n
        self.target = m
        self.curr_board_state = np.full([n, n], ".")
        self.copy_board_state = np.full([n, n], ".")
        self.nmoves = 0

    def draw_board(self):
        for row in range(self.n):
            r = ""
            for column in range(self.n):
                r = r + f" {self.curr_board_state[row][column]} |"
            print(r)

    def is_tie(self, board):
        num = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if board[i][j] != ".":
                    num += 1
        if num == self.n * self.n:
            return True
        return False

    def heuristics(self, board):
        cons_x_row = 0
        cons_x_col = 0
        cons_x_diag = 0
        cons_y_row = 0
        cons_y_col = 0
        cons_y_diag = 0

        for i in range(0, self.n):
            row = board[i]
            for j in range(0, len(row)):
                try:
                    sub_row = row[j: j + self.target]
                except:
                    break
                if "O" not in sub_row and "X" in sub_row:
                    cons_x_row += 100
                elif "X" not in sub_row and "O" in sub_row:
                    cons_y_row += -100

        for i in range(0, self.n):
            col = board[:, i]
            for j in range(0, len(col)):
                try:
                    sub_col = col[j: j + self.target]
                except:
                    break
                if "O" not in sub_col and "X" in sub_col:
                    cons_x_col += 100
                elif "X" not in sub_col and "O" in sub_col:
                    cons_y_col += 100

        for i in range(board.shape[1]):
            diag = np.diagonal(board, offset=i)
            b_diag1 = np.diagonal(board, offset=i+1, axis1=1, axis2=0)
            flip_diag = np.flipud(board).diagonal(offset=i)
            b_diag2 = np.flipud(board).diagonal(offset=i+1, axis1=1, axis2=0)

            if len(diag) >= self.target:
                for i in range(0, len(diag)):
                    try:
                        sub_diag = diag[i : i + self.target]
                    except:
                        break
                    if "O" not in sub_diag and "X" in sub_diag:
                        cons_x_diag += 100
                    elif "X" not in sub_diag and "O" in sub_diag:
                        cons_y_diag += 100

            if len(b_diag1) >= self.target:
                for i in range(0, len(b_diag1)):
                    try:
                        sub_diag = b_diag1[i : i + self.target]
                    except:
                        break
                    if "O" not in sub_diag and "X" in sub_diag:
                        cons_x_diag += 50
                    elif "X" not in sub_diag and "O" in sub_diag:
                        cons_y_diag += 50

            if len(b_diag2) >= self.target:
                for i in range(0, len(b_diag2)):
                    try:
                        sub_diag = b_diag2[i : i + self.target]
                    except:
                        break
                    if "O" not in sub_diag and "X" in sub_diag:
                        cons_x_diag += 50
                    elif "X" not in sub_diag and "O" in sub_diag:
                        cons_y_diag += 50

            if len(flip_diag) >= self.target:
                for i in range(0, len(flip_diag)):
                    try:
                        sub_diag = flip_diag[i : i + self.target]
                    except:
                        break
                    if "O" not in sub_diag and "X" in sub_diag:
                        cons_x_diag += 100
                    elif "X" not in sub_diag and "O" in sub_diag:
                        cons_y_diag += 100

        max_wins_x = max(cons_x_row, cons_x_col, cons_x_diag)
        max_wins_y = max(cons_y_row, cons_y_col, cons_y_diag)

        if max_wins_x > max_wins_y:
            return (max_wins_x, 0, 0)
        elif max_wins_x < max_wins_y:
            return (-max_wins_y, 0, 0)
        else:
            return (0, 0, 0)

    def is_won(self, player, board):

        is_won = False

        rows = list()
        cols = list()
        diags = list()
        winning_pattern = player * self.target

        for i in range(board.shape[0]):
            sublist = board[i].tolist()
            ele = ''.join(sublist)
            if winning_pattern in ele:
                is_won = True
        for i in range(board.shape[1]):
            sublist = board[:, i].tolist()
            ele = ''.join(sublist)
            if winning_pattern in ele and is_won == False:
                is_won = True
        for i in range(board.shape[1]):
            d1 = np.diagonal(board, offset=i).tolist()
            d2 = np.diagonal(board, offset=i, axis1=1, axis2=0).tolist()
            d3 = np.flipud(board).diagonal(offset=i).tolist()
            d4 = np.flipud(board).diagonal(offset=i, axis1=1, axis2=0).tolist()
            ele1 = ''.join(d1)
            ele2 = ''.join(d2)
            ele3 = ''.join(d3)
            ele4 = ''.join(d4)

            if winning_pattern in ele1 or winning_pattern in ele2 or winning_pattern in ele3 or winning_pattern in ele4 and is_won == False:
                is_won = True

        if is_won and player == "X":
            return (1, 0, 0)
        elif is_won and player == "O":
            return (-1, 0, 0)

    def is_end_of_game(self, depth: int, board):
        if self.is_tie(board):
            return True
        elif self.is_won("X", board) is not None:
            return True
        elif self.is_won("O", board) is not None:
            return True
        elif depth == 0:
            return True
        return False

    def max_value(self, alpha: float, beta: float, depth: int) -> tuple:
        """Player X, i.e. AI."""
        max_value = -2
        # initialize maximizer's coordinates
        max_x, max_y = None, None

        if self.is_end_of_game(depth, self.copy_board_state):
            if self.is_tie(self.copy_board_state):
                return (0, 0, 0)
            elif self.is_won("X", self.copy_board_state) is not None:
                return self.is_won("X", self.copy_board_state)
            elif self.is_won("O", self.copy_board_state) is not None:
                return self.is_won("O", self.copy_board_state)
            else:
                return self.heuristics(self.copy_board_state)

        for i in range(0, self.n):
            for j in range(0, self.n):
                # if empty, make a move and call minimizer
                if self.copy_board_state[i][j] == ".":
                    self.copy_board_state[i][j] = "X"
                    v, min_x, min_y = self.min_value(alpha, beta, depth - 1)

                    # maximize further
                    if v > max_value:
                        max_value = v
                        max_x = i
                        max_y = j
                    # undo move
                    self.copy_board_state[i][j] = "."
                    # print(max_value, beta, alpha)
                    # stop examining moves, if current value better than beta
                    if max_value >= beta:
                        return max_value, max_x, max_y
                    # update alpha if current value is less
                    if max_value > alpha:
                        alpha = max_value

        return max_value, max_x, max_y

    def min_value(self, alpha: float, beta: float, depth: int) -> tuple:
        """Player O, i.e. our code."""
        min_value = 2
        # initialize minimizer's coordinates
        min_x, min_y = None, None

        if self.is_end_of_game(depth, self.copy_board_state):
            if self.is_tie(self.copy_board_state):
                return (0, 0, 0)
            elif self.is_won("X", self.copy_board_state) is not None:
                return self.is_won("X", self.copy_board_state)
            elif self.is_won("O", self.copy_board_state) is not None:
                return self.is_won("O", self.copy_board_state)
            else:
                return self.heuristics(self.copy_board_state)

        for i in range(0, self.n):
            for j in range(0, self.n):
                # if empty, make a move and call maximizer
                if self.copy_board_state[i][j] == ".":
                    self.copy_board_state[i][j] = "O"
                    v, max_x, max_y = self.max_value(alpha, beta, depth - 1)

                    # minimize further
                    if v < min_value:
                        min_value = v
                        min_x = i
                        min_y = j
                    # undo move
                    self.copy_board_state[i][j] = "."

                    # stop examining moves, if current value is already less than alpha
                    if min_value <= alpha:
                        return min_value, min_x, min_y
                    # update beta if current value is less
                    if min_value < beta:
                        beta = min_value

        return min_value, min_x, min_y


def play_game(opponent_team_id: int, n: int, m: int):
    """Play the game."""
    max_depth = 3
    game = Game(n=n, m=m)
    while not game.is_end_of_game(max_depth, game.curr_board_state):
        game.copy_board_state = deepcopy(game.curr_board_state)
        min_value, min_x, min_y = game.min_value(alpha=-2, beta=2, depth=max_depth)
        if game.curr_board_state[min_x][min_y] != ".":
            print("Incorrect move made by your code!")
            break
        print("O makes this move: {}, {}".format(min_x, min_y))
        game.curr_board_state[min_x][min_y] = "O"
        game.nmoves += 1
        game.draw_board()
        if game.is_end_of_game(max_depth, game.curr_board_state):
            break
        x, y = input("Enter x and y for oppo: ").split()
        x = int(x)
        y = int(y)
        if game.curr_board_state[x][y] != ".":
            print("Incorrect move made by opponent!")
            break
        print("X makes this move: {}, {}".format(x, y))
        game.curr_board_state[x][y] = "X"
        game.nmoves += 1
        game.draw_board()
        # max_depth = max_depth - 1

    if game.is_end_of_game(max_depth, game.curr_board_state):
        print("Game over!")
        if game.is_won("X", game.curr_board_state) is not None:
            print("X won!")
        elif game.is_won("O", game.curr_board_state) is not None:
            print("O won!")
        elif game.is_tie(game.curr_board_state):
            print("Tie!")

        game.draw_board()


if __name__ == "__main__":

    # add exception handlers later
    opponent_team_id = int(input("Please enter opponent team id: \n"))
    n, m = input("Enter n and m for an n x n game with target m: ").split()
    play_game(opponent_team_id, int(n), int(m))
