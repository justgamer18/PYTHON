import pygame

def debug(font , info , y = 50 , x = None , color = 'white'):
	screen = pygame.display.get_surface()
	if x == None:
		x = screen.get_width() // 2
	surf , rect = font.render(str(info) , fgcolor = color)
	rect.center = (x , y)
	screen.blit(surf , rect)