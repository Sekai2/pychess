#game gui code

import pygame
import time
from misc import *

#identifies the index of the square selected
def id_square(coordinate):
	x = coordinate[0]
	y = coordinate[1]
	x_index = x // 79
	y_index = y // 79
	index = x_index + y_index*16
	return hex(index)

class gui():
	def __init__(self):
		self.dot = None
		self.coordinate1 = None
		self.coordinate2 = None
		self.press_count = 0
		self.event = None

		#colours
		self.black = (0, 0, 0)
		self.grey = (27, 25, 22)
		self.white = (255, 255, 255)

		#place
		pygame.init()
		icon = pygame.image.load('assets/logo.png')
		pygame.display.set_icon(icon)

		self.gameDisplay = pygame.display.set_mode((631,632))


		pygame.display.set_caption('Tim Chess')
		clock = pygame.time.Clock()
		gui_board = pygame.image.load('assets/board.png')

		#load pieces
		white_pawn = pygame.image.load('assets/wp.png')#0
		white_bishop = pygame.image.load('assets/wb.png')#1
		white_knight = pygame.image.load('assets/wn.png')#2
		white_rook = pygame.image.load('assets/wr.png')#3
		white_queen = pygame.image.load('assets/wq.png')#4
		white_king = pygame.image.load('assets/wk.png')#5

		black_pawn = pygame.image.load('assets/bp.png')#6
		black_bishop = pygame.image.load('assets/bb.png')#7
		black_knight = pygame.image.load('assets/bn.png')#8
		black_rook = pygame.image.load('assets/br.png')#9
		black_queen = pygame.image.load('assets/bq.png')#10
		black_king = pygame.image.load('assets/bk.png')#11

		#loading other assets
		self.square_selected = pygame.image.load('assets/SquareSelected.png')
		self.piece_pick = pygame.image.load('assets/piecepickpng.png')
		self.checkmateW = pygame.image.load('assets/CheckmateW.png')
		self.checkmateB = pygame.image.load('assets/CheckmateB.png')

		self.piece_list = [white_pawn, white_bishop, white_knight, white_rook, white_queen, white_king, black_pawn, black_bishop, black_knight, black_rook, black_queen, black_king]

		self.gameDisplay.blit(gui_board, (0,0))

		crashed = False
		checkmate = False
		while not crashed:
			for self.event in pygame.event.get():
				if self.event.type == pygame.QUIT:
					crashed = True

			if checkmate == False:
				self.gameDisplay.blit(gui_board, (0,0))
				if self.dot != None:
					self.__SquareSelect(self.dot)
				self.__board_update()

				self.__getmouse == 0

				f = open('move.txt','r')
				content = f.read()
				f.close()
				if content == 'listening':
					self.__getSelection()

				elif content == 'chooseWhite':
					self.piece_pick_load('white')
					self.__choose_square()

				elif content == 'chooseBlack':
					self.piece_pick_load('black')
					self.__choose_square()

				elif content == 'White':
					self.__board_update()
					self.gameDisplay.blit(self.checkmateW, (158,237))					
					checkmate = True

				elif content == 'Black':
					self.__board_update()
					self.gameDisplay.blit(self.checkmateB, (158,237))
					checkmate = True

			else:
				time.sleep(5)
				quit()

			pygame.display.update()
			clock.tick(60)

	#adding transparency to image
	def __blit_alpha(self, source, location, opacity):
		x = location[0]
		y = location[0]
		temp = pygame.Surface((source.get_width(), source.get_height())).convert()
		temp.blit(self.gameDisplay, (-x, -y))
		temp.blit(source, (0,0))
		temp.set_alpha(opacity)
		self.gameDisplay.blit(temp, location)

	#updating the pieces on the board
	def __board_update(self):
		f = open('board.txt', 'r')
		board = f.read()
		f.close()
		piece_characters = 'PBNRQKpbnrqk'
		for i in range(len(board)):
			if (i & 0x88) == 0:
				if board[i] != 'o':
					y = board_rank(i) * 80 + 10
					x = board_file(i) * 79 + 9
					self.gameDisplay.blit(self.piece_list[piece_characters.find(board[i])], (x,y))

				elif board[i] == 'o':
					pass

	#loading the pawn transformation selection box
	def piece_pick_load(self, colour):
		if colour == 'black':
			self.gameDisplay.blit(self.piece_pick, (166,125))
			self.gameDisplay.blit(self.piece_list[8], (178,130))
			self.gameDisplay.blit(self.piece_list[7], (250,130))
			self.gameDisplay.blit(self.piece_list[9], (322,130))
			self.gameDisplay.blit(self.piece_list[10], (394,130))

		elif colour == 'white':
			self.gameDisplay.blit(self.piece_pick, (166,440))
			self.gameDisplay.blit(self.piece_list[2], (178,445))
			self.gameDisplay.blit(self.piece_list[1], (250,445))
			self.gameDisplay.blit(self.piece_list[3], (322,445))
			self.gameDisplay.blit(self.piece_list[4], (394,445))

	def __getSelection(self):
		if self.press_count == 0:
			if pygame.mouse.get_pressed() == (True, False, False):
				self.__getmouse()

		elif self.press_count == 2:
			if pygame.mouse.get_pressed() == (True, False, False):
				self.__getmouse()
				self.dot = None
				self.press_count = 3

		elif self.press_count == 1:
			if self.event.type == pygame.MOUSEBUTTONUP:
				self.press_count = 2

		elif self.press_count == 3:
			if self.event.type == pygame.MOUSEBUTTONUP:
				self.press_count = 0

	def __getmouse(self):
		if pygame.mouse.get_pos()[0] < 632 and pygame.mouse.get_pos()[1] < 633:
			if self.coordinate1 == None:
				mouse_pos = pygame.mouse.get_pos()
				self.coordinate1 = mouse_pos
				self.press_count = 1
				self.dot = mouse_pos

			else:
				self.coordinate2 = pygame.mouse.get_pos()
				self.__move(self.coordinate1, self.coordinate2)

	def __SquareSelect(self, coordinate):
		x = (coordinate[0] // 79) * 79
		y = (coordinate[1] // 79) * 79
		self.__blit_alpha(self.square_selected, (x,y), 128)

	#submitting user move input
	def __move(self, coordinate1, coordinate2):
		index1 = id_square(coordinate1)
		index2 = id_square(coordinate2)
		if len(index1) < 4:
			index1 = index1[:2] + '0' + index1[2]

		if len(index2) < 4:
			index2 = index2[:2] + '0' + index2[2]
			
		indexs = index1 + index2
		f = open('move.txt','w')
		f.write(indexs)
		f.close()
		self.coordinate1 = None
		self.coordinate2 = None


	def __choose_square(self):
		if self.press_count == 3:
			if pygame.mouse.get_pressed() == (True, False, False):
				coordinate = pygame.mouse.get_pos()
				result = None

				x = coordinate[0]
				y = coordinate[1]
				if 125 < y < 195 or 440 < y < 510:
					if 166< x < 250:
						result = 'N'

					elif 250 < x < 322:
						result = 'B'

					elif 322 < x < 394:
						result = 'R'

					elif 394 < x < 466:
						result = 'Q'

					else:
						result = None

					if result != None:
						f = open('move.txt','w')
						f.write(result)
						f.close()
				
					self.press_count = 1

		elif self.press_count == 1:
			if self.event.type == pygame.MOUSEBUTTONUP:
				self.press_count = 0

		return None

	def __quit(self):
		pygame.quit()
		quit()

gui1 = gui()