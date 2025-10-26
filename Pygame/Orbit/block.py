import pygame,random
class Block(pygame.sprite.Sprite):
	def __init__(self,w,h):
		super().__init__()
		self.w,self.h=w,h
		self.width=self.w//2;self.height=self.h//25
		color=['cyan','yellow','lime','magenta','deeppink','hotpink','springgreen','red','blue','green','orange','turquoise1']
		x=[self.width // 2 , self.w - self.width // 2]
		self.x=random.choice(x)
		self.color=random.choice(color)
		self.image=pygame.Surface((self.width,self.height))
		self.image.fill(self.color)
		self.rect=self.image.get_rect(center=(self.x,0))
		self.speed=0;self.isscore=False
	def update(self,dt):
		self.rect.y+=self.speed*dt
		if self.rect.y>self.h:self.kill()
class Spawner:
	def __init__(self,w,h):
		self.w,self.h=w,h
		self.blocks=pygame.sprite.Group()
		self.speed=self.h*0.4
		self.difftime=pygame.time.get_ticks()
		self.lastblock=None
		self.score=0
	def addblock(self):block=Block(self.w,self.h);self.blocks.add(block);self.lastblock=block
	def move(self,dt):
		for block in self.blocks:block.speed = self.speed
		self.blocks.update(dt)
	def draw(self,surface):self.blocks.draw(surface)
	def incdiff(self,ball,dt):
		now=pygame.time.get_ticks()
		if (now-self.difftime)>1000:self.difftime=now;self.speed+=10;ball.speed+=2.5
	def collision(self,ball):return any(ball.collide(b.rect) for b in self.blocks)
	def update(self,surface,ball,dt):self.move(dt);self.draw(surface);self.incdiff(ball,dt);self.collision(ball)
	def isspawn(self):return not (self.lastblock) or (self.lastblock.rect.y)>=self.h//4
	def checkscore(self,ball):
		for b in self.blocks:
			if b.rect.y>ball.pivotpos.y+ball.offset.y and not b.isscore:
				self.score+=1
				b.isscore=True
		
		
		
	
		
	
		
		