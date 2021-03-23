import numpy as np
import requester as req
from copy import deepcopy
import time

# the remaining issue is in the two copies of the board
class Game:
    def __init__(self, n, m):
        self.n = n
        self.target = m
        self.curr_board_state = np.zeros((n, n)).astype(str)
        self.copy_board_state = np.zeros((n, n)).astype(str)
        self.nmoves = 0

    def draw_board(self):
        for row in range(self.n):
            r = ''
            for column in range(self.n):
                r = r + f" {self.curr_board_state[row][column]} |"
            print(r)

    def is_tie(self):
        is_tie = False
        if self.nmoves+1== self.n * self.n:
            is_tie = True
        if is_tie:
            return (0, 0, 0)

    def is_won(self, player):
        is_won = False
        for indexes in self.check_indexes(self.target):
            if all(self.curr_board_state[r][c] == player for r, c in indexes):
                is_won = True
        if is_won and player == 'X':
            return (1, 0, 0)
        if is_won and player == 'O':
            return (0, 0, -1)

    def is_end_of_game(self, depth: int):
        if self.is_tie() is not None:
            return True
        elif self.is_won("X") is not None:
            return True
        elif self.is_won("O") is not None:
            return True
        elif depth == 0:
            return True
        return False

    def check_indexes(self, n):
        for r in range(n):
            yield [(r, c) for c in range(n)]
        for c in range(n):
            yield [(r, c) for r in range(n)]
        yield [(i, i) for i in range(n)]
        yield [(i, n - 1 - i) for i in range(n)]

    def max_value(self, alpha: float, beta: float, depth: int) -> tuple:
        """Player X, i.e. AI."""
        max_value = -2
        # initialize maximizer's coordinates
        max_x, max_y = None, None

        if self.is_end_of_game(depth):
            if self.is_tie() is not None:
                return self.is_tie()
            elif self.is_won("X") is not None:
                return self.is_won("X")
            elif self.is_won("O") is not None:
                return self.is_won("O")

        for i in range(0, self.n):
            for j in range(0, self.n):
                # if empty, make a move and call minimizer
                if self.curr_board_state[i][j] == '0.0':
                    self.curr_board_state[i][j] = "X"
                    v, min_x, min_y = self.min_value(alpha, beta, depth - 1)
                    print(max_value)
                    # maximize further
                    if v > max_value:
                        max_value = v
                        max_x = i
                        max_y = j
                    # undo move
                    self.curr_board_state[i][j] = '0.0'
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

        if self.is_end_of_game(depth):
            if self.is_tie() is not None:
                return self.is_tie()
            elif self.is_won("X") is not None:
                return self.is_won("X")
            elif self.is_won("O") is not None:
                return self.is_won("O")

        for i in range(0, self.n):
            for j in range(0, self.n):
                # if empty, make a move and call maximizer
                if self.curr_board_state[i][j] == '0.0':
                    self.curr_board_state[i][j] = "O"
                    v, max_x, max_y = self.max_value(alpha, beta, depth - 1)
                    print(min_value)
                    # minimize further
                    if v < min_value:
                        min_value = v
                        min_x = i
                        min_y = j
                    # undo move
                    self.curr_board_state[i][j] = '0.0'   

                    # stop examining moves, if current value is already less than alpha
                    if min_value <= alpha:
                        return min_value, min_x, min_y
                    # update beta if current value is less
                    if min_value < beta:
                        beta = min_value

        return min_value, min_x, min_y


def play_game(opponent_team_id: int, n: int, m: int):
    """Play the game."""
    max_depth = 5
    game = Game(n=n, m=m)
    while not game.is_end_of_game(max_depth):
        game.copy_board_state = deepcopy(game.curr_board_state)
        min_value, min_x, min_y = game.min_value(alpha=-2, beta=2, depth = max_depth)
        if game.curr_board_state[min_x][min_y] != '0.0':
            print("Incorrect move made by your code!")
            break
        print("O makes this move: {}, {}".format(min_x, min_y))
        game.curr_board_state[min_x][min_y] = "O"
        game.nmoves += 1
        x, y = input("Enter x and y for oppo: ").split()
        x = int(x)
        y = int(y)
        if game.curr_board_state[x][y] != '0.0':
            print("Incorrect move made by opponent!")
            break
        print("X makes this move: {}, {}".format(x, y))
        game.curr_board_state[x][y] = "X"
        game.nmoves += 1
        game.draw_board()
        max_depth = max_depth - 1

    if game.is_end_of_game(max_depth):
        print("Game over!")
        result = game.is_tie()
        if result is not None:
            print("Tie!")
        elif game.is_won("X") is not None:
            print("X won!")
        elif game.is_won("O") is not None:
            print("O won!")
        game.draw_board()


if __name__ == "__main__":

    # add exception handlers later
    opponent_team_id = int(input("Please enter opponent team id: \n"))
    n, m = input("Enter n and m for an n x n game with target m: ").split()
    play_game(opponent_team_id, int(n), int(m))
