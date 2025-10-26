from config import *

def debug(info , y = 50 , x = screen_width * 0.5 , color = debug_color , size = font_size):
	surf , rect = font.render(str(info) , fgcolor = color , size = size)
	rect.center = (x , y)
	screen.blit(surf , rect)