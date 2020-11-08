import DATA
import math

# 123
# 804
# 765


def compute_manhattan(a, i):
	b = DATA.index_map[a]
	a = i
	# print("a: ", a)
	# print("b: ", b)
	y_delta = int(abs(a - b) / DATA.n)
	# print("y: ", y_delta)
	x_delta = abs(a - b) % DATA.n
	# print("x: ", x_delta)
	return y_delta + x_delta
