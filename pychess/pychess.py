import time
import os
import math

from misc import *
from score import *

#piece class
class Piece():
	def __init__(self, colour, location):
		self.colour = colour
		self.location = location
		self.ADSquares = []

	#diagonal sliding for queens and bishops

	def update_slide(self, location, direction, squares):
		location = location + direction
		if board1.offBoardCheck(location + direction) == True:
			if board1.board[location] == None:
				squares.append(location)
				self.update_slide(location, direction, squares)
			squares.append(location)

		return(squares)

	def id_direction(self, moved):
		if moved in self.ADSquares:
			direction = moved - self.location
			#help










			
			self.ADSquares = self.update_slide(self.location, direction, self.ADSquares)

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
	def __init__(self, colour, location ):
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
		print('checking for check')
		for i in board1.board:
			if i != None:
				if i.colour != self.colour:
					print(i.movePiece(self.location))
					if i.movePiece(self.location) == True:
						print('In check fail')
						return False

					else:
						print(str(type(i)) + ' cannot attack king')
		print('Check Check True')
		return True

	def update_ADSquares(self):
		print('\nupdating King')
		self.ADSquares = []
		directions = [-17, -16, -15, -1, 1, 15, 16, 17]
		for i in directions:
			self.ADSquares.append(self.location + i)

	def slide_check(self, location, direction):
		i = 0
		if board1.offBoardCheck(location) == True:
			print('a')
			if board1.board[location] != None:
				print('b')
				print(board1.board[location].colour)
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


class FEN:
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
class ChessBoard:
	def __init__(self):
		FEN_code = FEN()
		self.board = []

		self.Wking_location = 4
		self.Bking_location = 116

		self.board = FEN_code.load('standard')

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
			print('is sliding')
			self.slideLocations.pop(self.slideLocations.index(location1))
			self.slideLocations.append(piece.location)

		else:
			print('is not sliding')

	def move(self, location1, location2, colour):
		piece1 = self.board[location1]
		piece2 = self.board[location2]
		print(piece1.colour)
		if piece1 != None:
			if self.offBoardCheck(location2) == True:
				if piece1.colour == colour:
					if self.__selfTake(location1, location2) == True:
						print(piece1.ADSquares)
						if type(piece1) is not Pawn:
							if location2 in piece1.ADSquares:
								self.board[location2] = self.board[location1]
								self.board[location1] = None
								self.board[location2].location = location2
								self.board[location2].update_ADSquares()
								self.update_locations(self.board[location2], location1)
								print('slide locations:')
								print(self.slideLocations)
								for i in self.slideLocations:
									self.board[i].id_direction(location1)
									self.board[i].id_direction(location2)
								self.print_board()
								self.__write_board()
								self.__attack_check(piece1,piece2)
								return True

						else:
							if self.board[location2] == None:
								if piece1.movePawn(location2) == True:
									self.board[location2] = self.board[location1]
									self.board[location1] = None
									self.board[location2].location = location2
									self.board[location2].update_ADSquares()
									for i in self.slideLocations:
										self.board[i].id_direction(location1)
										self.board[i].id_direction(location2)
									self.print_board()
									self.__write_board()
									return True

								elif piece1.enPassant(location2) != 0:
									print('enPassant')
									take = piece1.enPassant(location2)
									self.board[take] = None
									self.board[location2] = self.board[location1]
									self.board[location1] = None
									self.board[location2].location = location2
									self.board[location2].update_ADSquares()
									for i in self.slideLocations:
										self.board[i].id_direction(location1)
										self.board[i].id_direction(location2)
									self.print_board()
									self.__write_board()
									self.__attack_check(piece1,piece2)
									return True

							else:
								print('attacking')
								print(piece1.ADSquares)
								print(location2)
								if location2 in piece1.ADSquares:
									self.board[location2] = self.board[location1]
									self.board[location1] = None
									self.board[location2].location = location2
									self.board[location2].update_ADSquares()
									for i in self.slideLocations:
										self.board[i].id_direction(location1)
										self.board[i].id_direction(location2)
									self.print_board()
									self.__write_board()
									self.__attack_check(piece1,piece2)
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
		if negcheck(hexsquare) == False:
			if (hexsquare & 0x88) == 0:
				return True

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

	def __write_board(self):
		print('writing')
		self.__clear_board()
		f = open('board.txt', 'a')
		for i in self.board:
			if i != None:
				f.write(i.character)

			else:
				f.write('o')
		f.close()
		print('written')

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
			if board1.move(location1, location2, self.colour) == False:
				self.turn()

			else:
				f = open('move.txt','w')
				f.write('complete')
				f.close()

		except:
			f = open('move.txt','w')
			f.write('listening')
			f.close()

#chess ai class
class computer(player):
	def __init__(self, colour):
		player.__init__(self)
		self.colour = colour

	def turn(self):
		pass

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

	def minimax(depth, node, maxing, values, max_depth):
		if depth == max_depth:
			return values[node]

		if maxing:
			return max(minimax(depth + 1, node * 2, False, values, max_depth),minimax(depth + 1, node * 2 + 1, False, values, max_depth))

		else:
			return min(minimax(depth + 1, node * 2, True, values, max_depth),minimax(depth + 1, node * 2 + 1, True, values, max_depth))

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

def game():
	global board1
	board1 = ChessBoard()
	board1.ADBoard_init()
	board1.print_board()
	valid = False
	global chessClock
	chessClock = clock(3600)
	while valid == False:
		menu = input('Input 1 to play against a player\nInput 2 to play against computer\n\n')
		if menu == '1':
			print('playing against human')
			player1 = human('white')
			player2 = human('black')
			end = False
			while end == False:
				player1.turn()
				player2.turn()
				#update_Data(chessClock)

		elif menu == '2':
			valid = True
			print('playing against computer')

		else:
			print('that is not an option')

if __name__ == '__main__':
	game()