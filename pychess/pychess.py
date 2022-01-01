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

		self.update_ADSquares()

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

	def update_slide(self, location, direction, squares, board):
		location = location + direction
		if board.offBoardCheck(location + direction) == True:
			if board1.board(location) == None:
				squares.append(location)
				self.update_slide(location, direction, squares)
			squares.append(location)

		return(squares)


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

	def update_ADSquares(self):
		if self.colour == 'white':
			direction = 1

		else:
			direction = -1

		self.ADSquares = [(self.location + (16*direction) - 1),(self.location + (16*direction) + 1)]

	def movePawn(self, destination):
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

	def update_ADSquares(self):
		print('updating Knight')
		self.ADSquares = []
		square_dif = [-33 ,-25 ,-18, -14, 14, 18, 25, 33]
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

	def movePiece(self, destination):
		print('bishop selected')
		return self.diagonal_check(self.location, destination)

	def update_ADSquares(self):
		self.ADSquares = []
		directions = [-17, -15, 15, 17]
		for i in directions:
			self.ADSquares = self.update_slide(self.location, i, self.ADSquares, board1)

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

	def update_ADSquares(self):
		self.ADSquares = []
		directions = [-16, -1, 1, 16]
		for i in directions:
			self.ADSquares = self.update_slide(self.location, i, self.ADSquares, board1)

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

	def update_ADSquares(self):
		self.ADSquares = []
		directions = [-17, -16, -15, -1, 1, 15, 16, 17]
		for i in directions:
			self.ADSquares = self.update_slide(self.location, i, self.ADSquares, board1)

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
		#	print(i)
			if i != None:
				#print(i)
		#		print(i.colour)
				if i.colour != self.colour:
		#			print(i)
					print(i.movePiece(self.location))
					if i.movePiece(self.location) == False:
						print('In check fail')
						return False

					else:
						print(str(type(i)) + ' cannot attack king')
		print('Check Check True')
		return True

	def update_ADSquares(self):
		self.ADSquares = []
		directions = [-17, -16, -15, -1, 1, 15, 16, 17]
		for i in directions:
			self.ADSquares.append(self.location + i)

#		if self.slide_check(self.location, 16) == True:
#			return True

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

		elif mode == 'default':
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
		pass

	def notate(self, board):
		pass

#Board Class
class ChessBoard:
	def __init__(self):
		self.board = []
		for i in range(128):
			self.board.append(None)

		#adding pieces

#		load_FEN('standard')
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

		self.__write_board()

#	def load_Fen(self, mode):
#		if mode == 'standard':
#			for i in FEN.standard:
#				if i == '/':
#					self.board.append(None)
#
#				elif i == ' ':
#					break
#
#				elif i == 'r':
#					self.board.append(Rook('black', 0))
#				elif i == 'n':
#					self.board.append(Rook('black', 0))

	# def move(self, location1, location2):
	# 	piece1 = self.board[location1]
	# 	piece2 = self.board[location2]
	# 	if piece1 != None:
	# 		if self.__selfTake(location1, location2) == True:
	# 			if self.offBoardCheck(location2) == True:
	# 				print('checked pass 1')
	# 				if type(piece1) is not Pawn:
	# 					if piece1.movePiece(location2) == True:
	# 						print('not pawn')

	# 						print('checked pass 2')
	# 						self.board[location2] = self.board[location1]
	# 						self.board[location1] = None
	# 						self.board[location2].location = location2
	# 						#print(self.board[self.Wking_location].check_check())
	# 						if self.board[self.Wking_location].check_check() == True:
	# 							if self.board[self.Bking_location].check_check() == True:
	# 								print('not in check')
	# 								self.print_board()
	# 								self.__attack_check(piece1,piece2)
	# 								self.__write_board()
	# 								return True

	# 							else:
	# 								print('in check')
	# 								self.board[location1] = self.board[location2]
	# 								self.board[location2] = None
	# 								self.board[location1].location = location1
	# 								return False

	# 						else:
	# 							print('in check')
	# 							self.board[location1] = self.board[location2]
	# 							self.board[location2] = None
	# 							self.board[location1].location = location1
	# 							return False

	# 				elif type(self.board[location1]) is Pawn:
	# 					if self.board[location1].movePiece(location2, self.board[location2]) == True:
	# 						print('checked pass 2')
	# 						self.board[location2] = self.board[location1]
	# 						self.board[location1] = None
	# 						self.board[location2].location = location2
	# 						self.print_board()
	# 						self.__write_board()
	# 						self.__attack_check(piece1, piece2)
	# 						return True

	def move(self, location1, location2):
		piece1 = self.board[location1]
		piece2 = self.board[location2]
		if piece1 != None:
			if self.offBoardCheck(location2) == True:
				if self.__selfTake(location1, location2) == True:
					print(piece1.ADSquares)
					if type(piece1) is not Pawn:
						if location2 in piece1.ADSquares:
							self.board[location2] = self.board[location1]
							self.board[location1] = None
							self.board[location2].location = location2
							self.print_board()
							self.__attack_check(piece1,piece2)
							self.__write_board()
							return True

					else:
						if self.board[location2] == None:
							if piece1.movePawn(location2) == True:
								self.board[location2] = self.board[location1]
								self.board[location1] = None
								self.board[location2].location = location2
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

			print(content)
			location1 = int(content[:4], base = 16)
			location2 = int(content[4:], base = 16)
			print(location2)
			if board1.move(location1, location2) == False:
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