import pygame , sys
from player import Player
from enemy import Enemies
from menu import Menu
from debug import debug

pygame.init()

info = pygame.display.Info()
width = info.current_w
height = info.current_h
screensize = (width , height)

screen = pygame.display.set_mode(screensize)

clock = pygame.time.Clock()

font = pygame.freetype.Font(None,  width // 13)
bulletfont = pygame.freetype.Font(None , width // 25)

sound = pygame.mixer.Sound('shootsound.mp3')
sound.set_volume(0.1)

spawn = pygame.event.custom_type()
restart = pygame.event.custom_type()

pygame.time.set_timer(spawn , 2500)

def refresh():
	return Player(width , height) , Enemies(width , height , bulletfont) , Menu(width , height , font)
	
class State(enumerate):
	start = 0
	play = 1
	out = 2
	reset = 3
	
state = State.start

player , enemies , menu = refresh()
while True:
	
	screen.fill('black')
	dt = clock.tick(60) / 1000
	
	menu.fps(clock)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.FINGERDOWN and not state == State.out:
			if state == State.reset:
				player , enemies , menu = refresh()
			pygame.key.start_text_input()
			state = State.play
		elif event.type == pygame.TEXTINPUT:
			player.shoot(bulletfont , event.text , sound)
		elif event.type == spawn and state == State.play:
			enemies.addenemies()
		elif event.type == restart and state == State.out:
			state = State.reset
		
	if state == State.start:
		menu.start()
	
	if state == State.play:
		player.update(enemies , dt)
		player.draw(screen)
		enemies.draw(screen)
		enemies.update(player , dt)
		menu.score(player)
		if player.isdead():
			state = State.out
			pygame.time.set_timer(restart , 2000)
		
	elif state == State.out:
		pygame.key.stop_text_input()
		player.deathanimation(screen , dt)
	
	elif state == State.reset:
		menu.gameover()
	
	pygame.display.flip()