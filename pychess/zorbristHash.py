from PRNG import *
#zobrist hashing class
class hashTable():
	def __init__(self, seed = time.time_ns()):
		self.constVal = [0,1,2,3,4,5,6,7,8,9,10,11]
		self.pieceChar = 'PRBNQKprbnqk'
		self.random_val = PRNG.LCG(768, seed, 18446744073709551557, 13891176665706064842)
		self.table = []
		self.black_move = PRNG.LCG(1, 4829959, 18446744073709551557,13891176665706064842)
		self.hashList = []
		for i in range(18446744073709551557):
			self.hashList.append(None)

	def init_zobrist(self):
		self.table = []
		for i in range(64):
			self.table.append([])
			for j in range(12):
				self.table[i].append(None)

		for i in range(64):
			for j in range(12):
				self.table[i][j] = self.random_val[i*j]

	def hash(self, board, colour):
		h = 0
		if colour == 'black':
			h = h ^ self.black_move

		p = 0
		print(len(board.board))
		for i in range(128):
			print(board.board[i])
		for i in range(128):
			if i % 16 < 9:
				if board.board[i] != None:
					j = self.constVal[self.pieceChar.index(board.board[i].character)]
					h = h ^ self.table[p][j]

				p += 1

		return h

hashTable()