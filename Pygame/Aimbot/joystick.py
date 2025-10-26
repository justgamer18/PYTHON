import pygame

class Joystick:
	
	def __init__(self , width , height):
		self.width = width
		self.height = height
		self.baseradius = self.width // 7
		self.stickradius = self.width // 10
		self.color = 'gray30'
		self.basepos = pygame.Vector2(self.width // 2 , self.height // 1.20)
		self.stickpos = self.basepos.copy()
		self.direction = pygame.Vector2()
		self.isactive = False
		self.alpha = 0
	
	def getdirection(self):
		direction = pygame.mouse.get_pos() - self.basepos
		mindistance = min(direction.length() , self.baseradius)
		if direction.length_squared() != 0:
			direction=direction.normalize() * mindistance
			return direction
		return pygame.Vector2()
		
	def istouch(self):
		return (pygame.mouse.get_pos() - self.basepos).length() <= self.baseradius
	
	def update(self):
		self.stickpos = self.basepos + self.getdirection() if self.isactive else self.basepos.copy()
		self.color = 'gray50' if self.isactive else 'gray20'
			
	def event(self , event):
		if event.type == pygame.FINGERDOWN and self.istouch():
			self.isactive = True
		elif event.type == pygame.FINGERUP:
			self.isactive = False
		
	def draw(self , surface):
		pygame.draw.circle(surface , self.color , self.basepos , self.baseradius , 5)
		pygame.draw.circle(surface , self.color , self.stickpos , self.stickradius)
		
		
		