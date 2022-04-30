#main python code

import time
import math
import copy
import random
import subprocess
import threading
import json

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import sqlite3

from misc import *
from score import *
from PRNG import *
from zorbristHash import *
from evaluate import *
from passwordHash import *
from saving import *

#parent class for all piece types
class Piece():
	def __init__(self, colour, location):
		self.colour = colour
		self.location = location
		self.ADSquares = []
		self.hashval = 0

	def clean(self):
		#deletes repeats from ADSquares
		for i in self.ADSquares:
			 if self.ADSquares.count(i) > 1:
			 	for j in range(self.ADSquares.count(i)-1):
			 		self.ADSquares.remove(i)

	def update_slide(self, location, direction, squares, chessBoard):

		#updates ADSqures for a single line/direction
		location = location + direction
		if chessBoard.offBoardCheck(location) == True:
			if chessBoard.board[location] == None:
				if location in squares:
					squares.remove(location)
				squares.append(location)
				self.update_slide(location, direction, squares, chessBoard)
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

	def block_update(self, location1, location2, chessBoard):
		#updates ADSquares for sliding pieces when blocking pieces are moved or pieces are moved into slide line
		if location2 in self.ADSquares:
			self.update_ADSquares(chessBoard)

		else:
			direction = self.id_direction(location1)
			if direction != None:
				self.ADSquares = self.update_slide(self.location, direction, self.ADSquares, chessBoard)

		self.clean()

