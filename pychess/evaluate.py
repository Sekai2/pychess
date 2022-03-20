import numba
from numba import jit

def countMaterial(board):
		count = []
		pieceChar = 'PNBRQKpnbrqk'
		for i in range(12):
			count.append(0)

		for i in board:
			if i != None:
				count[pieceChar.find(i.character)] += 1
		return count

#Evalutation code
class evaluate():
	def valSub(count, i):
		return count[i] - count[i + 6]

	def bishopPair(count):
		pairScore = 0
		if count[2] >= 2:
			if count[0] + count[6] >= 8:
				pairScore += ((16 - count[0]- count[6]) * 5) + 10

			else:
				pairScore += 50

		if count[8] >= 2:
			if count[0] + count[6] >= 8:
				pairScore -= ((16 - count[0]- count[6]) * 5) + 10

			else:
				pairScore -= 50

		return pairScore

	def material(count):
		multiplier = [100,350,350,525,1000,10000]
		materialScore = 0
		index = 0
		for i in multiplier:
			materialScore += i * evaluate.valSub(count, index)
			index += 1

		materialScore += evaluate.bishopPair(count)

		return materialScore