import pygame
import random
class Fruit:
	def __init__(self,c,w,h):
		self.c=c
		self.w=w
		self.h=h
		self.r=random.randint(self.w//13,self.w//11)
		self.colour=random.choice(self.c)
		self.x=random.randint(100,self.w-100)
		if self.x>self.w//2:
			self.velx=random.randint(-5,0)
		else:
			self.velx=random.randint(0,5)
		self.y=self.h+self.r
		self.vely=random.randint(-self.h//35,-self.h//50)
		self.gravity=1
	def update(self):
		self.vely+=self.gravity
		self.x+=self.velx
		self.y+=self.vely
	def draw(self,surface):
		pygame.draw.circle(surface,self.colour,(self.x,self.y),self.r)
	def collision(self,tap):
		if tap:
			mx,my=pygame.mouse.get_pos()
			colx=self.x-mx
			coly=self.y-my
			col=(colx*colx)+(coly*coly)
			return col<=(self.r*self.r)*2.5
		return False
class Spawner:
	def __init__(self,c,w,h,):
		self.c=c
		self.bomb=pygame.Color('white')
		self.w=w
		self.h=h
		self.diff=self.h//200
		self.difftime=pygame.time.get_ticks()
		self.fruits=[]
		self.score=0
	def addfruits(self):
		fruit=Fruit(self.c,self.w,self.h)
		self.fruits.append(fruit)
	def remove(self):
		for f in self.fruits[:]:
			if f.y>=self.h+(3*f.r):
				self.fruits.remove(f)	
				return f.colour!=self.bomb
		return False	
	def update(self):
		for f in self.fruits:
			f.update()
	def draw(self,surface):
		for f in self.fruits:
			f.draw(surface)
	def iscollide(self,tap):
		for f in self.fruits[:]:
			if f.collision(tap):
				self.fruits.remove(f)
				if f.colour==self.bomb:
					return False
				self.score+=1
		return True
	def isspawn(self):
		return not self.fruits or self.fruits[-1].y<self.h//self.diff
	def incdiff(self):
		now=pygame.time.get_ticks()
		if now-self.difftime>500:
			self.difftime=now
			self.diff=max(2,self.diff-0.2)
	def out(self,tap):
		return self.remove() or not self.iscollide(tap)
		
		