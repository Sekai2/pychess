import pygame
import time
from misc import *

def id_square(coordinate):
	x = coordinate[0]
	y = coordinate[1]
	x_index = x // 79
	y_index = y // 79
	index = x_index + y_index*16
	print(coordinate)
	print('x ' + str(x_index))
	print('y ' + str(y_index))
	print('board index = ' + str(index))
	return hex(index)

class gui():
	def __init__(self):
		self.coordinate1 = None
		self.coordinate2 = None
		self.press_count = 0

		#colours
		self.black = (0, 0, 0)
		self.grey = (55, 55, 55)
		self.white = (255, 255, 255)

		#place
		pygame.init()
		icon = pygame.image.load('assets/logo.png')
		pygame.display.set_icon(icon)

		self.gameDisplay = pygame.display.set_mode((750,632))
		self.gameDisplay.fill(self.white)
		#board (coordinate), (dimensions): (0,0),(631,632)
		#board (coordinate), (dimensions): (631,632)


		pygame.display.set_caption('PyChess')
		clock = pygame.time.Clock()
		gui_board = pygame.image.load('assets/board.png')

		#defining fonts


		#load pieces
		white_pawn = pygame.image.load('assets/wp.png')
		white_bishop = pygame.image.load('assets/wb.png')
		white_knight = pygame.image.load('assets/wn.png')
		white_rook = pygame.image.load('assets/wr.png')
		white_queen = pygame.image.load('assets/wq.png')
		white_king = pygame.image.load('assets/wk.png')

		black_pawn = pygame.image.load('assets/bp.png')
		black_bishop = pygame.image.load('assets/bb.png')
		black_knight = pygame.image.load('assets/bn.png')
		black_rook = pygame.image.load('assets/br.png')
		black_queen = pygame.image.load('assets/bq.png')
		black_king = pygame.image.load('assets/bk.png')

		self.piece_list = [white_pawn, white_bishop, white_knight, white_rook, white_queen, white_king, black_pawn, black_bishop, black_knight, black_rook, black_queen, black_king]

		self.gameDisplay.blit(gui_board, (0,0))

		for i in range(8):
			x = (79 * (i+1)) - 70
			position = (x,484)
			self.gameDisplay.blit(white_pawn, (position))

		crashed = False
		while not crashed:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					crashed = True

			self.gameDisplay.blit(gui_board, (0,0))
			self.__board_update()
			self.__updateBar()

			self.__getmouse == 0

			f = open('move.txt','r')
			content = f.read()
			if content == 'listening':

				if self.press_count == 0:
					if pygame.mouse.get_pressed() == (True, False, False):
						self.__getmouse()

				elif self.press_count == 2:
					if pygame.mouse.get_pressed() == (True, False, False):
						self.__getmouse()
						self.press_count = 0
						time.sleep(1)

				elif self.press_count == 1:
					if event.type == pygame.MOUSEBUTTONUP:
						print('2')
						self.press_count = 2

			pygame.display.update()
			clock.tick(60)

	def __board_update(self):
		f = open('board.txt', 'r')
		board = f.read()
		f.close()
		piece_characters = 'pbnrqkPBNRQK'
		for i in range(len(board)):
			if (i & 0x88) == 0:
				if board[i] != 'o':
					y = board_rank(i) * 80 + 10
					x = board_file(i) * 79 + 9
					self.gameDisplay.blit(self.piece_list[piece_characters.find(board[i])], (x,y))

				elif board[i] == 'o':
					pass

	def __getmouse(self):
		if pygame.mouse.get_pos()[0] < 632 and pygame.mouse.get_pos()[1] < 633:
			if self.coordinate1 == None:
				print('pressed1')
				self.coordinate1 = pygame.mouse.get_pos()
				print('first coordinate:')
				print(self.coordinate1)
				self.press_count = 1

			else:
				print('pressed2')
				self.coordinate2 = pygame.mouse.get_pos()
				print('second coordinate:')
				print(self.coordinate2)
				self.__move(self.coordinate1, self.coordinate2)

	def __move(self, coordinate1, coordinate2):
		index1 = id_square(coordinate1)
		index2 = id_square(coordinate2)
		indexs = index1 + index2
		f = open('move.txt','w')
		f.write(indexs)
		f.close()
		self.coordinate1 = None
		self.coordinate2 = None

	def __updateBar(self):
		f = open('UCode.txt', 'r')
		content = f.read()
		f.close()
		font = pygame.font.SysFont('Calibri', 50)
		img = font.render('90:30', True, self.grey)
		self.gameDisplay.blit(img, (631,20))

	def __quit(self):
		pygame.quit()
		quit()

gui1 = gui()