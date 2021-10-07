from piece import *

#Board Class
class ChessBoard:
	def __init__(self):
		self.board = []
		for i in range(128):
			self.board.append(None)

		#adding pieces
		#add white pieces
		self.board[0] = Rook('white', 0)
		self.board[1] = Knight('white', 1)
		self.board[2] = Bishop('white', 2)
		self.board[3] = Queen('white', 3)
		self.board[4] = King('white', 4)
		self.board[5] = Bishop('white', 5)
		self.board[6] = Knight('white', 6)
		self.board[7] = Rook('white', 7)

		#add black pieces
		self.board[112] = Rook('black', 112)
		self.board[113] = Knight('black', 113)
		self.board[114] = Bishop('black', 114)
		self.board[115] = Queen('black', 115)
		self.board[116] = King('black', 116)
		self.board[117] = Bishop('black', 117)
		self.board[118] = Knight('black', 118)
		self.board[119] = Rook('black', 119)

		#add all pawns
		for i in range (128):
			if 16 <= i <= 23:
				self.board[i] = Pawn('white', i)

			elif 96 <= i <= 103:
				self.board[i] = Pawn('black', i)

	def move(self, location1, location2):
		piece1 = self.board[location1]
		piece2 = self.board[location2]
		if piece1 != None:
			if self.__selfTake(location1, location2) == True:
				if self.__offBoardCheck(location2) == True:
					print('checked pass 1')
					if piece1.character.lower() != 'p':
						if piece1.movePiece(location2) == True:
							print('checked pass 2')
							self.board[location2] = self.board[location1]
							self.board[location1] = None
							self.board[location2].location = location2
							self.print_board()
							self.attack_check(piece1,piece2)
							return True

					elif self.board[location1].character.lower() == 'p':
						if self.board[location1].movePiece(location2, self.board[location2]) == True:
							print('checked pass 2')
							self.board[location2] = self.board[location1]
							self.board[location1] = None
							self.board[location2].location = location2
							self.print_board()
							self.attack_check(piece1,piece2)
							return True

		print('Failed')
		self.print_board()
		return False

	def attack_check(piece1,piece2):
		if piece1.colour == piece2.colour:


	def __selfTake(self, location1, location2):
		if self.board[location1] != None:
			colour1 = self.board[location1].colour

		else:
			colour1 = None

		if self.board[location2] != None:
			colour2 = self.board[location2].colour

		else:
			colour2 = None

		if colour1 == None and colour2 == None:
			return True

		elif colour1 == colour2:
			print('self take error')
			return False

		else:
			return True

	def __offBoardCheck(self, hexsquare):
		if (hexsquare & 0x88) == 0:
			return True

		else:
			print('off board error')
			return False

	def print_board(self):
		print('board:')
		x = 0
		for i in range(8):
			out = []
			for j in range(16):
				try:
					out.append(self.board[x].character)
				except:
					out.append('o')
				x += 1
			print(out)

#player class
class player():
	def __init__(self):
		self.score = 0

#chess ai class
class computer(player):
	def __init__(self):
		player.__init__(self)
		pass

#Elo Calculation
def expectedScore(Ra, Rb):
	Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
	return Ea

def updateElo(Ra, Sa, Ea):
	NewRa = Ra + 34 *(Sa - Ea)
	return NewRa

def game():
	board = ChessBoard()
	board.print_board()
	board.move(0x10, 0x30)

if __name__ == '__main__':
	game()
