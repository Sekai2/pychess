import numba
from numba import jit

def countMaterial(board):
		count = []
		pieceChar = ['PNBRQKpnbrqk']
		for i in range(12):
			count.append(0)

		for i in board:
			if i != None:
				count[pieceChar.index(i.character)] += 1

		return count

#Evalutation code
class evaluate():
	@jit(nopython = True)
	def valMult(a, b):#for material calculation
		return a * b

	@jit(nopython = True)
	def valSub(a, b):
		return a - b

	def material(count):
		return reduce()