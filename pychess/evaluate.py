#Evalutation code
class evaluate():
	def material(board):
		count = []
		pieceChar = ['PNBRQKpnbrqk']
		for i in range(12):
			count.append(0)

		for i in board:
			count[pieceChar.index(i.character)] += 1