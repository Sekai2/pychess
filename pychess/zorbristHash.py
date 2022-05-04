from PRNG import *
#zobrist hashing class
class hashTable():
	def __init__(self, seed = time.time_ns()):
		self.constVal = [0,1,2,3,4,5,6,7,8,9,10,11]
		self.pieceChar = 'PRBNQKprbnqk'
		self.random_val = PRNG.LCG(maxn = 768, seedn = seed, m = 18446744073709551557, a = 2774243619903564593)
		self.table = []
		self.black_move = PRNG.LCG(maxn = 1, seedn = 4829959, m = 18446744073709551557, a = 2774243619903564593)[0]
		self.hashTbl = {}

	def init_zobrist(self):
		self.table = []
		for i in range(64):
			self.table.append([])
			for j in range(12):
				self.table[i].append(None)

		for i in range(64):
			for j in range(12):
				self.table[i][j] = self.random_val[i*12 + j]

	def hash(self, board, colour):
		h = 0
		if colour == 'black':
			h = h ^ self.black_move

		p = 0
		for i in range(128):
			if (i & 0x88) == 0:
				if board.board[i] != None:
					j = self.constVal[self.pieceChar.index(board.board[i].character)]
					h = h ^ self.table[p][j]

				p += 1
		return h

	#adding items to the lookup table
	def append(self, board, colour, score, FEN, hashVal = None):
		content = [board, score, FEN]
		if hashVal == None:
			hashVal = self.hash(board, colour)
		if hashVal not in self.hashTbl:
			self.hashTbl[hashVal] = content

		else:
			if self.hashTbl[hashVal][2] == content[2]:
				return
			replace = self.hashTbl[hashVal]
			replace = (replace[0], replace[1], replace[2], hashVal + 1)
			self.append(board, colour, score, FEN, hashVal = hashVal + 1)

	def find(self, content, colour, hashVal = None):
		if hashVal == None:
			hashVal = self.hash(content, colour)

		if hashVal in self.hashTbl:
			if len(self.hashTbl[hashVal]) == 4:
				if self.hashTbl[2] == self.hashTabl[2]:
					return self.hashTbl[hashVal]
				return self.find(content, hashVal + 1)

			else:
				return self.hashTbl[hashVal]