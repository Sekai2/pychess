#miscellaneous functions

def negcheck(x):
	if x < 0:
		return True
	return False

def board_file(i):
	file = i & 7
	return file

def board_rank(i):
	rank = (i >> 4)
	return rank

def abs(x):
	if negcheck(x) == True:
		x = -1 * x
	return x

#piece class

#diagonal sliding for queens and bishops
def diagonal_check(location1, location2):
	if (location1 % 17 == location2 % 17):
		return 1

	elif (location1 % 15 == location2 % 15):
		return -1

#diagonal sliding for queens and rooks
def straight_check(location1, location2):
	if (board_file(location1) == board_file(location2)):
		if (board_rank(location1) == board_rank(location2)):
			return True

class Piece():
	def __init__(self, colour, location):
		self.colour = colour
		self.location = location

class Pawn(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 1
		self.character = 'P'
		if self.colour == 'white':
			self.character = self.character.lower()

	def movePiece(self, destination, objPiece):
		print('Pawn selected')
		if objPiece == None:
			if board_file(self.location) == board_file(self.location):
				if board_rank(self.location) == 1:
					if board_rank(destination) - board_rank(self.location) <= 2:
						return True

				elif board_rank(self.location) == 6:
					if board_rank(self.location) - board_rank(destination) <= 2:
						return True

				elif abs(board_rank(destination) - board_rank(self.location)) == 1:
					return True

				else:
					return False

		elif objPiece.colour != self.colour:
			if abs(board_rank(destination) - board_rank(self.location)) == 1:
				if abs(board_file(destination) - board_file(self.location)) == 1:
					return True

				else:
					return False

		else:
			return False

class Knight(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 3
		self.character = 'N'
		if self.colour == 'white':
			self.character = self.character.lower()

	def movePiece(self, destination):
		print('Knight selected')
		if (board_rank(destination) == board_rank(self.location) + 2) or (board_rank(destination) == board_rank(self.location) - 2):
			if (board_file(destination) == board_file(self.location) + 1) or (board_file(destination) == board_file(self.location) - 1):
				print('pass again')
				return True

		elif (board_rank(destination) == board_rank(self.location) + 1) or (board_rank(destination) == board_rank(self.location) - 1):
			if (board_file(destination) == board_file(self.location) + 2) or (board_file(destination) == board_file(self.location) - 2):
				print('pass again')
				return True

		else:
			return False

class Bishop(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 3
		self.character = 'B'
		if self.colour == 'white':
			self.character = self.character.lower()

	def movePiece(self, destination):
		pass

class Rook(Piece):
	def __init__(self, colour, location ):
		Piece.__init__(self, colour, location)
		self.value = 5
		self.character = 'R'
		if self.colour == 'white':
			self.character = self.character.lower()

	def movePiece(self, destination):
		pass

class Queen(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 9
		self.character = 'Q'
		if self.colour == 'white':
			self.character = self.character.lower()

	def movePiece(self, destination):
		pass

class King(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 10000000
		self.character = 'K'
		if self.colour == 'white':
			self.character = self.character.lower()

	def movePiece(self, destination):
		pass