import sys
from colors import *
import DATA


from solver import *
from heuristics import *


dir_solution = [1, 1, 0, 3, 3, 0, 1, 2, 3, 2, 1, 0, 3, 0, 1, 2, 3, 2, 1, 0]
#len queu is 48670

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
	if len(sys.argv) > 1:
		DATA.n = int(sys.argv[1])
	else:
		DATA.n = 3
	# two_move = [1, 3, 0, 8, 2, 4, 7, 6, 5]
	# two_move = gen_test_n_moves(5000)
	# two_move = apply_moves(generate_solution(), dir_solution)
	P = Solver(DATA, [2, 1, 3, 8, 0, 4, 7, 6, 5])
	# print(P)
