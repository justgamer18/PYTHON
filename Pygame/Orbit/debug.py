import pygame
def debug(info,font,y=50,x=550,color='white'):
	display=pygame.display.get_surface()
	infosurf=font.render(str(info),False,color)
	inforect=infosurf.get_rect(center=(x,y))
	display.blit(infosurf,inforect)