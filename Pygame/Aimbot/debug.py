import pygame

def debug(font , info , y = 100 , x = None , color = 'white'):
	screen = pygame.display.get_surface()
	width = screen.get_width()
	font.antialiased = False
	if x == None:
		x = width // 2
	surface , rect = font.render(str(info) , fgcolor = color)
	rect.center =(x , y)
	screen.blit(surface , rect)