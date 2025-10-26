import sys
import pygame
from fruit import Spawner
from color import *
from menu import Menu
pygame.init()
clock=pygame.time.Clock()
info=pygame.display.Info()
width=info.current_w
height=info.current_h
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption(';')
font=pygame.font.Font(None,width//10)
spawn=pygame.event.custom_type()
restart=pygame.event.custom_type()
def refresh():
	return Spawner(neon,width,height),Menu(font,white,width,height)
spawner,menu=refresh()
class State(enumerate):
	start= 0
	play=1
	out=2
	reset=3
state=State.start
run=True
while run:
	tap=False
	screen.fill(black)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run=False
		elif event.type==pygame.MOUSEBUTTONDOWN:
			if state == State.start:
				state = State.play
			if state==State.reset:
				spawner,menu=refresh()
				state=State.play
			tap=True
		elif event.type==pygame.MOUSEBUTTONUP:
			tap=False
		elif event.type==spawn:
			spawner.addfruits()
		elif event.type==restart and state==State.out:
			state=State.reset
	if spawner.isspawn():
		pygame.event.post(pygame.event.Event(spawn))
		
	if state == State.start:
		menu.start(screen)
	if state==State.play:
		if spawner.out(tap):
			menu.vibrate(100)
			state=State.out
			pygame.time.set_timer(restart,1000)
		spawner.draw(screen)
		spawner.iscollide(tap)
		spawner.update()
		spawner.incdiff()
		menu.score(screen,spawner)
	elif state==State.reset:
		menu.gameover(screen,spawner)
	menu.lag(screen,clock)
	pygame.display.flip()
	clock.tick(60)
pygame.quit()
sys.exit()