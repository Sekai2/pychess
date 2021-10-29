import threading
from misc import *
from score import *
from gui import *

#piece class
class Piece():
	def __init__(self, colour, location):
		self.colour = colour
		self.location = location

	#diagonal sliding for queens and bishops
	def diagonal_check(self, location1, location2):
		if (location1 % 17 == location2 % 17):
			print('diagonal right')
			direction = 17

		elif (location1 % 15 == location2 % 15):
			print('diagonal left')
			direction = 15

		else:
			return False

		distance = board_rank(location2) - board_rank(location1)
		if negcheck(distance) == True:
			direction = -1 * (direction)

		blocked = False
		check_location = location1
		while blocked == False:
			check_location = check_location + direction
			print(check_location)

			if check_location == location2:
				return True

			elif board1.board[check_location] != None:
				return False

	def straight_check(self, location1, location2):
		if board_file(location1) == board_file(location2):
			print('verticle slide')
			distance = board_rank(location2) - board_rank(location1)
			print(distance)

			direction = 1

			if negcheck(distance) == True:
				direction = -1

			valid = True

			count = 0

			for i in range(abs(distance)-1):
				check_location = location1 + (i * direction * 16) + (16 * direction)
				print(check_location)

				if board1.board[check_location] == None:
					count += 1

			if count == abs(distance) -1:
				return True

			else:
				return False

		elif board_rank(location1) == board_rank(location2):
			print('horizontal slide')
			distance = board_file(location2) - board_file(location1)
			print(distance)

			direction = 1

			if negcheck(distance) == True:
				direction = -1

			valid = True

			count = 0

			for i in range(abs(distance)-1):
				check_location = location1 + (i * direction ) + ( direction)

				if board1.board[check_location] == None:
					count += 1

			if count == abs(distance) -1:
				return True

			else:
				return False

		else:
			return False

	def check():
		pass

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
		print('bishop selected')
		return self.diagonal_check(self.location, destination)

class Rook(Piece):
	def __init__(self, colour, location ):
		Piece.__init__(self, colour, location)
		self.value = 5
		self.character = 'R'

		if self.colour == 'white':
			self.character = self.character.lower()

	def movePiece(self, destination):
		print('Rook selected')
		return self.straight_check(self.location, destination)

class Queen(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 9
		self.character = 'Q'
		if self.colour == 'white':
			self.character = self.character.lower()

	def movePiece(self, destination):
		print('queen selected')
		print(self.diagonal_check(self.location, destination))
		if self.straight_check(self.location, destination) == True:
			return True

		elif self.diagonal_check(self.location, destination) == True:
			return True

		else:
			return False

class King(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 10000000
		self.character = 'K'
		if self.colour == 'white':
			self.character = self.character.lower()

	def movePiece(self, destination):
		print('king selected')
		if abs(board_file(destination) - board_file(self.location)) <= 1:
			if abs(board_rank(destination) - board_rank(self.location)) <= 1:
				return True

			else:
				return False

		else:
			return False

	def check_check(self):
		if self.slide_check(self.location, 16) == True:
			return True

	def slide_check(self, location, direction):
		i = 0
		if board1.offBoardCheck(location) == True:
			print('a')
			if board1.board[location] != None:
				print('b')
				if board1.board[location].colour != self.colour:
					print('c')
					if board1.board[location].movePiece(self.location) == True:
						return False

			else:
				print('c')
				next_location = location + direction
				self.check_straight(next_location, direction)

		else:
			print('c')
			return True




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

		self.Wking_location = 4
		self.Bking_location = 116
		#add all pawns and checkBoard
		for i in range (128):
			if 0x10 <= i <= 0x17:
				self.board[i] = Pawn('white', i)

			elif 0x60 <= i <= 0x67:
				self.board[i] = Pawn('black', i)

		#initial gui
		gui1 = gui()

	def move(self, location1, location2):
		piece1 = self.board[location1]
		piece2 = self.board[location2]
		if piece1 != None:
			if self.__selfTake(location1, location2) == True:
				if self.offBoardCheck(location2) == True:
					print('checked pass 1')
					if type(piece1) is not Pawn:
						if piece1.movePiece(location2) == True:

							print('checked pass 2')
							self.board[location2] = self.board[location1]
							self.board[location1] = None
							self.board[location2].location = location2
							if self.board[self.Wking_location].check_check() == True:
								print('not in check')
								self.print_board()
								self.__attack_check(piece1,piece2)
								return True
							else:
								self.board[location1] = self.board[location2]
								self.board[location2] = None
								self.board[location1].location = location1

					elif type(self.board[location1]) is Pawn:
						if self.board[location1].movePiece(location2, self.board[location2]) == True:
							print('checked pass 2')
							self.board[location2] = self.board[location1]
							self.board[location1] = None
							self.board[location2].location = location2
							self.print_board()
							self.__attack_check(piece1, piece2)
							return True

		print('Failed')
		self.print_board()
		return False

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

	def offBoardCheck(self, hexsquare):
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
					if self.board[x] == 'w' or self.board[x] == 'b':
						out.append(self.board[x])
					out.append(self.board[x].character)
				except:
					out.append('o')
				x += 1
			print(out)

	def __attack_check(self, piece1, piece2):
		if piece2 != None:
			score_change(piece1, piece2)

	def __attack_board(self,piece):
		colour = piece.colour[0]
		if type(piece) is Bishop:

			location = piece.position
			count = 0
			direction = 1
			diagonal = 15
			while count != 4:
				location = location + (direction * diagonal)
				if self.board[location] == None:
					self.board[location + 8] = colour

				else:
					count += 1
					location = piece.position
					if count == 1:
						direction = -1

					elif count == 2:
						direction = 1
						diagonal = 17

					elif count == 3:
						direction = -1
		#this bit need coding
				

		if type(piece) is Rook:
			
			location = piece.position
			count = 0
			direction = 1
			straight = 16
			while count != 4:
				location = location + (direction * straight)
				if self.board[location] == None:
					self.board[location + 8] = colour

				else:
					count +=1
					location = piece.position
					if count == 1:
						direction = -1

					elif count == 2:
						direction = 1
						straight = 1

					elif count == 3:
						direction = -1

#player class
class player():
	def __init__(self, colour):
		self.score = 0
		self.colour = colour

	def turn():
		pass


#chess ai class
class computer(player):
	def __init__(self):
		player.__init__(self)
		pass

def game():
	global board1
	board1 = ChessBoard()
	board1.print_board()
	board1.move(0x10, 0x30)
	board1.move(0x60, 0x40)
	board1.move(0x11, 0x31)
	board1.move(0x64, 0x44)
	board1.move(0x73, 0x55)
	board1.move(0x75, 0x42)
	board1.move(0x42, 0x15)

if __name__ == '__main__':
	game()
