import pygame

from config import *
from map import Map
from joystick import Joystick
from player import Player
from raycast import Raycast
from debug import debug

class Game:
	
	def __init__(self):
		self.map = Map()
		self.joystick = Joystick()
		self.player = Player(self.map)
		self.raycast = Raycast(self.map)
		
	def handle_event(self):
		for event in pg.event.get():
			
			if event.type == pg.QUIT:
				pygame.quit()
				sys.exit()
			
			self.joystick.handle_event(event)
				
	def debug(self):
		debug(int(clock.get_fps()))
		
	def update(self):
		dt = clock.tick(fps) / 1000
		
		self.joystick.update()
		self.player.update(self.joystick , dt)
		self.raycast.update(self.player)
		
		pg.display.flip()
			
	def draw(self):
		screen.fill(screen_color)
		
		#self.map.draw()
		#self.player.draw()
		self.raycast.draw()
		self.joystick.draw()
		self.debug()
	
	def run(self):
		while True:
			
			self.handle_event()
			self.update()
			self.draw()
		
if __name__ == '__main__':
	game = Game()
	game.run()