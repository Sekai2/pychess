import time
import os
import math
import random

from misc import *
from score import *

#parent class for all piece types
class Piece():
	def __init__(self, colour, location):
		self.colour = colour
		self.location = location
		self.ADSquares = []
		self.hashval = 0

	#diagonal sliding for queens and bishops

	def clean(self):
		#deletes repeats from ADSquares
		for i in self.ADSquares:
			 if self.ADSquares.count(i) > 1:
			 	for j in range(self.ADSquares.count(i)-1):
			 		self.ADSquares.remove(i)

	def update_slide(self, location, direction, squares):

		#updates ADSqures for a single line/direction
		location = location + direction
		if board1.offBoardCheck(location) == True:
			if board1.board[location] == None:
				if location in squares:
					squares.remove(location)
				squares.append(location)
				self.update_slide(location, direction, squares)
			squares.append(location)

		return(squares)

	def id_direction(self, moved):
		#identifies the between piece and a location, used to identify direction that needs to be updated for a sliding piece
		if moved in self.ADSquares:
			direction = moved - self.location
			multiplier = direction // abs(direction)
			if abs(direction) < 7:
				direction = multiplier

			elif self.location % 16 == moved % 16:
				direction = 16
				direction = direction * multiplier

			elif self.location % 17 == moved % 17:
				direction = 17
				direction = direction * multiplier

			elif self.location % 15 == moved % 15:
				direction = 15
				direction = direction * multiplier

			return direction

	def block_update(self, location1, location2):
		print('block updating')
		#updates ADSquares for sliding pieces when blocking pieces are moved or pieces are moved into slide line
		if location2 in self.ADSquares:
			self.update_ADSquares()

		else:
			direction = self.id_direction(location1)
			if direction != None:
				self.ADSquares = self.update_slide(self.location, direction, self.ADSquares)

		self.clean()
		print('aaaaaaaa')

