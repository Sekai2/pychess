from PRNG import *
#zobrist hashing class
class hashTable():
	def __init__(self, seed = time.time_ns()):
		self.constVal = [0,1,2,3,4,5,6,7,8,9,10,11]
		self.pieceChar = 'PRBNQKprbnqk'
		self.random_val = PRNG.LCG(maxn = 768, seedn = seed, m = 268435399, a = 246049789)
		self.table = []
		self.black_move = PRNG.LCG(maxn = 1, seedn = 4829959, m = 268435399, a = 246049789)[0]
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
		for i in range(128):
			if (i & 0x88) == 0:
				if board.board[i] != None:
					j = self.constVal[self.pieceChar.index(board.board[i].character)]
					h = h ^ self.table[p][j]

				p += 1
		board.print_board()
		print(h)
		return h

	def append(self, hashVal, content):
		if self.hashTbl[hashVal] == None:
			self.hashTbl[hashVal] = content

		else:
			print('colision')
			replace = self.hashTbl[hashVal]
			replace = (replace[0], replace[1], hashVal + 1)
			self.append(hashVal + 1, content)

	def find(self, content, hashVal = None):
		if hashVal == None:
			hashVal = self.hash(content)

		if len(hashTbl[hashVal]) == 3:
			return self.find(content, hashVal + 1)

		else:
			return hashTbl[hashVal]

if __name__ == '__main__':
	class piece():
		def __init__(self, character):
			self.character = character


	class board():
		def __init__(self):
			self.board = []
			for i in range(128):
				self.board.append(None)
			self.board[0] = piece('R')
			self.board[1] = piece('N')
			self.board[2] = piece('B')
			self.board[3] = piece('Q')
			self.board[4] = piece('K')
			self.board[5] = piece('B')
			self.board[6] = piece('N')
			self.board[7] = piece('R')
			self.board[16] = piece('P')
			self.board[17] = piece('P')
			self.board[18] = piece('P')
			self.board[19] = piece('P')
			self.board[20] = piece('P')
			self.board[21] = piece('P')
			self.board[22] = piece('P')
			self.board[55] = piece('P')
			self.board[96] = piece('p')
			self.board[97] = piece('p')
			self.board[98] = piece('p')
			self.board[99] = piece('p')
			self.board[100] = piece('p')
			self.board[101] = piece('p')
			self.board[102] = piece('p')
			self.board[103] = piece('p')
			self.board[112] = piece('r')
			self.board[113] = piece('n')
			self.board[114] = piece('b')
			self.board[115] = piece('q')
			self.board[116] = piece('k')
			self.board[117] = piece('b')
			self.board[118] = piece('n')
			self.board[119] = piece('r')

	board1 = board()
	hashtbl = hashTable()
	hashtbl.init_zobrist()
	hashtbl.hash(board1, 'white')