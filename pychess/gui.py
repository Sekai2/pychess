import pygame
from misc import *

def id_square(coordinate):
	x = coordinate[0]
	y = coordinate[1]
	x_index = x // 79
	y_index = y // 79
	index = x*y
	return hex(index)

class gui():
	def __init__(self):

		#place
		pygame.init()
		self.gameDisplay = pygame.display.set_mode((631,632))
		pygame.display.set_caption('PyChess')
		clock = pygame.time.Clock()
		gui_board = pygame.image.load('assets/board.png')

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
		#self.gameDisplay.blit(black_rook, (9,10))
		#self.gameDisplay.blit(black_bishop, (88,10))
		#self.gameDisplay.blit(black_knight, (167,10))
		#self.gameDisplay.blit(black_queen, (246,10))
		#self.gameDisplay.blit(black_king, (325,10))
		#self.gameDisplay.blit(black_knight, (404,10))
		#self.gameDisplay.blit(black_bishop, (483,10))
		#self.gameDisplay.blit(black_rook, (562,10))

		#position = (9,90)
		#for i in range(8):
		#	x = (79 * (i+1)) - 70
		#	position = (x,90)
		#	self.gameDisplay.blit(black_pawn, (position))

		#self.gameDisplay.blit(white_rook, (9,563))
		#self.gameDisplay.blit(white_bishop, (88,563))
		#self.gameDisplay.blit(white_knight, (167,563))
		#self.gameDisplay.blit(white_queen, (246,563))
		#self.gameDisplay.blit(white_king, (325,563))
		#self.gameDisplay.blit(white_knight, (404,563))
		#self.gameDisplay.blit(white_bishop, (483,563))
		#self.gameDisplay.blit(white_rook, (562,563))

		for i in range(8):
			x = (79 * (i+1)) - 70
			position = (x,484)
			self.gameDisplay.blit(white_pawn, (position))

		crashed = False
		while not crashed:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					crashed = True

			if pygame.mouse.get_pressed() != (False, False, False):
				print(pygame.mouse.get_pos())

			self.gameDisplay.blit(gui_board, (0,0))
			self.__board_update()
			

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

	def __move(self):
		f = open('move.txt','rw')
		content = f.read()
		while content == 'listening':
	 		if pygame.mouse.get_pressed() == (True, False, False):
	 			coordinate = pygame.mouse.get_pos()
	 			index = id_square(coordinate)
	 			f.write(index)




	def __quit(self):
		pygame.quit()
		quit()

gui1 = gui()