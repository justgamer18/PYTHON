import pygame
import sys
from debug import debug
from joystick import Joystick
from player import Player
from enemy import Enemies
from menu import Menu

pygame.init()

info = pygame.display.Info()
width = info.current_w
height = info.current_h
screensize = (width , height)
screen = pygame.display.set_mode(screensize)

clock = pygame.time.Clock()
font = pygame.freetype.Font(None, width // 13)

shootsound = pygame.mixer.Sound('shootsound.mp3')
pygame.mixer.set_num_channels(100)
shootsound.set_volume(0.1)

shoot = pygame.event.custom_type()
spawn = pygame.event.custom_type()
restart = pygame.event.custom_type()

pygame.time.set_timer(shoot , 250)
pygame.time.set_timer(spawn , 250)

def refresh():
	return Joystick(width , height) , Player(width , height) , Enemies(width , height) , Menu(width , height , font)

joystick , player , enemies , menu= refresh()

class State(enumerate):
	start = 0
	play = 1
	out = 2
	reset = 3

state = State.start

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
				joystick , player , enemies , menu = refresh()
			state = State.play
		elif event.type == shoot and state == State.play:
			player.shoot(shootsound)
		elif event.type == spawn and state == State.play:
			enemies.addenemies()
		elif event.type == restart and state == State.out:
			state = State.reset
			
		joystick.event(event)
		
	if state == State.start:
		menu.start()
		
	if state == State.play:
		joystick.update()
		player.update(joystick , enemies , dt)
		joystick.draw(screen)
		player.draw(screen)
		enemies.update(player , dt)
		enemies.draw(screen)
		menu.score(player)
		if player.isdead():
			state = State.out
			pygame.time.set_timer(restart , 1500)
	
	elif state == State.out:
		player.deathanimation(screen , dt)
				
	elif state == State.reset:
		menu.gameover()
		
	pygame.display.flip()
	