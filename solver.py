import random
from npuzzle import *
import DATA
from heuristics import *
from colors import *
import time

def fill_line(puzzle, index, dir):
	up, left = get_dir(dir)
	val = puzzle[index]
	for i in range(DATA.n - 1):
		if not (0 < (index + (up * DATA.n) + left) < DATA.n * DATA.n):
			break
		if puzzle[index + (up * DATA.n) + left] != None:
			break
		index = index + (up * DATA.n) + left
		puzzle[index] = val + 1
		val = puzzle[index]
	return index

def generate_solution():
	puzzle = [None] * (DATA.n * DATA.n)
	index = 0
	puzzle[index] = 1
	puzzle[(int((DATA.n)/ 2) * DATA.n) + int((DATA.n - 1) / 2)] = 0
	dir = 0
	while None in puzzle:
		index = fill_line(puzzle, index, dir)
		dir = (dir + 1) % 4
	return puzzle

def generate():
	array = list(range(0, DATA.n * DATA.n))
	random.shuffle(array)
	return array

def get_index_map(solution):
	# print(solution)
	rev = [0] * len(solution)
	for i, v in enumerate(solution):
		rev[v] = i
	return rev

def benchmark(func):
    """
    Un décorateur qui affiche le temps qu'une fonction met à s'éxécuter
    """
    import time
    def wrapper(*args, **kwargs):
        t = time.perf_counter()
        res = func(*args, **kwargs)
        print(func.__name__, time.perf_counter()-t)
        return res
    return wrapper

class Solver():
	def __init__(self, DATA, puzzle=None):
		if puzzle:
			self.puzzle = puzzle
		else:
			self.puzzle = generate()
		self.original_puzzle = copy.deepcopy(self.puzzle)
		DATA.solution = generate_solution()
		DATA.index_map = get_index_map(DATA.solution)
		self.statistics = []
		# print(DATA.index_map)
		self.big_queue = []
		self.launch_Astar()

	@benchmark
	def launch_Astar(self):
		tt_cost = lambda x: x.total_cost
		self.big_queue = []
		self.big_queue.append(NPuzzle(self.puzzle))

		state_studied = 0
		loop_nb = 0
		end = False
		while len(self.big_queue) and end == False:
		# for i in range(3):
			loop_nb += 1
			# if True:
			# 	print(self.big_queue[0])
			for dir in range(4):
				child = self.big_queue[0].do_move(dir)
				if child != None:
					state_studied += 1
					self.big_queue.append(child)
					if child.is_game_over():
						# print("GGGGGGGG")
						# print("Total states studied: ", state_studied)
						# print("Was originally: ", self.original_puzzle)
						# print(child)
						end = True
						break
			del self.big_queue[0]

			self.big_queue.sort(key=tt_cost)
		print("Queue of states:            {}".format(len(self.big_queue)))
		print("Total nb states generated:  {}".format(state_studied))
		print("A* cycle number:            {}".format(loop_nb))


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
		return board
