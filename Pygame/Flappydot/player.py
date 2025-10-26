import pygame
class Player:
	def __init__(self,w,h,c):
		self.r=w//15
		self.x=w//6
		self.y=h//2
		self.boundary=w//100
		self.vy=0
		self.gravity=2.5
		self.jump=-h*0.014
		self.colour=c.white
		self.h=h
	def move(self,tap):
		self.vy+=self.gravity
		if tap:
			self.vy=self.jump
		self.y+=self.vy
	def draw(self,surface):
		pygame.draw.circle(surface,self.colour,(self.x,self.y),self.r,self.boundary)
	def collide(self,rect):
		closestx=max(rect.left,min(self.x,rect.right))
		closesty=max(rect.top,min(self.y,rect.bottom))
		colx=self.x-closestx
		coly=self.y-closesty
		col=(colx*colx)+(coly*coly)
		return col<(self.r*self.r)
			
		