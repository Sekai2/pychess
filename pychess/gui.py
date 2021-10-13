import pygame

class gui():
	def __init__(self):
		pygame.init()
		gameDisplay = pygame.display.set_mode((631,632))
		pygame.display.set_caption('PyChess')
		clock = pygame.time.Clock()
		gui_board = pygame.image.load('assets/board.png')

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

		crashed = False
		while not crashed:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					crashed = True

				print(event)

			gameDisplay.blit(gui_board, (0,0))
			gameDisplay.blit(black_rook, (9,10))
			gameDisplay.blit(black_bishop, (88,10))

			pygame.display.update()
			clock.tick(60)

	def __quit(self):
		pygame.quit()
		quit()

gui1 = gui()