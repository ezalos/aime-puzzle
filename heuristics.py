import DATA
import math

# 123
# 804
# 765
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(mem=None)
def linear_conflict(a, b):
	a_goal = DATA.index_map[a]
	b_goal = DATA.index_map[b]
	if linear_conflict.mem == None:
		s = DATA.n * DATA.n
		linear_conflict.mem = [[-1 for i in range(s)] for j in range(s)]
	if linear_conflict.mem[a][b] == -1:
		same_col = lambda a, b: a % DATA.n == b % DATA.n
		same_row = lambda a, b: int(a / DATA.n) == int(b / DATA.n)
		inside_row = lambda a, ga, b: (int(a / DATA.n) <= int(b / DATA.n) <= int(ga / DATA.n)) or (int(a / DATA.n) >= int(b / DATA.n) >= int(ga / DATA.n))
		inside_col = lambda a, ga, b: (a % DATA.n <= b % DATA.n <= ga % DATA.n) or (a % DATA.n >= b % DATA.n >= ga % DATA.n)
		conflict = 0
		if (same_col(a, b) and same_col(a_goal, b_goal)):
			if inside_col(a, a_goal, b) or inside_col(b, b_goal, a):
				conflict = 1
		elif (same_row(a, b) and  same_row(a_goal, b_goal)):
			if inside_row(a, a_goal, b) or inside_row(b, b_goal, a):
				conflict = 1
		linear_conflict.mem[a][b] = conflict
	return linear_conflict.mem[a][b]

@static_vars(mem=None)
def compute_manhattan(a, i):
	b = DATA.index_map[a]
	a = i
	if compute_manhattan.mem == None:
		s = DATA.n * DATA.n
		compute_manhattan.mem = [[-1 for i in range(s)] for j in range(s)]
	if compute_manhattan.mem[a][b] == -1:
		conflict = linear_conflict(a, b)
		# print("a: ", a)
		# print("b: ", b)
		y_delta = int(abs(a - b) / DATA.n)
		# print("y: ", y_delta)
		x_delta = abs(a - b) % DATA.n
		# print("x: ", x_delta)
		compute_manhattan.mem[a][b] = y_delta + x_delta + conflict
	return compute_manhattan.mem[a][b]

@static_vars(mem=None)
def compute_manhattan2(a, b, z):
	b = DATA.index_map[a]
	a = i
	if compute_manhattan2.mem == None:
		s = DATA.n * DATA.n
		compute_manhattan2.mem = [[[-1 for i in range(s)] for i in range(s)] for j in range(s)]
	if compute_manhattan2.mem[a][b] == -1:
		conflict = 0
		if a % DATA.n == b % DATA.n or int(a / DATA.n) == int(b / DATA.n) :
			conflict = 2
		# print("a: ", a)
		# print("b: ", b)
		y_delta = int(abs(a - b) / DATA.n)
		# print("y: ", y_delta)
		x_delta = abs(a - b) % DATA.n
		# print("x: ", x_delta)
		compute_manhattan2.mem[a][b] = y_delta + x_delta + conflict
	return compute_manhattan2.mem[a][b]

# // sum min(manhattan(0, a), manhattan(0, b)), manhattan(a, b) + 2 conflit
