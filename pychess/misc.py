#miscellaneous functions

def negcheck(x):
	if x < 0:
		return True
	return False

def board_file(i):
	file = i & 7
	return file

def board_rank(i):
	rank = (i >> 4)
	return rank

def abs(x):
	if negcheck(x) == True:
		x = -1 * x
	return x