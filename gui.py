#gui

import pygame

class gui():
	def __init__(self):
		pygame.init()
		logo = pygame.image.load('assets/logo.png')
		pygame.display.set_icon(logo)
		pygame.display.set_caption('Pychess')

		board = pygame.image.load('assets/board.png')
		screen = pygame.display.set_mode((631,632))
		

		running = True

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

gui1 = gui()
