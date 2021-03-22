import numpy as np
import requester as req


class Game:
    def __init__(self, n, m):
        self.n = n
        self.target = m
        self.curr_board_state = np.zeros((n, n)).astype(str)
        self.nmoves = 0

    def draw_board(self):
        for row in self.curr_board_state:
            for column in self.curr_board_state:
                print(column + " ")
            print("\n")

    # def is_valid_move(self, x, y):
    #   return self.curr_board_state[x][y]==0

    def is_game_finished(self, player):
        for indexes in self.checkIndexes(self.target):
            if all(self.curr_board_state[r][c] == player for r, c in indexes):
                return True
        return False

    def checkIndexes(self, n):
        for r in range(n):
            yield [(r, c) for c in range(n)]

        for c in range(n):
            yield [(r, c) for r in range(n)]

        yield [(i, i) for i in range(n)]
        yield [(i, n - 1 - i) for i in range(n)]

    def evaluate_game(self, player):
        if player == "X":
            return "X won"
        elif player == "O":
            return "O won"
        elif game.nmoves == game.n ** 2:
            return "Tie"

    def max_value(self, alpha: float, beta: float) -> tuple:
        """Player X, i.e. AI."""
        max_value = -float("inf")
        # initialize maximizer's coordinates
        max_x, max_y = None, None
        # if game is finished, evaluate scores
        if self.is_game_finished("X"):
            return self.evaluate_game("X")

        for i in range(0, self.n):
            for j in range(0, self.n):
                # if empty, make a move and call minimizer
                if self.curr_board_state[i][j] == '0':
                    self.curr_board_state[i][j] = "X"
                    v, min_x, min_y = self.min_value(alpha, beta)

                    # maximize further
                    if v > max_value:
                        max_value = v
                        max_x = i
                        max_y = j
                    # undo move
                    self.curr_board_state[i][j] = '0'

                    # stop examining moves, if current value better than beta
                    if max_value >= beta:
                        return max_value, max_x, max_y
                    # update alpha if current value is less
                    if max_value > alpha:
                        alpha = max_value

        return max_value, max_x, max_y

    def min_value(self, alpha: float, beta: float) -> tuple:
        """Player O, i.e. human."""
        min_value = float("inf")
        # initialize minimizer's coordinates
        min_x, min_y = None, None
        # if game is finished, evaluate scores
        if self.is_game_finished:
            return self.evaluate_game()

        for i in range(0, self.n):
            for j in range(0, self.n):
                # if empty, make a move and call maximizer
                if self.curr_board_state[i][j] == '0':
                    self.curr_board_state[i][j] = "O"
                    v, max_x, max_y = self.max_value(alpha, beta)

                    # minimize further
                    if v < min_value:
                        min_value = v
                        min_x = i
                        min_y = j
                    # undo move
                    self.curr_board_state[i][j] = '0'   

                    # stop examining moves, if current value is already less than alpha
                    if min_value <= alpha:
                        return min_value, min_x, min_y
                    # update beta if current value is less
                    if min_value < beta:
                        beta = min_value

        return min_value, min_x, min_y


def play_game(opponent_team_id: int, n: int, m: int):
    """Play the game."""
    while True:
        game_id = req.create_game(opponent_team_id)
        game = Game(n=n, m=m)
        max_value, max_x, max_y = game.max_value(alpha=-float("inf"), beta=float("inf"))
        print("AI makes this move: {}, {}".format(max_x, max_y))
        # if self.is_valid_move(max_x, max_y):
        req.make_a_move(game_id, (max_x, max_y))
        game.nmoves += 1
        moves = req.get_move_list(game_id)["moves"]
        # wait for the opponent to make a move
        while req.get_move_list(game_id) == moves:
            time.sleep(2)
        game.nmoves += 1
        # now update the game's current board state with the moves made by AI and opponent
        for move in moves:
            symbol = move["symbol"]
            x = int(move["move"].split(",")[0])
            y = int(move["move"].split(",")[1])
            game.curr_board_state[x][y] = symbol
        # print the board
        req.get_board_map(game_id)
        if game.is_game_finished():
            print("Game over!")
            game.draw_board()
            break


if __name__ == "__main__":

    # add exception handlers later
    opponent_team_id = int(input("Please enter opponent team id: \n"))
    n, m = input("Enter n and m for an n x n game with target m: ").split()
    play_game(opponent_team_id, int(n), int(m))
