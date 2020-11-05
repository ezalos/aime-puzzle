import numpy as np
import random
import sys

def generate_n_puzzle(n):

	array = list(range(0, n * n))
	random.shuffle(array)
	print(array)
	puzzle = []
	[puzzle.append(array[(i * n) : (i + 1) * n]) for i in range(n)]
	return puzzle


if __name__ == "__main__":
	if len(sys.argv) > 1:
		print(generate_n_puzzle(int(sys.argv[1])))
