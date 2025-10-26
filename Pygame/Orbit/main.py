import pygame,sys
from player import Ball as player;from block import Spawner;from menu import Ui
from debug import debug
pygame.init()
info=pygame.display.Info()
width=info.current_w;height=info.current_h
screen=pygame.display.set_mode((width , height))
clock=pygame.time.Clock()
font=pygame.font.Font(None,width//10)
spawn=pygame.event.custom_type()
restart=pygame.event.custom_type()
def refresh():return player(width,height),Spawner(width,height),Ui(font)
ball,spawner,ui=refresh()
class State(enumerate): play=1;reset=2;out=3;start=4
state=State.start
hold=False
while True:
	screen.fill('black');dt=clock.tick(60)/1000
	for event in pygame.event.get():
		if event.type==pygame.QUIT:pygame.quit();sys.exit()
		elif event.type==pygame.FINGERDOWN:
			if state==State.play:hold=True
			elif state==State.reset:ball,spawner,ui=refresh();state=State.play
			elif state==State.start: state=State.play
		elif event.type==pygame.FINGERUP:hold=False
		elif event.type==spawn:spawner.addblock()
		elif event.type==restart and state==State.out:state=State.reset
	if spawner.isspawn():pygame.event.post(pygame.event.Event(spawn))
	if state==State.play:
		ball.draw(screen);ball.update(hold,dt)
		spawner.update(screen,ball,dt)
		ui.scoreupdate(screen,spawner,ball)
		if spawner.collision(ball):state=State.out;pygame.time.set_timer(restart,2000)	
	elif state==State.start:ui.startupdate(screen)
	elif state== State.out and hasattr(ball , 'animation'):ball.animation(screen)
	elif state==State.reset:ui.outupdate(screen)
	ui.fps(screen,clock)
	#debug(screen.get_size() , font)
	pygame.display.flip()


	
 