import sys
from colors import *
import DATA


from solver import *
from heuristics import *

test_3_50 = [
	[0, 1, 3, 8, 2, 4, 7, 6, 5],
	[2, 0, 8, 7, 6, 4, 5, 3, 1],
	[3, 8, 4, 1, 2, 5, 7, 6, 0],
	[1, 4, 6, 8, 3, 2, 0, 7, 5],
	[1, 2, 3, 0, 8, 4, 7, 6, 5],
	[1, 3, 6, 8, 2, 4, 7, 0, 5],
	[2, 4, 6, 1, 3, 5, 8, 0, 7],
	[6, 1, 2, 4, 0, 3, 8, 7, 5],
	[0, 6, 2, 1, 8, 3, 7, 5, 4],
	[8, 1, 3, 7, 4, 0, 6, 2, 5],
	[3, 8, 5, 0, 1, 2, 7, 4, 6],
	[1, 3, 6, 2, 0, 4, 8, 7, 5],
	[1, 0, 3, 8, 2, 6, 7, 5, 4],
	[7, 8, 3, 6, 0, 5, 2, 4, 1],
	[0, 1, 4, 8, 6, 2, 7, 5, 3],
	[1, 0, 2, 7, 4, 3, 6, 8, 5],
	[2, 3, 4, 6, 7, 8, 1, 0, 5],
	[1, 2, 3, 8, 5, 0, 7, 4, 6],
	[1, 3, 4, 0, 2, 7, 8, 6, 5],
	[1, 2, 3, 0, 5, 8, 7, 6, 4]]


dir_solution = [1, 1, 0, 3, 3, 0, 1, 2, 3, 2, 1, 0, 3, 0, 1, 2, 3, 2, 1, 0]
#len queu is 48670

def gen_dataset(size, shuffle):
	print("test_" + str(DATA.n) + "_" + str(size) + " = [")
	for i in range(20):
		test = gen_test_n_moves(shuffle)
		print(test, ",")
	print("]")


def gen_test_n_moves(n):
	solution = generate_solution()
	for i in range(n):
		zero = solution.index(0)
		new_zero = None
		while new_zero == None:
			new_zero = move_index(zero, random.randint(0, 4))
		solution[zero] = solution[new_zero]
		solution[new_zero] = 0
	return solution

def apply_moves(puzzle, moves):
	solution = puzzle
	for dir in moves[-1:0:-1]:
		zero = solution.index(0)
		new_zero = None
		while new_zero == None:
			new_zero = move_index(zero, dir)
		solution[zero] = solution[new_zero]
		solution[new_zero] = 0
	return solution

if __name__ == "__main__":
	if len(sys.argv) == 2:
		DATA.n = int(sys.argv[1])
	else:
		DATA.n = 3
	if len(sys.argv) > 2:
		if sys.argv[1] == "test":
	 		P = Solver(DATA, test_3_50[int(sys.argv[2])])
	else:
		test = gen_test_n_moves(500)
		P = Solver(DATA, test)
	# two_move = [1, 3, 0, 8, 2, 4, 7, 6, 5]
	# test = [4, 7, 2, 1, 3, 5, 6, 8, 0]
	# two_move = apply_moves(generate_solution(), dir_solution)
	# P = Solver(DATA, test)
	# P = Solver(DATA, [2, 1, 3, 8, 0, 4, 7, 6, 5])
	# print(P)
