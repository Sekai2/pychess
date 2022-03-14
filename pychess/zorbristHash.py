from PRNG import *
#zobrist hashing class
class zobrist():
	def __init__(self, seed = time.time_ns()):
		self.white_pawn = 1
		self.white_rook = 2
		self.white_bishop = 3
		self.white_knight = 4
		self.white_queen = 5
		self.white_king = 6
		self.black_pawn = 7
		self.black_rook = 8
		self.black_bishop = 9
		self.black_knight = 10
		self.black_queen = 11
		self.black_king = 12
		self.random_val = PRNG.LCG(768, seed)
		self.table = []
		self.black_move = PRNG.LCG(1)

	def init_zobrist(self):
		self.table = []
		for i in range(64):
			self.table.append([])
			for j in range(12):
				self.table[i].append(None)

		for i in range(64):
			for j in range(12):
				self.table[i][j] = self.random_val[i*j]

	def hash(borad):
		h = 0


zob = zobrist()
zob.init_zobrist()
print(zob.black_move)