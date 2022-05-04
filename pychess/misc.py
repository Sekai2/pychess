#miscellaneous functions
from PRNG import *

def negcheck(x):
	if x < 0:
		return True
	return False

#board file index
def board_file(i):
	file = i & 7
	return file

#board rank index
def board_rank(i):
	rank = (i >> 4)
	return rank

#absolute value function
def abs(x):
	if negcheck(x) == True:
		x = -1 * x
	return x

#standard board file function
def file_letter(i):
	rank = 'abcdefgh'
	return rank[board_file(i)]

#standard board rank function
def rank_num(i):
	num = '87654321'
	return str(int(num[board_rank(i)]))

#bitwise left and right rotates
def leftRotate(n, d, bits = 32):
	return(n << d)|(n >> (bits - d))

def rightRotate(n, d, bits = 32):
	return(n >> d)|(n << (bits - d)) & 0xFFFFFFFF

def tupleMax(a, b):
	if a[0] > b[0]:
		return a

	elif a[0] == b[0]:
		rand_val = PRNG.LCG(m = 2)
		if rand_val == 0:
			return a

		else:
			return b

	else:
		return b

def tupleMin(a, b):
	if a[0] < b[0]:
		return a

	else:
		return b