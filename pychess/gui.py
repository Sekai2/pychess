import pygame
class gui():
	def __init__(self):
		pygame.init()
		gameDisplay = pygame.display.set_mode((631,632))
		pygame.display.set_caption('PyChess')
		clock = pygame.time.Clock()
		gui_board = pygame.image.load('assets/board.png')

#		class White_Pawn(pygame.sprite.Sprite):
#			def __init__(self):
#				pygame.sprite.Sprite.__init__(self)
#				self.image = white_pawn()
#				self.image.set_colorkey(WHITE)
#				self.rect = self.image.get_rect();

#		pieces = pygame.sprite.Group()
#		pieces.add(White_Pawn)

#		White_Pawn.rect.x = 300
#		White_Pawn.rect.y = 300

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

		gameDisplay.blit(gui_board, (0,0))
		gameDisplay.blit(black_rook, (9,10))
		gameDisplay.blit(black_bishop, (88,10))
		gameDisplay.blit(black_knight, (167,10))
		gameDisplay.blit(black_queen, (246,10))
		gameDisplay.blit(black_king, (325,10))
		gameDisplay.blit(black_knight, (404,10))
		gameDisplay.blit(black_bishop, (483,10))
		gameDisplay.blit(black_rook, (562,10))

		position = (9,90)
		for i in range(8):
			x = (79 * (i+1)) - 70
			position = (x,90)
			gameDisplay.blit(black_pawn, (position))

		gameDisplay.blit(white_rook, (9,563))
		gameDisplay.blit(white_bishop, (88,563))
		gameDisplay.blit(white_knight, (167,563))
		gameDisplay.blit(white_queen, (246,563))
		gameDisplay.blit(white_king, (325,563))
		gameDisplay.blit(white_knight, (404,563))
		gameDisplay.blit(white_bishop, (483,563))
		gameDisplay.blit(white_rook, (562,563))

		for i in range(8):
			x = (79 * (i+1)) - 70
			position = (x,484)
			gameDisplay.blit(white_pawn, (position))

		crashed = False
		while not crashed:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					crashed = True

			if pygame.mouse.get_pressed() != (False, False, False):
				print(pygame.mouse.get_pos())

			

			pygame.display.update()
			clock.tick(60)

	def __quit(self):
		pygame.quit()
		quit()

gui1 = gui()