#Note: ADSqaures(variable) stores all the squares which a piece attacks
#      update_ADSquares(method) updates the ADSqaures for a piece
class Pawn(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 1
		self.character = 'P'
		if self.colour == 'white':
			self.character = self.character.lower()

	def update_ADSquares(self):
		print('updating pawn')
		if self.colour == 'white':
			direction = -1

		else:
			direction = 1

		self.ADSquares = [(self.location + (16*direction) - 1),(self.location + (16*direction) + 1)]

		

	def movePawn(self, destination):
		#pawn specific method for normal pawn movement
		if self.colour == 'white':
			if negcheck(self.location - destination) == True:
				return False

		if board_file(self.location) == board_file(destination):
			if board_rank(self.location) == 1:
				if board_rank(destination) - board_rank(self.location) <= 2:
					return True

			elif board_rank(self.location) == 6:
				if board_rank(self.location) - board_rank(destination) <= 2:
					return True

			elif abs(board_rank(destination) - board_rank(self.location)) == 1:
				return True

		return False

	def enPassant(self, destination):
		#pawn specific method for moving a pawn using the en passant rule
		print('enPassant check')
		if self.colour == 'white':
			rank = 3
			direction = -1

		if self.colour == 'black':
			rank = 4
			direction = 1

		adjacent = [self.location + 1, self.location -1]
		for i in adjacent:
			if board1.board[i].colour != self.colour:
				if type(board1.board[i]) == Pawn:
					if board_rank(self.location) == rank:
						if board_file(destination) == board_file(i):
							if destination == (i + 16 * direction):
								return i
		return 0


class Knight(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 3
		self.character = 'N'
		if self.colour == 'white':
			self.character = self.character.lower()

	def update_ADSquares(self):
		print('\nupdating Knight')
		self.ADSquares = []
		square_dif = [-33 ,-31 ,-18, -14, 14, 18, 31, 33]
		for i in square_dif:
			if board1.offBoardCheck(self.location + i) == True:
				self.ADSquares.append(self.location + i)

class Bishop(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 3
		self.character = 'B'
		if self.colour == 'white':
			self.character = self.character.lower()

	def update_ADSquares(self):
		print('\nupdating Bishop')
		self.ADSquares = []
		directions = [-17, -15, 15, 17]
		for i in directions:
			self.ADSquares = self.update_slide(self.location, i, self.ADSquares)

class Rook(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 5
		self.character = 'R'

		if self.colour == 'white':
			self.character = self.character.lower()

	def update_ADSquares(self):
		print('\nupdating Rook')
		self.ADSquares = []
		directions = [-16, -1, 1, 16]
		for i in directions:
			self.ADSquares = self.update_slide(self.location, i, self.ADSquares)

class Queen(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 9
		self.character = 'Q'
		if self.colour == 'white':
			self.character = self.character.lower()

	def update_ADSquares(self):
		print('\nupdating Queen')
		self.ADSquares = []
		directions = [-17, -16, -15, -1, 1, 15, 16, 17]
		for i in directions:
			self.ADSquares = self.update_slide(self.location, i, self.ADSquares)

class King(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 10000000
		self.character = 'K'
		self.Qcastling = True
		self.Kcastling = True
		if self.colour == 'white':
			self.character = self.character.lower()

	def update_ADSquares(self):
		print('\nupdating King')
		self.ADSquares = []
		directions = [-17, -16, -15, -1, 1, 15, 16, 17]
		for i in directions:
			if board1.offBoardCheck(self.location + i) == True:
				self.ADSquares.append(self.location + i)

class FEN():
	def __init__(self):
		self.standard = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
		self.quantity = 0

	def load(self,mode):
		if mode == 'file':
			file_name = input('Input the file name')
			f = open(file_name, 'r')
			FEN_code = f.read()
			if self.__verify(FEN_code) == True:
				board = self.__initiate(FEN_code)

			else:
				print('failed to load FEN code')
				return False

		elif mode == 'standard':
			board = self.__initiate(self.standard)

		elif mode == 'selfInput':
			FEN_code = input('Input valid FEN code')
			if self.__verify(FEN_code) == True:
				board = self.__initiate(FEN_code)

			else:
				print('failed to load FEN code')
				return False

		return board

	def __verify(self, FEN_code):
		dictionary = 'rnbqkpRNBQKP8- 01'
		valid_p = 'rnbqkRNBQKP'
		valid_c = 'KQkq'
		digits = '12345678'
		colour = 'wb'

		pointer = 0
		count = 0
		boardx = []
		boardy = []
		while FEN_code[pointer] != ' ':
			if FEN_code[pointer] == '/':
				if len(boardx) == 8:
					return False

			elif FEN_code[pointer] in digits:
				for i in int(FEN_code[pointer]):
					boardx.append(FEN_code[pointer])

			elif FEN_code[pointer] in valid_p:
				boardx.append(FEN_code[pointer])

			else:
				return False

		for i in range(13):
			if i == 1:
				if FEN_code[pointer + i] not in colour:
					return False

			elif i == 3:
				pass

			pointer += 1

	def __initiate(self, FEN_code):
		digits = '12345678'
		board = []
		for i in FEN_code:
			if i == '/':
				for i in range(8):
					board.append(None)
			elif i == 'r':
				board.append(Rook('black', (len(board))))
				self.quantity += 1

			elif i == 'n':
				board.append(Knight('black', (len(board))))
				self.quantity += 1

			elif i == 'b':
				board.append(Bishop('black', (len(board))))
				self.quantity += 1

			elif i == 'q':
				board.append(Queen('black', (len(board))))
				self.quantity += 1

			elif i == 'k':
				board.append(King('black', (len(board))))
				self.quantity += 1

			elif i == 'p':
				board.append(Pawn('black', (len(board))))
				self.quantity += 1

			elif i == 'R':
				board.append(Rook('white', (len(board))))
				self.quantity += 1

			elif i == 'N':
				board.append(Knight('white', (len(board))))
				self.quantity += 1

			elif i == 'B':
				board.append(Bishop('white', (len(board))))
				self.quantity += 1

			elif i == 'Q':
				board.append(Queen('white', (len(board))))
				self.quantity += 1

			elif i == 'K':
				board.append(King('white', (len(board))))
				self.quantity += 1

			elif i == 'Q':
				board.append(Queen('white', (len(board))))
				self.quantity += 1

			elif i == 'P':
				board.append(Pawn('white', (len(board))))
				self.quantity += 1

			elif i in digits:
				for j in range(int(i)):
					board.append(None)

			else:
				print(len(board))
				return(board)

	def notate(self, board):
		pass

#Board Class
class ChessBoard():
	def __init__(self, board):
		FEN_code = FEN()
		self.board = []

		self.Wking_location = 116
		self.Bking_location = 4


		if board == 'standard':
			self.board = FEN_code.load('standard')

		else:
			self.board = board

		self.slideLocations = []
		for i in self.board:
			if type(i) == Queen or type(i) == Bishop or type(i) == Rook:
				self.slideLocations.append(self.board.index(i))

		self.__write_board()

	def ADBoard_init(self):
		for i in self.board:
			if i != None:
				i.update_ADSquares()

	def update_locations(self, piece, location1):
		if type(piece) == Bishop or type(piece) == Rook or type(piece) == Queen:
			self.slideLocations.pop(self.slideLocations.index(location1))
			self.slideLocations.append(piece.location)

		if type(piece) == King:
			if piece.colour == 'white':
				self.Wking_location = piece.location

			elif piece.colour == 'black':
				self.Bking_location = piece.location

	def __checkCheck(self, piece):
		#initiating check for check
		if piece.colour == 'white':
			if self.Bking_location in piece.ADSquares:
				return 'black'

		else:
			if self.Wking_location in piece.ADSquares:
				return 'white'
		return False

	def __checkmateCheck(self, colour, piece):
		print('checking for Checkmate')
		if colour == 'white':
			king = self.board[self.Wking_location]

		else:
			king = self.board[self.Bking_location]

		kingSquares = king.ADSquares

		direction = piece.id_direction(king.location)

		inLineSquares = []
		inLineSquares = piece.update_slide(piece.location, direction, inLineSquares)

		for i in range(len(self.board)):
			if self.board[i] != None:
				if self.board[i].colour != king.colour:
					for j in king.ADSquares:
						if j in self.board[i].ADSquares:
							kingSquares.remove(j)

						elif len(kingSquares) == 0:
							for p in i.ADSquares:
								if p in inLineSquares:
									return False
							return True

				else:
					if i in kingSquares:
						kingSquares.remove(i)

					for p in i.ADSquares:
						if p in inLineSquares:
							return False


		if len(kingSquares) == 0:
			return True

		return False

	def __revert(self, location1, location2, piece2):
		print('reverting')
		self.board[location1] = self.board[location2]
		self.board[location1].location = location1
		self.board[location2] = piece2
		if self.board[location2] != None:
			self.board[location2].location = location2
		self.board[location1].update_ADSquares()
		self.update_locations(self.board[location1], location2)
		for i in self.slideLocations:
			self.board[i].block_update(location2, location1)

	def __update_Board(self, location1, location2, colour, piece1, piece2):
		self.board[location2] = self.board[location1]
		self.board[location1] = None
		self.board[location2].location = location2
		self.board[location2].update_ADSquares()
		self.update_locations(self.board[location2], location1)

		if type(piece1) == King:
			self.board[location2].Kcastling = False
			self.board[location2].Qcastling = False
			#updating king index

		for i in self.slideLocations:
			self.board[i].block_update(location1, location2)
			squares = []
			for i in self.board[i].ADSquares:
				squares.append(file_letter(i) + rank_num(i))

		if colour == 'white':
			if self.Bking_location in self.board[location2].ADSquares:
				if self.__checkmateCheck(colour) == True:
					print('checkmate')
					return('checkmate')

		elif colour == 'black':
			if self.Wking_location in self.board[location2].ADSquares:
				if self.__checkmateCheck(colour) == True:
					print('checkmate')
					return('checkmate')

		for i in self.board:
			if i != None:
				if self.__checkCheck(i) == colour:
					print(' in check')
					if self.__checkmateCheck(colour, i) == True:
						print('checkmate')
						return('checkmate')
					self.__revert(location1, location2, piece2)
					print('returning false')
					return False

		#updating castling ability
		if piece1.colour == colour:
			if type(piece1) == Rook:
				if piece1.colour == 'white':
					if location1 == 112:
						self.board[self.Wking_location].Qcastling = False

					elif location1 == 119:
						self.board[self.Wking_location].Kcastling = False

				elif piece1.colour == 'black':
					if location1 == 0:
						self.board[self.Bking_location].Qcastling = False

					elif location1 == 7:
						self.board[self.Bking_location].Kcastling = False

			if type(piece2) == Rook:
				if piece1.colour == 'white':
					if location2 == 112:
						self.board[self.Wking_location].Qcastling = False

					elif location2 == 119:
						self.board[self.Wking_location].Kcastling = False

				elif piece1.colour == 'black':
					if location2 == 0:
						self.board[self.Bking_location].Qcastling = False

					elif location2 == 7:
						self.board[self.Bking_location].Kcastling = False

		self.__write_board()
		#self.__attack_check(piece1,piece2)
		return True

	def castle(self, piece, location2):
		if piece.colour == 'white':
			if location2 == 0x72:
				if piece.Qcastling == True:
					if piece.location in self.board[112].ADSquares:
						if self.__update_castle(0x72, 0x70, 0x73, 'white') == True:
							return True

			elif location2 == 0x76:
				if piece.Kcastling == True:
					if piece.location in self.board[119].ADSquares:
						if self.__update_castle(0x76, 0x77, 0x75, 'white') == True:
							return True

		elif piece.colour == 'black':
			if location2 == 0x02:
				if piece.Qcastling == True:
					if piece.location in self.board[0].ADSquares:
						if self.__update_castle(0x02, 0x00, 0x03, 'black') == True:
							return True

			elif location2 == 0x06:
				if piece.Kcastling == True:
					if piece.location in self.board[7].ADSquares:
						if self.__update_castle(0x06, 0x07, 0x05, 'black') == True:
							return True
		return False

	def __update_castle(self, Klocation, Rlocation1, Rlocation2, colour):
		if colour == 'white':
			Klocation1 = self.Wking_location
			self.Wking_location = Klocation

		else:
			Klocation1 = self.Bking_location
			self.Bking_location = Klocation

		self.board[Klocation] = self.board[Klocation1]
		self.board[Klocation1] = None
		self.board[Klocation].location = Klocation
		self.board[Rlocation2] = self.board[Rlocation1]
		self.board[Rlocation1] = None
		self.board[Rlocation2].location = Rlocation2
		self.board[Klocation].update_ADSquares()
		self.board[Rlocation2].update_ADSquares()

		self.update_locations(self.board[Rlocation2], Rlocation1)

		for i in self.slideLocations:
			self.board[i].block_update(Rlocation1, Rlocation2)
			self.board[i].block_update(Klocation1, Klocation)

		for i in self.board:
			if i != None:
				if self.__checkCheck(i) == self.board[Klocation].colour:
					if self.__checkmateCheck(colour):
						return 'checkmate'
					self.__revert_castle(Klocation, Rlocation1, Rlocation2)
					return False
		self.__write_board()
		return True

	def __revert_castle(self, Klocation, Rlocation1, Rlocation2):
		if self.board[Klocation].colour == 'white':
			location = 116
			self.Wking_location = 116

		else:
			location = 4
			self.Bking_location = 4

		self.board[location] = self.board[Klocation]
		self.board[Klocation] = None
		self.board[location].location = location
		self.board[Rlocation1] = self.board[Rlocation2]
		self.board[Rlocation2] = None
		self.board[Rlocation1].location = Rlocation1
		self.board[location].update_ADSquares()
		self.board[Rlocation1].update_ADSquares()
		self.update_locations(self.board[Rlocation1], Rlocation2)
		for i in self.slideLocations:
			self.board[i].block_update(Rlocation2, Rlocation1)
			self.board[i].block_update(location, Klocation)

	def move(self, location1, location2, colour):
		piece1 = self.board[location1]
		piece2 = self.board[location2]

		if piece1 != None:
			if self.offBoardCheck(location2) == True:
				if piece1.colour == colour:
					if self.__selfTake(location1, location2) == True:
						if type(piece1) is not Pawn:
							if type(piece1) == King:
								if location2 in piece1.ADSquares:
									return self.__update_Board(location1, location2, colour, piece1, piece2)

								else:
									return self.castle(piece1, location2)

							elif location2 in piece1.ADSquares:
								return self.__update_Board(location1, location2, colour, piece1, piece2)

						else:
							if self.board[location2] == None:
								if piece1.movePawn(location2) == True:
									return self.__update_Board( location1, location2, colour, piece1, piece2)

								elif piece1.enPassant(location2) != 0:
									take = piece1.enPassant(location2)
									self.board[take] = None
									return self.__update_Board(location1, location2, colour, piece1, piece2)

							else:
								if location2 in piece1.ADSquares:
									return self.__update_Board(location1, location2, colour, piece1, piece2)
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
			return False

		else:
			return True

	def offBoardCheck(self, hexsquare):
		if negcheck(hexsquare) == False:
			if (hexsquare & 0x88) == 0:
				return True
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

	def __write_board(self):
		self.__clear_board()
		f = open('board.txt', 'a')
		for i in self.board:
			if i != None:
				f.write(i.character)

			else:
				f.write('o')
		f.close()

	def __clear_board(self):
		f = open('board.txt', 'w')
		f.write('')
		f.close()


	def __attack_check(self, piece1, piece2):
		if piece2 != None:
			score_change(piece1, piece2)

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
	def __init__(self):
		self.score = 0

	def turn():
		pass

class human(player):
	def __init__(self, colour):
		player.__init__(self)
		self.colour = colour

	def turn(self):
		print(self.colour + '\'s turn')
		f = open('move.txt','w')
		f.write('listening')
		f.close()
		f = open('move.txt','r')
		content = f.read()
		f.close()
		try:
			while content == 'listening' or content == '':
				f = open('move.txt','r')
				content = f.read()
			f.close()

			print('contents is: ')
			print(content)
			location1 = int(content[:4], base = 16)
			location2 = int(content[4:], base = 16)
			print(location1)
			print(location2)
			moveResult = board1.move(location1, location2, self.colour)
			if moveResult == False:
				print('wrong move')
				self.turn()

			elif moveResult == 'checkmate':
				return True

			else:
				print('turn over')
				f = open('move.txt','w')
				f.write('complete')
				f.close()

		except:
			f = open('move.txt','w')
			f.write('listening')
			f.close()

#node class for min max tree
class node():
	def __init__(self, val):
		self.val = val
		self.children = []
		self.hash = None
		self.visited = False

	def append(self, child):
		self.children.append(child)

	def generate(self, colour):
		for i in self.val:
			if i != None:
				if i.colour == colour:
					if type(i) == Pawn:
						tempBoard = self.val
						if tempBoard.move(i.location, i.location + 16, colour) == True:
							self.append(tempBoard.board)

						tempBoard = self.val
						if tempBoard.move(i.location, i.location + 32, colour) == True:
							self.append(tempBoard.board)

					elif type(i) == King:
						for j in i.ADSquares:
							tempBoard = self.val
							if tempBoard.move(i.location, j, colour) == True:
								self.append(tempBoard.board)

						if i.colour == 'white':
							if i.location == 116:
								if i.Qcastling == True:
									tempBoard = self.val
									if tempBoard.move(116, 114, colour) == True:
										self.append(tempBoard.board)

								if i.Kcastling == True:
									tempBoard = self.val
									if tempBoard.move(116, 118, colour) == True:
										self.append(tempBoard.board)

						if i.colour == 'black':
							if i.location == 4:
								if i.Qcastling == True:
									tempBoard = self.val
									if tempBoard.move(4, 2, colour) == True:
										self.append(tempBoard.board)

								if i.Kcastling == True:
									tempBoard = self.val
									if tempBoard.move(4, 2, colour) == True:
										self.append(tempBoard.board)


					else:
						for j in i.ADSquares:
							tempboard = self.val
							if tempBoard.move(i.location, j, colour) == True:
								self.append(tempBoard.board)

#chess ai class
class computer(player):
	def __init__(self, colour):
		player.__init__(self)
		self.colour = colour
		self.max_depth = 2

	def turn(self):
		rootNode = node(board1.board)
		grow(rootNode, 0, max_depth,self.colour)
		minimax(self, 1, rootNode, 0, self.max_depth, False, self.colour)

	def evaluate(self):
		if self.colour == 'white':
			multiplier = 1

		elif self.colour == 'black':
			multiplier = -1

		materialScore = materialEval()
		mobilityScore = mobilityEval()
		score = (materialScore + mobilityScore) * multiplier

	def materialEval(self):
		pass

	def mobilityEval(self):
		pass

#	def minimax(depth, node, maxing, values, max_depth):
#		if depth == max_depth:
#			return values[node]
#
#		if maxing:
#			return max(minimax(depth + 1, node * 2, False, values, max_depth),minimax(depth + 1, node * 2 + 1, False, values, max_depth))
#
#		else:
#			return min(minimax(depth + 1, node * 2, True, values, max_depth),minimax(depth + 1, node * 2 + 1, True, values, max_depth))

	def grow(self, node, depth, max_depth, colour):
		if node == max_depth:
			return

		else:
			node.generate(colour)
			if colour == 'white':
				colour = 'black'

			else:
				colour = 'white'
			for i in currentNode.children:
				grow(i, depth + 1, max_depth, colour)


class clock():
	def __init__(self, timer):
		self.start_time = time.time()
		self.end_time = time.time() + timer
		self.time = 0

	def update(self):
		raw = self.end_time - (time.time - start_time)
		minutes = raw // 60
		seconds = raw % 60

		self.time = minutes + (seconds * 0.01)
		return self.time

def update_Data(clock):
	f = open('UCode.txt','a')
	f.write(clock.update())
	f.close()

def endGame(colour):
	print('Checkmate')
	if colour == 'white':
		colour = 'Black'

	else:
		colour = 'White'

	print(colour + ' wins!')

	quit()

def game():
	global board1
	board1 = ChessBoard('standard')
	board1.ADBoard_init()
	board1.print_board()
	valid = False
	global chessClock
	chessClock = clock(3600)
	while valid == False:
		menu = input('Input 1 to play against a player\nInput 2 to play against computer\n\n')
		if menu == '1':
			valid = True
			print('playing against human')
			player1 = human('white')
			player2 = human('black')
			end = False
			endColour = 'white'
			while end != True:
				end = player1.turn()
				if end != True:
					end = player2.turn()

				else:
					endColour = 'black'
				#update_Data(chessClock)

			endGame(endColour)

		elif menu == '2':
			valid = True
			print('playing against computer')
			loop = True
			colour = input('Select your side w/b:\n')
			while loop == True:
				try:
					print('testing')
					if colour.lower == 'w':
						loop = False
						print('Playing as white')
						colour1 = 'white'
						colour2 = 'black'

					elif colour.lower == 'b':
						loop = False
						print('Playing as black')
						colour1 = 'black'
						colour2 = 'white'

					else:
						print('a')
						print('That is not an option')

				except:
					print('b')
					print('That is not an option')

				player1 = human(colour1)
				player2 = computer(colour2)
				end = False
				endColour = 'white'
				while end != True:
					end = player1.turn()
					if end != True:
						end = player2.turn()

					else:
						endColour = 'black'

				endGame(endColour)


		else:
			print('that is not an option')

if __name__ == '__main__':
	game()
