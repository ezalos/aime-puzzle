import numpy as np
import random
import math
import sys

PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def get_dir(dir):
	left = (dir == 0) - (dir == 2)
	up = (dir == 1) - (dir == 3)
	return up, left

def fill_line(puzzle, index, dir):
	up, left = get_dir(dir)
	n = int(math.sqrt(len(puzzle)))
	val = puzzle[index]
	for i in range(n - 1):
		if not (0 < (index + (up * n) + left) < n * n):
			break
		if puzzle[index + (up * n) + left] != None:
			break
		index = index + (up * n) + left
		puzzle[index] = val + 1
		val = puzzle[index]
	return index

def generate_solution(n):
	puzzle = [None] * (n * n)
	index = 0
	puzzle[index] = 1
	puzzle[(int((n)/ 2) * n) + int((n - 1) / 2)] = 0
	dir = 0
	while None in puzzle:
		index = fill_line(puzzle, index, dir)
		dir = (dir + 1) % 4
	return puzzle

def generate(n):
	array = list(range(0, n * n))
	random.shuffle(array)
	return array

class NPuzzle():
	def __init__(self, n):
		self.n = n
		self.puzzle = generate(n)
		self.solution = generate_solution(n)

	def __str__(self):
		m = (self.n ** 2) - 1
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
			elif self.puzzle[idx]== self.solution[idx]:
				board += GREEN
			else:
				board += RED
			board += "{1:{0}d} ".format(m, i)
			if (idx % self.n) == self.n - 1:
				board += "\n"
		board += RESET
		return board

if __name__ == "__main__":
	if len(sys.argv) > 1:
		n = int(sys.argv[1])
	else:
		n = 3
	P = NPuzzle(n)
	print(P)
