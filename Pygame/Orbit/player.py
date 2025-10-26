import pygame
class Ball:
	def __init__(self,w,h):
		self.w,self.h=w,h
		self.r=self.w//12
		self.speed = 250
		self.angle=0
		self.pivotpos=pygame.Vector2(self.w//2,self.h//1.5)
		self.offset=pygame.Vector2(self.w//3.5,0)
		self.ballpos1=self.pivotpos+self.offset
		self.ballpos2=self.pivotpos-self.offset
		self.color = 'white'
		self.rgb = 255
	def update(self,tap,dt):
		if tap:
			mx=pygame.mouse.get_pos()[0]
			if mx>self.w//2:self.angle+=self.speed*dt
			elif mx<self.w//2:self.angle-=self.speed*dt
			else:self.angle=0
		rotation=self.offset.rotate(self.angle)
		self.ballpos1=self.pivotpos+rotation
		self.ballpos2=self.pivotpos-rotation
	def draw(self,surface):
		pygame.draw.circle(surface,self.color,self.ballpos1,self.r,10);pygame.draw.circle(surface,self.color,self.ballpos2,self.r,10)
	def collidecheck(self,point,rect):
		closestx=max(rect.left,min(point.x,rect.right));closesty=max(rect.top,min(point.y,rect.bottom))
		colx=point.x-closestx;coly=point.y-closesty
		col=(colx*colx)+(coly*coly);return col<=(self.r*self.r)
	def collide(self,rect):return self.collidecheck(self.ballpos1,rect) or self.collidecheck(self.ballpos2,rect)
	def animation(self,surface):
		if self.pivotpos.y>=self.h//2:
			self.pivotpos.y-=self.h//400
		self.angle+=10
		rotation=self.offset.rotate(self.angle)
		self.ballpos1=self.pivotpos+rotation
		self.ballpos2=self.pivotpos-rotation
		if self.offset.x >= 0:
			self.offset.x-=self.w//350
		self.rgb -= 2.5
		color = max(int(self.rgb) , 0)
		self.color = (color , color , color)
		self.draw(surface)
			
class Ballsprite(pygame.sprite.Sprite):
	def __init__(self,w,h):
		super().__init__()
		self.w,self.h=w,h
		self.size = min(self.w , self.h)
		self.r=self.size//12
		self.speed=self.size//4
		self.angle=0
		self.pivotpos=pygame.Vector2(self.size//2,self.size//1.5)
		self.offset=pygame.Vector2(self.size//3.5,0)
		self.image=pygame.Surface((self.r*2,self.r*2),pygame.SRCALPHA)
		pygame.draw.circle(self.image,'white',(self.r,self.r),self.r,10)
		self.rect1=self.image.get_rect(center=self.pivotpos+self.offset)
		self.rect2=self.image.get_rect(center=self.pivotpos-self.offset)
	def update(self,tap,dt):
		if tap:
			mx=pygame.mouse.get_pos()[0]
			if mx>self.size//2:self.angle+=self.speed*dt
			elif mx<self.size//2:self.angle-=self.speed*dt
			else:self.angle=0
		rotation=self.offset.rotate(self.angle)
		self.rect1.center=self.pivotpos+rotation
		self.rect2.center=self.pivotpos-rotation
	def draw(self,surface):
		surface.blit(self.image,self.rect1);surface.blit(self.image,self.rect2)
	def collidecheck(self,rect,rect2):
		return rect.colliderect(rect2)
	def collide(self,rect):return self.collidecheck(self.rect1,rect) or self.collidecheck(self.rect2,rect)

class Box(pygame.sprite.Sprite):
	def __init__(self,w,h):
		super().__init__()
		self.w,self.h=w,h
		self.size=self.w//7
		self.pivotpos=pygame.Vector2(self.w//2,self.h//1.5)
		self.offset=pygame.Vector2(self.w//3.5,0)
		self.image=pygame.Surface((self.size,self.size))
		pygame.draw.rect(self.image,"white",(0,0,self.size,self.size),10)
		self.image1=self.image.copy()
		self.rect1=self.image1.get_rect(center=self.pivotpos+self.offset)
		self.rect2=self.image1.get_rect(center=self.pivotpos-self.offset)
		self.speed=self.w//4;self.angle=0
		self.rotospeed=260;self.rotoangle=0
	def update(self,hold,dt):
		if hold:
			mx=pygame.mouse.get_pos()[0]
			if mx>self.w//2:self.angle+=self.speed*dt;self.rotoangle+=self.rotospeed*dt
			elif mx<self.w//2:self.angle-=self.speed*dt;self.rotoangle-=self.rotospeed*dt
			else:self.angle=0;self.rotoangle=0
		rotation=self.offset.rotate(self.angle)
		self.image1=pygame.transform.rotozoom(self.image,self.rotoangle,1)
		self.rect1.center=self.pivotpos+rotation
		self.rect2.center=self.pivotpos-rotation
		self.dt = dt
	def draw(self,surface):
		surface.blit(self.image1,self.rect1)
		surface.blit(self.image1,self.rect2)
	def collidecheck(self,rect,rect2):
		return rect.colliderect(rect2)
	def collide(self,rect):return self.collidecheck(self.rect1,rect) or self.collidecheck(self.rect2,rect)

		
		
		
		