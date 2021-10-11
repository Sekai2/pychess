import pygame

class gui():
	def __init__(self):
		pygame.init()
		gameDisplay = pygame.display.set_mode((631,632))
		pygame.display.set_caption('PyChess')
		clock = pygame.time.Clock()
		gui_board = pygame.image.load('assets/board.png')

		crashed = False
		while not crashed:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					crashed = True

				print(event)

			gameDisplay.blit(gui_board, (0,0))

			pygame.display.update()
			clock.tick(60)

	def __piece(self):
		

	def __quit(self):
		pygame.quit()
		quit()

gui1 = gui()