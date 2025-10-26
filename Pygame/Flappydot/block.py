import pygame
import random
class Block:
	def __init__(self,w,h,c,vx):
		self.gapsize=int(h*0.2)
		self.x=w
		self.isscore=False
		self.width=w//10
		colour=[pygame.Color('deeppink'),pygame.Color('hotpink'),pygame.Color('aqua'),pygame.Color('lime'),pygame.Color('magenta'),pygame.Color('lightskyblue'),pygame.Color('red'),pygame.Color('green'),pygame.Color('blue'),pygame.Color('orange'),pygame.Color('yellow')]
		self.colour=random.choice(colour)
		self.vx=vx
		self.gapst=random.randint(int(h*0.3),int(h-self.gapsize+h*0.2))
		self.toprect=pygame.Rect(self.x,0,self.width,h-self.gapst)
		self.bottomrect=pygame.Rect(self.x,h-self.gapst+self.gapsize,self.width,h-self.gapsize)
	def move(self):
		self.x-=self.vx
		self.toprect.x=self.x
		self.bottomrect.x=self.x
	def draw(self,surface):
		pygame.draw.rect(surface,self.colour,self.toprect)
		pygame.draw.rect(surface,self.colour,self.bottomrect)
class Spawner:
	def __init__(self,w,h,c):
		self.blocks=[]
		self.vx=w//100
		self.spawntime=1500
		self.w=w
		self.h=h
		self.c=c
		self.diff=pygame.time.get_ticks()
		self.score=0
	def addblocks(self):
		block=Block(self.w,self.h,self.c,self.vx)
		self.blocks.append(block)
	def move(self):
		for b in self.blocks[:]:
			b.move()
	def draw(self,surface):
		for b in self.blocks[:]:
			if b.x+b.width<0:
				self.blocks.remove(b)
			b.draw(surface)
	def checkcollide(self,player):
		if player.y+(player.r*2)>self.h or player.y<0:
			return True
		for b in self.blocks:
			if player.collide(b.toprect) or player.collide(b.bottomrect):
				return True		
	def checkscore(self,player):
		for b in self.blocks:
			if not b.isscore and b.x+b.width+player.r<player.x:
				self.score+=1
				b.isscore=True
	def difficulty(self):
		now=pygame.time.get_ticks()
		if (now-self.diff)>2500:
			self.diff=now
			self.vx+=0.2
			self.spawntime=max(250,self.spawntime-10)
			
		
		

		
		