#Note: ADSqaures(variable) stores all the squares which a piece attacks
#      update_ADSquares(method) updates the ADSqaures for a piece
class Pawn(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 1
		self.character = 'P'
		self.double_move = False
		if self.colour == 'black':
			self.character = self.character.lower()

	def update_ADSquares(self, chessBoard):
		if self.colour == 'white':
			direction = -1

		else:
			direction = 1

		square1 = self.location + (16*direction) - 1
		square2 = self.location + (16*direction) + 1

		self.ADSquares = []
		if chessBoard.offBoardCheck(square1) == True:
			self.ADSquares.append(square1)

		if chessBoard.offBoardCheck(square2) == True:
			self.ADSquares.append(square2)

	def movePawn(self, destination):
		#pawn specific method for normal pawn movement
		if self.colour == 'white':
			if negcheck(self.location - destination) == True:
				return False

		elif self.colour == 'black':
			if negcheck(self.location - destination) == False:
				return False

		if board_file(self.location) == board_file(destination):
			if board_rank(self.location) == 1:
				if board_rank(destination) - board_rank(self.location) <= 2:
					if board_rank(destination) - board_rank(self.location) == 2:
						self.double_move = True
					return True

			elif board_rank(self.location) == 6:
				if board_rank(self.location) - board_rank(destination) <= 2:
					if board_rank(self.location) - board_rank(destination) == 2:
						self.double_move = True
					return True

			elif abs(board_rank(destination) - board_rank(self.location)) == 1:
				return True

		return False

	def enPassant(self, destination, chessBoard):
		#pawn specific method for moving a pawn using the en passant rule
		if self.colour == 'white':
			rank = 3
			direction = -1

		elif self.colour == 'black':
			rank = 4
			direction = 1

		target = 0

		adjacent = [self.location + 1, self.location - 1]
		for i in adjacent:
			if board_file(i) == board_file(destination):
				if board_rank(i) == board_rank(self.location):
					target = i

		if chessBoard.board[target] == None:
			return 0

		if board_rank(destination) == board_rank(self.location) + direction:
			if chessBoard.board[target].colour != self.colour:
				if type(chessBoard.board[target]) == Pawn:
					if chessBoard.board[target].double_move == True:
						if board_rank(self.location) == rank:
							if destination == (target + 16 * direction):
								return i
		return 0


class Knight(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 3
		self.character = 'N'
		if self.colour == 'black':
			self.character = self.character.lower()

	def update_ADSquares(self, chessBoard):
		self.ADSquares = []
		square_dif = [-33 ,-31 ,-18, -14, 14, 18, 31, 33]
		for i in square_dif:
			if chessBoard.offBoardCheck(self.location + i) == True:
				self.ADSquares.append(self.location + i)

class Bishop(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 3
		self.character = 'B'
		if self.colour == 'black':
			self.character = self.character.lower()

	def update_ADSquares(self, chessBoard):
		self.ADSquares = []
		directions = [-17, -15, 15, 17]
		for i in directions:
			self.ADSquares = self.update_slide(self.location, i, self.ADSquares, chessBoard)

class Rook(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 5
		self.character = 'R'

		if self.colour == 'black':
			self.character = self.character.lower()

	def update_ADSquares(self, chessBoard):
		self.ADSquares = []
		directions = [-16, -1, 1, 16]
		for i in directions:
			self.ADSquares = self.update_slide(self.location, i, self.ADSquares, chessBoard)

class Queen(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 9
		self.character = 'Q'
		if self.colour == 'black':
			self.character = self.character.lower()

	def update_ADSquares(self, chessBoard):
		self.ADSquares = []
		directions = [-17, -16, -15, -1, 1, 15, 16, 17]
		for i in directions:
			self.ADSquares = self.update_slide(self.location, i, self.ADSquares, chessBoard)

class King(Piece):
	def __init__(self, colour, location):
		Piece.__init__(self, colour, location)
		self.value = 10000000
		self.character = 'K'
		self.Qcastling = False
		self.Kcastling = False
		if self.colour == 'black':
			self.character = self.character.lower()

	def update_ADSquares(self, chessBoard):
		self.ADSquares = []
		directions = [-17, -16, -15, -1, 1, 15, 16, 17]
		for i in directions:
			if chessBoard.offBoardCheck(self.location + i) == True:
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
		copyFEN = FEN_code
		populateBoard = True
		count = 0
		self.Wking_location = 116
		self.Bking_location = 4
		self.fullmove_clock = ''
		self.halfmove_clock = ''
		doublePawnLocation = ''

		for i in FEN_code:
			#print(i)
			if populateBoard == True:
				if i == ' ':
					for i in range(8):
						board.append(None)
						populateBoard = False
						castling = True

				elif i == '/':
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
					self.Bking_location = len(board) - 1

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
					self.Wking_location = len(board) - 1

				elif i == 'Q':
					board.append(Queen('white', (len(board))))
					self.quantity += 1

				elif i == 'P':
					board.append(Pawn('white', (len(board))))
					self.quantity += 1

				elif i in digits:
					for j in range(int(i)):
						board.append(None)

			elif castling == True:
				if i == 'K':
					board[self.Wking_location].Kcastling = True

				elif i == 'Q':
					board[self.Wking_location].Qcastling = True

				elif i == 'k':
					board[self.Bking_location].Kcastling = True

				elif i == 'q':
					board[self.Bking_location].Qcastling = True

				elif count == 1:
					castling = False
					doubleMove = True

				elif i == ' ':
					count += 1

			elif doubleMove == True:
				if len(doublePawnLocation) < 3:
					if i != '-':
						doublePawnLocation += i

					elif i == '-':
						doubleMove = False

				elif i == ' ':
					doubleMove = False

			else:
				self.halfmove_clock = int(FEN_code[-3])
				self.fullmove_clock = int(FEN_code[-1])
			
		return(board)

	def notate(self, board, turn):
		count = 0
		FEN_code = ''
		enPassant_location = None
		halfmove_clock = board.halfmove_clock
		fullmove_clock = board.fullmove_clock
		for i in range(len(board.board)):
			if i % 16 < 8:
				if count != 0:
					if board.board[i] != None:
						FEN_code += str(count)
						count = 0
						FEN_code += board.board[i].character

					else:
						count += 1

				elif board.board[i] == None:
					count = 1

				else:
					FEN_code += board.board[i].character
					if type(board.board[i]) == Pawn:
						if board.board[i].double_move == True:
							if board.board[i].colour == 'white':
								location = i + 16

							else:
								location = i - 16

							#enPassant_location = file_letter(location) + rank_num(location)

			elif i % 16 == 8:
				if count != 0:
					FEN_code += str(count)
					count = 0
				FEN_code += '/'

		FEN_code = FEN_code[:-1]

		FEN_code += ' '

		if turn == 'black':
			FEN_code += 'b '

		else:
			FEN_code += 'w '

		if board.board[board.Wking_location].Kcastling == True:
			FEN_code += 'K'

		if board.board[board.Wking_location].Qcastling == True:
			FEN_code += 'Q'

		if board.board[board.Bking_location].Kcastling == True:
			FEN_code += 'k'

		if board.board[board.Bking_location].Qcastling == True:
			FEN_code += 'q'

		FEN_code += ' '

		if enPassant_location != None:
			FEN_code += enPassant_location

		else:
			FEN_code += '- '

		FEN_code += str(halfmove_clock)

		FEN_code += ' '

		FEN_code += str(fullmove_clock)

		return FEN_code

#Board Class
class ChessBoard():
	def __init__(self, board):
		FEN_code = FEN()
		self.board = []

		self.Wking_location = 116
		self.Bking_location = 4

		self.fullmove_clock = 1
		self.halfmove_clock = 0

		if board == 'standard':
			self.board = FEN_code.load('standard')

		elif type(board) == list:
			self.board = board

		else:
			self.board = FEN_code.__initiate(board)

		self.Wking_location = FEN_code.Wking_location
		self.Bking_location = FEN_code.Bking_location
		self.fullmove_clock = FEN_code.fullmove_clock
		self.halfmove_clock = FEN_code.halfmove_clock

		self.slideLocations = []
		for i in self.board:
			if type(i) == Queen or type(i) == Bishop or type(i) == Rook:
				self.slideLocations.append(self.board.index(i))

		self.materialCount = countMaterial(self.board)

		self.write_board()

	def ADBoard_init(self):
		for i in self.board:
			if i != None:
				i.update_ADSquares(self)

	def update_locations(self, piece, location1):
		if piece.location in self.slideLocations:
			self.slideLocations.remove(piece.location)

		if type(piece) == Bishop or type(piece) == Rook or type(piece) == Queen:
			self.slideLocations.pop(self.slideLocations.index(location1))
			self.slideLocations.append(piece.location)

		elif type(piece) == King:
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
		if colour == 'white':
			king = self.board[self.Bking_location]
			colour = 'black'

		else:
			king = self.board[self.Wking_location]
			colour = 'white'

		kingSquares = king.ADSquares

		direction = piece.id_direction(king.location)

		inLineSquares = []
		inLineSquares = piece.update_slide(piece.location, direction, inLineSquares, self)
		temp = []
		for i in inLineSquares:
			if i not in temp:
				temp.append(i)

			else:
				inLineSquares.remove(i)

		for i in range(len(self.board)):
			if self.board[i] != None:
				if self.board[i].colour != king.colour:
					if type(self.board[i]) != Pawn:
						for j in king.ADSquares:
							if j in self.board[i].ADSquares:
								if j in kingSquares:
									kingSquares.remove(j)

					else:
						for j in king.ADSquares:
							if self.board[i].colour == 'white':
								if board_rank(i) != 7:
									if i + 15 in kingSquares:
										kingSquares.remove(i + 15)

									if i + 17 in kingSquares:
										kingSquares.remove(i + 17)

							elif self.board[i].colour == 'black':
								if board_rank(i) != 0:
									if i - 15 in kingSquares:
										kingSquares.remove(i - 15)

									if i - 17 in kingSquares:
										kingSquares.remove(i - 17)

				else:
					if i in kingSquares:
						kingSquares.remove(i)

					if type(self.board[i]) == Pawn:
						if self.board[i].colour == 'white':
							for t in self.board[i].ADSquares:
								if t == piece.location and self.move(self.board[i].location, t, colour, True) == True:
										return False

								else:
									if (i - 16) in inLineSquares:
										if self.move(self.board[i].location, i - 16, colour, True):
											return False


						elif self.board[i].colour == 'black':
							for t in self.board[i].ADSquares:
								if t == piece.location and self.move(self.board[i].location, t, colour, True) == True:
										return False

								else:
									if (i + 16) in inLineSquares and self.move(self.board[i].location, i + 16, colour, True):
										return False

					for p in self.board[i].ADSquares:
						if p in inLineSquares or p == piece.location:
							if self.move(self.board[i].location, p, colour, True) == True:
								return False

		if len(kingSquares) == 0:
			return True

		return False

	def final_update(self, colour, piece):
		pass

	def __choose_piece_change(self, colour, location):
		f = open('move.txt', 'w')
		if colour == 'white':
			f.write('chooseWhite')
			print('wrote')

		elif colour == 'black':
			f.write('chooseBlack')

		f.close()

		valid = 'NBRQ'

		transform = 'a'
		while transform not in valid:
			time.sleep(0.001)
			f = open('move.txt', 'r')
			transform = f.read()
			f.close()

		if transform == 'N':
			piece = Knight(colour, location)

		elif transform == 'B':
			piece = Bishop(colour, location)

		elif transform == 'R':
			piece = Rook(colour, location)

		elif transform == 'Q':
			piece = Queen(colour, location)

		return piece


	def __revert(self, location1, location2, piece2):
		self.board[location1] = self.board[location2]
		self.board[location1].location = location1
		self.board[location2] = piece2

		if self.board[location2] != None:
			self.board[location2].location = location2
		self.board[location1].update_ADSquares(self)
		self.update_locations(self.board[location1], location2)

		if type(piece2) == Bishop or type(piece2) == Rook or type(piece2) == Queen:
			self.slideLocations.append(location2)

		for i in self.slideLocations:
			self.board[i].block_update(location2, location1, self)

	def __update_Board(self, location1, location2, colour, piece1, piece2, stop_rvt):
		if type(piece1) == Pawn:
			if piece1.colour == 'white':
				OpRank = 0

			elif piece1.colour == 'black':
				OpRank = 7

			if board_rank(location2) == OpRank:
				print('changing')
				self.board[location2] = self.__choose_piece_change(colour, location2)
				print('piece selected')
				self.__updatePieceCount(self.board[location1])
				self.board[location1] = None
				self.board[location2].location = location2
				self.board[location2].update_ADSquares(self)
				if type(self.board[location2]) != Knight:
					self.slideLocations.append(location2)
				self.update_locations(self.board[location2], location1)
				self.__updatePieceCountNew(self.board[location2])

			else:
				self.board[location2] = self.board[location1]
				self.board[location1] = None
				self.board[location2].location = location2
				self.board[location2].update_ADSquares(self)
				self.update_locations(self.board[location2], location1)

		else:
			self.board[location2] = self.board[location1]
			self.board[location1] = None
			self.board[location2].location = location2
			self.board[location2].update_ADSquares(self)
			self.update_locations(self.board[location2], location1)

		if type(piece1) == King:
			self.board[location2].Kcastling = False
			self.board[location2].Qcastling = False
			#updating king index

		for i in self.slideLocations:
			self.board[i].block_update(location1, location2, self)

		if colour == 'white':
			if self.Bking_location in self.board[location2].ADSquares:
				if self.__checkmateCheck(colour, self.board[location2]) == True:
					return('checkmate')

			else:
				for i in self.board:
					if i != None:
						if type(i) == Pawn:
							if i.location != location2:
								i.double_move = False
						checkResult = self.__checkCheck(i)
						if checkResult == colour:
							if stop_rvt == True:
								return False
							self.__revert(location1, location2, piece2)
							return False

						elif checkResult != colour and checkResult != False:
							if self.__checkmateCheck(colour, i) == True:
								return('checkmate')

		elif colour == 'black':
			if self.Wking_location in self.board[location2].ADSquares:
				if self.__checkmateCheck(colour, self.board[location2]) == True:
					return('checkmate')

			else:
				for i in self.board:
					if i != None:
						if type(i) == Pawn:
							if i.location != location2:
								i.double_move = False
						checkResult = self.__checkCheck(i)
						if checkResult == colour:
							if stop_rvt == True:
								return False
							self.__revert(location1, location2, piece2)
							return False

						elif checkResult != colour and checkResult != False:
							if self.__checkmateCheck(colour, i) == True:
								return('checkmate')

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
		self.board[Klocation].update_ADSquares(self)
		self.board[Rlocation2].update_ADSquares(self)

		self.update_locations(self.board[Rlocation2], Rlocation1)

		for i in self.slideLocations:
			self.board[i].block_update(Rlocation1, Rlocation2, self)
			self.board[i].block_update(Klocation1, Klocation, self)

		for i in self.board:
			if i != None:
				if self.__checkCheck(i) == self.board[Klocation].colour:
					if self.__checkmateCheck(colour):
						return 'checkmate'
					self.__revert_castle(Klocation, Rlocation1, Rlocation2)
					return False
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
		self.board[location].update_ADSquares(self)
		self.board[Rlocation1].update_ADSquares(self)
		self.update_locations(self.board[Rlocation1], Rlocation2)
		for i in self.slideLocations:
			self.board[i].block_update(Rlocation2, Rlocation1, self)
			self.board[i].block_update(location, Klocation, self)

	def move(self, location1, location2, colour, revert):
		piece1 = self.board[location1]
		piece2 = self.board[location2]

		if piece1 != None:
			if self.offBoardCheck(location2) == True:
				if piece1.colour == colour:
					if self.__selfTake(location1, location2) == True:
						if type(piece1) is not Pawn:
							if type(piece1) == King:
								if location2 in piece1.ADSquares:
									result =  self.__update_Board(location1, location2, colour, piece1, piece2, revert)
									if revert == True:
										self.__revert(location1, location2, piece2)

									if result == True and revert == False:
										if piece2 != None:
											self.halfmove_clock = 0
											self.__updatePieceCount(piece2)

										elif type(piece1) == Pawn:
											self.halfmove_clock = 0

										else:
											self.halfmove_clock += 1
 
										if colour == 'black':
											self.fullmove_clock += 1

										if self.halfmove_clock == 50:
											result = 'end'

									return result

								else:
									if revert == True:
										result = self.castle(piece1, location2)
									
									else:
										result = self.castle(piece1, location2)

									if result == True and revert == False:
										if piece2 != None:
											self.halfmove_clock = 0
											self.__updatePieceCount(piece2)

										elif type(piece1) == Pawn:
											self.halfmove_clock = 0

										else:
											self.halfmove_clock += 1

										if colour == 'black':
											self.fullmove_clock += 1

										if self.halfmove_clock == 50:
											result = 'end'
									
									return result

							elif location2 in piece1.ADSquares:
								result =  self.__update_Board(location1, location2, colour, piece1, piece2, revert)
								if revert == True:
										self.__revert(location1, location2, piece2)

								if result == True and revert == False:
									if piece2 != None:
										self.halfmove_clock = 0
										self.__updatePieceCount(piece2)

									elif type(piece1) == Pawn:
										self.halfmove_clock = 0

									else:
										self.halfmove_clock += 1

									if colour == 'black':
										self.fullmove_clock += 1

									if self.halfmove_clock == 50:
										result = 'end'
									
								return result

						else:
							if self.board[location2] == None:
								aaa = piece1.movePawn(location2)
								if piece1.movePawn(location2) == True:
									result =  self.__update_Board(location1, location2, colour, piece1, piece2, revert)
									if revert == True:
										self.__revert(location1, location2, piece2)

									if result == True and revert == False:
										if piece2 != None:
											self.halfmove_clock = 0
											self.__updatePieceCount(piece2)

										elif type(piece1) == Pawn:
											self.halfmove_clock = 0

										else:
											self.halfmove_clock += 1

										if colour == 'black':
											self.fullmove_clock += 1

										if self.halfmove_clock == 50:
											result = 'end'
										
									return result

								elif piece1.enPassant(location2, self) != 0:
									take = piece1.enPassant(location2, self)
									self.board[take] = None
									result =  self.__update_Board(location1, location2, colour, piece1, piece2, revert)
									if revert == True:
										self.__revert(location1, location2, piece2)

									if result == True and revert == False:
										if piece2 != None:
											self.halfmove_clock = 0
											self.__updatePieceCount(piece2)

										elif type(piece1) == Pawn:
											self.halfmove_clock = 0

										else:
											self.halfmove_clock += 1

										if colour == 'black':
											self.fullmove_clock += 1

										if self.halfmove_clock == 50:
											result = 'end'										
									return result

							else:
								if location2 in piece1.ADSquares:
									result =  self.__update_Board(location1, location2, colour, piece1, piece2, revert)
									if revert == True:
										self.__revert(location1, location2, piece2)

									if result == True and revert == False:
										if piece2 != None:
											self.halfmove_clock = 0
											self.__updatePieceCount(piece2)

										elif type(piece1) == Pawn:
											self.halfmove_clock = 0

										else:
											self.halfmove_clock += 1

										if colour == 'black':
											self.fullmove_clock += 1

										if self.halfmove_clock == 50:
											result = 'end'
										
									return result
		return False

	def __updatePieceCount(self, piece):
		pieceChar = 'PNBRQKpnbrqk'
		self.materialCount[pieceChar.find(piece.character)] -= 1

	def __updatePieceCountNew(self, piece):
		pieceChar = 'PNBRQKpnbrqk'
		self.materialCount[pieceChar.find(piece.character)] += 1

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

	def write_board(self):
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

	def copyBoard(self):
		newBoard = []
		for i in self.board:
			if i != None:
				newBoard.append(copy.deepcopy(i))

			else:
				newBoard.append(None)

		newChessBoard = copy.deepcopy(self)
		newChessBoard.board = newBoard
		return newChessBoard
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
			moveResult = board1.move(location1, location2, self.colour, False)
			if moveResult == False:
				print('wrong move')
				return self.turn()

			elif moveResult == 'checkmate':
				return True

			elif moveResult == 'end':
				return True

			else:
				print('turn over')
				f = open('move.txt','w')
				f.write('complete')
				f.close()
				FEN_code = FEN()
				colour = 'white'
				if self.colour == 'white':
					colour = 'black'
				print(FEN_code.notate(board1, colour))

		except:
			f = open('move.txt','w')
			f.write('listening')
			f.close()

		board1.write_board()

#node class for min max tree
class node():
	def __init__(self, val):
		self.val = val
		self.children = []
		self.move = (0,0)#move that results in board stored in val
		self.hash = None
		self.board = val
		self.descendants = 0
		self.colour = ''#colour of turn to result in board stored in val
		self.hashcolour = ''
		self.terminal = False

	def append(self, child, move, colour):
		if colour == 'white':
			self.hashcolour = 'black'

		else:
			self.hashcolour = 'white'
			
		child.move = move
		child.colour = colour
		self.children.append(child)

	#child generation algorithm for node
	def generate(self, colour):
		if type(self.val) == int:
			self.val = self.board

		fen = FEN()
		for i in self.val.board:
			if i != None:
				if i.colour == colour:
					if type(i) == Pawn:
						if colour == 'black':
							tempBoard = self.val.copyBoard()
							result = tempBoard.move(i.location, i.location + 16, colour, False)
							if result == True:
								self.append(node(tempBoard), (i.location, i.location + 16), colour)
								#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#self.validate(self.val, i.location, i.location + 16, colour)

							elif result == 'checkmate' or result == 'end':
								self.append('terminal')
								self.terminal = True
								#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))

							tempBoard = self.val.copyBoard()
							result = tempBoard.move(i.location, i.location + 32, colour, False)
							if result == True:
								self.append(node(tempBoard), (i.location, i.location + 32), colour)
								#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#self.validate(self.val, i.location, i.location + 32, colour)

						elif colour == 'white':
							tempBoard = self.val.copyBoard()
							result = tempBoard.move(i.location, i.location - 16, colour, False)
							if result == True:
								self.append(node(tempBoard), (i.location, i.location - 16), colour)
								#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#self.validate(self.val, i.location, i.location - 16, colour)

							tempBoard = self.val.copyBoard()
							result = tempBoard.move(i.location, i.location - 32, colour, False)
							if result == True:
								self.append(node(tempBoard), (i.location, i.location - 32), colour)
								#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#self.validate(self.val, i.location, i.location - 32, colour)

						for j in i.ADSquares:
							tempBoard = self.val.copyBoard()
							result = tempBoard.move(i.location, j, colour, False)
							if result == True:
								self.append(node(tempBoard), (i.location, j), colour)
								#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#self.validate(self.val, i.location, j, colour)

					elif type(i) == King:
						for j in i.ADSquares:
							tempBoard = self.val.copyBoard()
							result = tempBoard.move(i.location, j, colour, False)
							if result == True:
								self.append(node(tempBoard), (i.location, j), colour)
								#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#self.validate(self.val, i.location, j, colour)

						if i.colour == 'white':
							if i.location == 116:
								if i.Qcastling == True:
									tempBoard = self.val.copyBoard()
									result = tempBoard.move(116, 114, colour, False)
									if result == True:
										self.append(node(tempBoard), (116, 114), colour)
										#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#		self.validate(self.val, 116, 114, colour)

								if i.Kcastling == True:
									tempBoard = self.val.copyBoard()
									result = tempBoard.move(116, 118, colour, False)
									if result == True:
										self.append(node(tempBoard), (116, 118), colour)
										#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#		self.validate(self.val, 116, 118, colour)

						if i.colour == 'black':
							if i.location == 4:
								if i.Qcastling == True:
									tempBoard = self.val.copyBoard()
									result = tempBoard.move(4, 2, colour, False)
									if result == True:
										self.append(node(tempBoard), (4, 2), colour)
										#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#		self.validate(self.val, 4, 2, colour)

								if i.Kcastling == True:
									tempBoard = self.val.copyBoard()
									result = tempBoard.move(4, 7, colour, False)
									if result == True:
										self.append(node(tempBoard), (4, 7), colour)
										#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#		self.validate(self.val, 4, 7, colour)

					else:
						for j in i.ADSquares:
							tempBoard = self.val.copyBoard()
							if tempBoard.move(i.location, j, colour, False) == True:
								self.append(node(tempBoard), (i.location, j), colour)
								#boardTable.append(tempBoard, self.hashcolour, evaluate.totalEval(tempBoard), fen.notate(tempBoard, self.hashcolour))
								#self.validate(self.val, i.location, j, colour)

	#tree traversal algorithm
	def count(self, node, ply, target_ply):
		if ply == target_ply:
			self.descendants += 1
			FEN_code = FEN()

		for i in node.children:
			self.count(i, ply + 1, target_ply)

		return self.descendants

#chess ai class
class computer(player):
	def __init__(self, colour):
		player.__init__(self)
		self.colour = colour
		self.max_depth = 2
		self.rootNode = None

	def turn(self):
		if self.rootNode == None:
			self.rootNode = node(board1)

		self.__updateRoot()
		print('rootNode is:')
		self.rootNode.val.print_board()
		self.grow(self.rootNode, 0, self.max_depth, self.colour)

		maxing = False
		if self.colour == 'white':
			maxing = True

		optimalVal = self.minimax(0, self.rootNode, maxing, self.max_depth)

		nextNode = optimalVal[1]
		moveResult = board1.move(nextNode.move[0], nextNode.move[1], nextNode.colour, False)

		if moveResult == 'checkmate':
			return True

		elif moveResult == 'end':
			return True
		FEN_code = FEN()
		colour = 'white'
		if self.colour == 'white':
			colour = 'black'

		self.rootNode = nextNode
		print(FEN_code.notate(board1, colour))
		board1.write_board()

	def totalEval(self, board):
		return evaluate.totalEval(board)

	def minimax(self, depth, node, maxing, max_depth):
		if depth == max_depth or node.val == 'terminal':
			if node.val != 'terminal':
				return (self.totalEval(node.val),node)

			elif node.val == 'terminal':
				if node.colour == 'white':
					return 100000000000000000000000

				else:
					return -100000000000000000000000

		if maxing:
			value = (-10000000000000000, None)
			for i in node.children:
				# if type(node.val) != int:
				# 	value = -10000000000000000
				value = tupleMax(value, self.minimax(depth +1, i, False, max_depth))
			if depth == 0:
				return value

			else:
				return (value[0], node)

		else:
			value = (10000000000000000, None)
			for i in node.children:
				# if type(node.val) != int:
				# 	value = 10000000000000000
				value = tupleMin(value, self.minimax(depth +1, i, True, max_depth))
			if depth == 0:
				return value

			else:
				return (value[0], node)

	def minimax_AlphaBeta(self, depth, node, maxing, max_depth, alpha = (0, None), beta = (0, None)):
		if depth == max_depth or len(node.children) == 0:
			return (self.totalEval(node.val), node)

		if maxing:
			bestVal = (-10000000000000000, None)
			for i in node.children:
				value = self.minimax_AlphaBeta(depth +1, node, False, max_depth, alpha, beta)
				bestVal = tupleMax(bestVal, value)
				alpha = tupleMax(alpha, bestVal)
				if beta[0] <= alpha[0]:
					break

			if depth == 0:
				return bestVal

			else:
				return (bestVal[0], node)

		else:
			bestVal = (10000000000000000, None)
			for i in node.children:
				value = self.minimax_AlphaBeta(depth +1, node, True, max_depth, alpha, beta)
				bestVal = tupleMin(bestVal, value)
				beta = tupleMin(beta, bestVal)
				if beta[0] <= alpha[0]:
					break

			if depth == 0:
				return bestVal

			else:
				return (bestVal[0], node)

	def grow(self, node, depth, max_depth, colour):
		if depth == max_depth or node.terminal == True:
			node.board = node.val

		else:
			if len(node.children) == 0:
				node.generate(colour)

			if self.colour == 'white':

				colour ='black'

			elif self.colour == 'black':

				colour = 'white'

			for i in node.children:
				self.grow(i, depth + 1, max_depth, colour)

	def __updateRoot(self):
		fen = FEN()
		targetFEN = fen.notate(board1, 'white')
		print('target FEN is :')
		print(targetFEN)
		for i in self.rootNode.children:
			if targetFEN == fen.notate(i.board, 'white'):
				print('found FEN is :')
				print(fen.notate(i.board,'white'))
				self.rootNode = i
				return

		self.rootNode = node(board1)

	def test(self):
		depth = input('Input the number of ply:\n')
		root = node(board1)
		start_time = time.time()
		self.grow(root, 0, int(depth), 'white')
		end_time = time.time()
		total_time = end_time - start_time
		print('time for generation: ' + str(total_time) + ' seconds')
		return root.count(root, 0, int(depth))

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

#login system
class login():
	def menu():
		global root
		#login screen
		root = tk.Tk()
		window_width = 300
		window_height = 200
		screen_width = root.winfo_screenwidth()
		screen_height = root.winfo_screenheight()
		centre_x = screen_width // 2 - window_width // 2
		centre_y = screen_height // 2 - window_height // 2
		root.geometry(f"{window_width}x{window_height}+{centre_x}+{centre_y}")
		root.resizable(False, False)
		root.attributes("-topmost", 1)

		username = tk.StringVar()
		password = tk.StringVar()

		signin = ttk.Frame(root)
		signin.pack(padx = 10, pady = 10, fill = 'x', expand = True)

		ttk.Label(signin, text = "Username:").pack(fill = "x", expand = True)
		user_entry = ttk.Entry(signin, textvariable = username)
		user_entry.pack(fill = "x", expand = True)
		user_entry.focus()

		ttk.Label(signin, text = "Password:").pack(fill = "x", expand = True)
		pass_entry = ttk.Entry(signin, textvariable = password, show = "*")
		pass_entry.pack(fill = "x", expand = True)

		login_button = ttk.Button(root, text='login', command = lambda: login.hashCheck(str(username.get()), str(password.get())))
		login_button.pack(ipadx = 5, ipady = 5, expand = True)

		create_account_button = ttk.Button(root, text='Create Account', command = lambda: login.create(str(username.get()), str(password.get())))
		create_account_button.pack(ipadx = 5, ipady = 5, expand = True)

		root.mainloop()



	#password hasher
	def passwordHash(password):
		# numbers = PRNG.LCG(len(password), 257991014)
		# h = 0
		# for i in range(len(password)):
		# 	h = h ^ ord(password[i]) ^ numbers[i]
		# return h
		return sha2(password)

	def create(username, password):
		wrongLabel = ttk.Label(text='Username already taken', foreground='red')
		hashed = hex(login.passwordHash(password))
		conn = sqlite3.connect('chessplayers.db')
		cursor = conn.cursor()
		cursor.execute("""SELECT Username
			FROM tblUsers
			WHERE Username = '%s'""" % username)
		check = cursor.fetchall()
		if len(check) == 0:
			cursor.execute("""INSERT INTO tblUsers (Username, Hash)
				VALUES (?,?)""", (username, hashed))
			conn.commit()

		else:
			wrongLabel.pack(fill = 'x', expand = True)

	def hashCheck(username, password):
		if password == '':
			return
		hashed = hex(login.passwordHash(password))
		conn = sqlite3.connect('chessplayers.db')
		cursor = conn.cursor()
		cursor.execute("""SELECT Username, Hash
			FROM tblUsers
			WHERE Username = '%s'""" % username)
		details = cursor.fetchall()
		if details == []:
			return

		elif details[0][1] == hashed:
			global user
			user = username
			root.destroy()
			login.selectMode()

		else:
			return

	def selectMode():
		global root
		root = tk.Tk()
		window_width = 300
		window_height = 200
		screen_width = root.winfo_screenwidth()
		screen_height = root.winfo_screenheight()
		centre_x = screen_width // 2 - window_width // 2
		centre_y = screen_height // 2 - window_height // 2
		root.geometry(f"{window_width}x{window_height}+{centre_x}+{centre_y}")
		root.resizable(False, False)
		root.attributes("-topmost", 1)

		pvp_button = ttk.Button(root, text='MULTIPLAYER', command = lambda: pvp())
		pvp_button.pack(ipadx = 5, ipady = 5, expand = True)

		pvc_button = ttk.Button(root, text='SINGLE PLAYER', command = lambda: pvc())
		pvc_button.pack(ipadx = 5, ipady = 5, expand = True)

		load_button = ttk.Button(root, text='LOAD', command = lambda: login.load())
		load_button.pack(ipadx = 5, ipady = 5, expand = True)

	def load():
		root.destroy()
		selectC = tk.Tk()
		listbox = tk.Listbox(selectC)
		listbox.pack(side = tk.LEFT, fill = tk.BOTH)
		scrollbar = tk.Scrollbar(selectC)
		scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
		game_explorer = save()
		game_list = game_explorer.listAll(user)

		for i in game_list:
			listbox.insert(tk.END, i)

		listbox.config(yscrollcommand = scrollbar.set)
		scrollbar.config(command = listbox.yview)



def endGame(colour):
	board1.write_board()
	print('Checkmate')
	if colour == 'white':
		colour = 'Black'

	else:
		colour = 'White'

	f = open('move.txt', 'w')
	f.write(colour)
	f.close()

	print(colour + ' wins!')
	return

def startGui():
	subprocess.run('python gui.pyw', shell = False)

def game():
	global board1
	board1 = ChessBoard('standard')
	board1.ADBoard_init()
	valid = False
	global chessClock
	chessClock = clock(3600)
	f = open('move.txt', 'w')
	f.write('')
	f.close()
	while valid == False:
		login.menu()
		valid = True

#player vs player
def pvp():
	root.destroy()
	#start gui thread
	guiThread = threading.Thread(target = startGui)
	guiThread.start()
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

#player vs computer
def pvc():
	root.destroy()
	global selectC
	selectC = tk.Tk()
	window_width = 300
	window_height = 200
	screen_width = selectC.winfo_screenwidth()
	screen_height = selectC.winfo_screenheight()
	centre_x = screen_width // 2 - window_width // 2
	centre_y = screen_height // 2 - window_height // 2
	selectC.geometry(f"{window_width}x{window_height}+{centre_x}+{centre_y}")
	selectC.resizable(False, False)
	selectC.attributes("-topmost", 1)

	white = ttk.Button(selectC, text='WHITE', command = lambda: playing_as_white())
	white.pack(ipadx = 5, ipady = 5, expand = True)

	black = ttk.Button(selectC, text='BLACK', command = lambda: playing_as_black())
	black.pack(ipadx = 5, ipady = 5, expand = True)

	global boardTable
	boardTable = hashTable(seed = 855788754)
	boardTable.init_zobrist()


def playing_as_white():
	selectC.destroy()
	guiThread = threading.Thread(target = startGui)
	guiThread.start()

	colour1 = 'white'
	colour2 = 'black'

	player1 = human(colour1)
	player2 = computer(colour2)
	end = False
	endColour = 'white'
	while end != True:
		if colour1 == 'white':
			end = player1.turn()

		else:
			end = player2.turn()

		if end != True:
			if colour1 == 'white':
				end = player2.turn()

			else:
				end = player1.turn()

		else:
			endColour = 'black'

	endGame(endColour)

def playing_as_black():
	selectC.destroy()
	guiThread = threading.Thread(target = startGui)
	guiThread.start()

	colour1 = 'black'
	colour2 = 'white'

	player1 = human(colour1)
	player2 = computer(colour2)
	end = False
	endColour = 'white'
	while end != True:
		if colour1 == 'white':
			end = player1.turn()

		else:
			end = player2.turn()

		if end != True:
			if colour1 == 'white':
				end = player2.turn()

			else:
				end = player1.turn()

		else:
			endColour = 'black'

	endGame(endColour)

def testMode(menu):
	if menu == '3':
		print('///////////computer test mode///////////')
		cpu1 = computer('white')
		print('1st move count: ')
		print(cpu1.test())

	elif menu == '4':
		print('///////////zobrist test mode////////////')
		hashBoard = hashTable()
		hashBoard.init_zobrist()
		hashedBoard = hashBoard.hash(board1, 'white')
		print(hashedBoard)

	elif menu == '5':
		player1 = computer('white')
		a = node(None)
		b = node(None)
		c = node(None)
		d = node(None)
		e = node(None)
		f = node(None)
		c.children = [node(24),node(654),node(24),node(678)]
		d.children = [node(84), node(74)]
		e.children = [node(723), node(85), node(1644)]
		f.children = [node(627),node(560),node(45), node(6264), node(69)]
		a.children = [c,d]
		b.children = [e,f]
		root = node(None)
		root.children = [a,b]
		#player1.grow(root, 0, 2, 'white')
		print(player1.minimax(0, root, True, 3))

	else:
		print('that is not an option')

if __name__ == '__main__':
	game()