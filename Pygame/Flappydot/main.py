import sys
import pygame
import colour
from menu import Menu
from player import Player
from block import Spawner
pygame.init()
info=pygame.display.Info()
clock=pygame.time.Clock()
width=info.current_w
height=info.current_h
screen=pygame.display.set_mode((width,height))
font=pygame.font.Font(None, width//10)
spawn=pygame.USEREVENT+1
restart=pygame.USEREVENT+2
pygame.display.set_caption(';')
def refresh():
	return Player(width,height,colour),Spawner(width,height,colour),Menu(colour,width,height,font)
player,spawner,menu=refresh()
pygame.time.set_timer(spawn,spawner.spawntime)
class State(enumerate):
	start= 0
	play=1
	out=2
	restart=3
state=State.start
run=True
while run:
	tap=False
	screen.fill(colour.black)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run=False
		elif event.type==pygame.FINGERDOWN:
			if state==State.start:
				state = State.play
			elif state == State.play:
				tap = True
			elif state==State.restart:
				player,spawner,menu=refresh()
				state=State.play
		elif event.type==spawn:
			spawner.addblocks()
			pygame.time.set_timer(spawn,spawner.spawntime)
		elif event.type==restart and state==State.out:
			state=State.restart
			
	if state == State.start:
		menu.starter(screen)
	if state==State.play:
		player.move(tap)
		player.draw(screen)
		spawner.move()
		spawner.difficulty()
		if spawner.checkcollide(player):
			pygame.time.set_timer(restart,1500)
			state=State.out
			menu.vibrate(100)
	elif state==State.out:
		if menu.blink():
			player.draw(screen)
	elif state==State.restart:
		menu.gameover(screen,spawner)
	if state!=State.restart:
		spawner.draw(screen)
		menu.score(screen,player,spawner)
	menu.lag(screen,clock)
	clock.tick(60)
	pygame.display.flip()
pygame.quit()
sys.exit()

