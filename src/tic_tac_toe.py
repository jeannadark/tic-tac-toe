import numpy as np


class Game:
	def __init__(self, n, m):
		self.n = n
		self.m = m
		self.curr_board_state = np.zeros((n, m))
	
	def draw_board(self):
		# -- #

	def is_valid_move(self, x, y):
		# -- #

	def is_game_finished(self):
		# -- #

	def evaluate_game(self):
		# -- #

	def max_value(self, alpha: float, beta: float) -> tuple:
		"""Player O, i.e. AI."""
		max_value = -float('inf')
		# initialize maximizer's coordinates
		max_x, max_y = None, None
		# if game is finished, evaluate scores
		if self.is_game_finished:
			return self.evaluate_game()

		for i in range(0, self.n):
			for j in range(0, self.m):
				# if empty, make a move and call minimizer
				if self.curr_board_state[i][j] == " ":
					self.curr_board_state[i][j] = "O"
					v, min_x, min_y = self.min_value(alpha, beta)

					# maximize further
					if v > max_value:
						max_value = v
						max_x = i
						max_y = j
					# undo move
					self.curr_board_state[i][j] = " "

					# stop examining moves, if current value better than beta
					if max_value >= beta:
						return max_value, max_x, max_y
					# update alpha if current value is less
					if max_value > alpha:
						alpha = max_value

		return max_value, max_x, max_y

	def min_value(self, alpha: float, beta: float) -> tuple:
		"""Player X, i.e. opponent."""
		min_value = float('inf')
		# initialize minimizer's coordinates
		min_x, min_y = None, None
		# if game is finished, evaluate scores
		if self.is_game_finished:
			return self.evaluate_game()

		for i in range(0, self.n):
			for j in range(0, self.m):
				# if empty, make a move and call maximizer
				if self.curr_board_state[i][j] == " ":
					self.curr_board_state[i][j] = "X"
					v, max_x, max_y = self.max_value(alpha, beta)

					# minimize further
					if v < min_value:
						min_value = v
						min_x = i
						min_y = j
					# undo move
					self.curr_board_state[i][j] = " "

					# stop examining moves, if current value is already less than alpha
					if min_value <= alpha:
						return min_value, min_x, min_y
					# update beta if current value is less
					if min_value < beta:
						beta = min_value

		return min_value, min_x, min_y

	def play_game(self):
		# -- #




def main():
	# -- #
	# useful resource for requests handling: https://github.com/Eyasluna/CSCI_6511_AI_spring2020/blob/master/project_2/tictactoe.py