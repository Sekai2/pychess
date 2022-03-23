from PRNG import *
#zobrist hashing class
class hashTable():
	def __init__(self, seed = time.time_ns()):
		self.constVal = [0,1,2,3,4,5,6,7,8,9,10,11]
		self.pieceChar = 'PRBNQKprbnqk'
		self.random_val = PRNG.LCG(maxn = 768, seedn = seed, m = 268435399, a = 246049789)
		self.table = []
		self.black_move = PRNG.LCG(maxn = 1, seedn = 4829959, m = 268435399, a = 246049789)
		self.hashTbl = []
		for i in range(268435399):
			self.hashTbl.append(None)

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

	def append(hashVal, content):
		if self.hashTbl[hashVal] == None:
			self.hashTbl[hashVal] = content

		else:
			replace = self.hashTbl[hashVal]
			replace = (replace[0], replace[1], hashVal + 1)
			self.append(hashVal + 1, content)

	def find(content, hashVal = 0):
		hashVal = self.hash(content)
		if len(hashTbl[hashVal]) == 3:
			return self.find(content, hashVal + 1)

		else:
			return hashTbl[hashVal]