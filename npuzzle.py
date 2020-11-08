import DATA
from heuristics import *
from colors import *
import sys
import copy

def get_dir(dir):
	left = (dir == 0) - (dir == 2)
	up = (dir == 1) - (dir == 3)
	return up, left

def move_index(index, dir):
	up, left = get_dir(dir)
	if (index % DATA.n == 0 and dir == 2) or (index % DATA.n == DATA.n -1 and dir == 0):
		return None
	index = index + (DATA.n * up) + left
	if 0 > index or index > (DATA.n * DATA.n) - 1:
		return None
	return index

def compute_puzzle_cost(puzzle):
	puzzle_cost = [0] * len(puzzle)
	# print("i_m: ", DATA.index_map)
	# print("puz: ", puzzle)
	for i, v in enumerate(puzzle):
		# print("v: ", v, "r: ", compute_manhattan(v, i))
		if v != 0 :
			puzzle_cost[i] = compute_manhattan(v, i)
	# print("cost:", puzzle_cost)
	# puzzle_cost = [compute_manhattan(i) for i, v in enumerate(puzzle) if v != 0]

	return puzzle_cost

class NPuzzle():
	def __init__(self, puzzle, puzzle_cost=None, total_cost=0, history=[], zero=None):
		self.puzzle = puzzle
		if zero != None:
			self.zero = zero
		else:
			self.zero = puzzle.index(0)
		self.end = self.is_game_over()
		self.history = history
		# print("Zero: ", self.zero)
		# print("HISTORY: ", history, self.history)
		if not history:
			self.puzzle_cost = compute_puzzle_cost(puzzle)
			# print("puzzle_cost: ", self.puzzle_cost)
			self.total_cost = 0
			for i in self.puzzle_cost:
				self.total_cost += i
			# print("total_cost: ", self.total_cost)
		else:
			self.total_cost = total_cost + 1
			self.puzzle_cost = puzzle_cost
			self.total_cost -= self.puzzle_cost[self.zero]
			self.puzzle_cost[self.zero] = 0

			old_zero = move_index(self.zero, (self.history[-1] + 2) % 4)
			self.puzzle_cost[old_zero] = compute_manhattan(self.puzzle_cost[old_zero], old_zero)

			self.total_cost += self.puzzle_cost[old_zero]


	def heuristic(self, index, func):
		return func(self, index) + len(self.history)

	def do_move(self, dir):
		# val 0 + val de do_move -> cost to be saved
		if self.history and dir % 2 == self.history[-1] % 2 \
		and dir != self.history[-1]:
			return None

		new_zero = move_index(self.zero, dir)
		if new_zero == None:
			return None

		puzzle = copy.deepcopy(self.puzzle)

		# print("do_move Zero: ", self.zero)
		# print("do_move NewZero: ", new_zero)
		puzzle[self.zero] = puzzle[new_zero]
		puzzle[new_zero] = 0

		if not self.history:
			history = [dir]
		else:
			history = copy.deepcopy(self.history)
			history.append(dir)

		child = NPuzzle(puzzle,
					copy.deepcopy(self.puzzle_cost),
					self.total_cost,
					history,
					new_zero)

		name = ""
		for i in puzzle:
			name += str(i) + ' '

		if not DATA.hmap or not name in DATA.hmap:
			DATA.hmap[name] = True
			return child
		return None


	def is_game_over(self):
		if self.puzzle != DATA.solution:
				return False
		print("GG")
		return True

	def __str__(self):
		m = (DATA.n ** 2) - 1
		m = len(str(m))
		if len(str(-1)):
			m = len(str(-1))
		board = ""
		for idx, val in enumerate(self.puzzle):
			i = self.puzzle[idx]
			if i ==  None:
				i = -1
				board += YELLOW
			elif i == 0:
				board += BLUE
			elif self.puzzle[idx]== DATA.solution[idx]:
				board += GREEN
			else:
				board += RED
			board += "{1:{0}d} ".format(m, i)
			if (idx % DATA.n) == DATA.n - 1:
				board += "\n"
		board += RESET
		board += PURPLE
		board += str(self.history)
		board += RESET + "\n"
		board += RED
		board += "COST IS :" + str(self.total_cost)
		board += RESET + "\n"
		board += "\n"
		return board
