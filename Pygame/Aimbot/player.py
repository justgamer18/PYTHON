import pygame

class Playerbullet:
	
	def __init__(self , pos , direction):
		self.pos = pos
		dir = direction
		self.angle = dir.angle_to(pygame.Vector2(1 , 0))
		self.direction = dir.copy()
		self.color = 'orange'
		self.speed = 1800
		self.radius = 5
		
	def update(self , dt):
		movement = self.direction.normalize() if self.direction.length() != 0 else pygame.Vector2(-1 , 0)
		self.pos -= movement * self.speed * dt

	def draw(self , surface):
		pygame.draw.circle(surface , self.color , self.pos , self.radius)
		
	
class Playergun:
	
	def __init__(self , pos , width , height):
		self.width = width
		self.height = height
		self.offset = pygame.Vector2(50 , 0)
		self.length = pygame.Vector2(50 , 0)
		self.pos = pos
		self.startpos = self.pos + self.offset
		self.endpos =  self.startpos + self.length
		self.color = 'red'
		self.direction = pygame.Vector2(-1 , 0)
		self.magazine=[]
		
	def update(self , direction , target , isactive ,dt):
		if isactive:
			self.direction = direction.normalize()
		if self.direction.length_squared() != 0:
			angle = self.direction.angle_to(pygame.Vector2(1 , 0))
			rotation = self.offset.rotate(180 - angle ).normalize()
			self.startpos = self.pos + (rotation * self.offset.length())
			self.endpos = self.startpos + (rotation * self.length.length())
		for bullet in self.magazine[:]:
			bullet.update(dt)
		self.magazine = [bullet for bullet in self.magazine if 0 < bullet.pos.x < self.width and 0 < bullet.pos.y < self.height]
				
	def loadbullets(self):
		bullets = Playerbullet(self.endpos , self.direction)
		self.magazine.append(bullets)
		
	def draw(self , surface):
		pygame.draw.line(surface , self.color , self.startpos , self.endpos , 10)
		for bullet in self.magazine:
			bullet.draw(surface)
			
class Aimbotbullet:
	
	def __init__(self , pos , direction):
		self.pos = pos
		dir = direction
		self.angle = dir.angle_to(pygame.Vector2(1 , 0))
		self.direction = dir.copy()
		self.color = 'orange'
		self.speed = 1800
		self.radius = 5
		
	def update(self , dt):
		movement = self.direction.normalize() if self.direction.length() != 0 else pygame.Vector2(-1 , 0)
		self.pos += movement * self.speed * dt
		
	def draw(self , surface):
		pygame.draw.circle(surface , self.color , self.pos , self.radius)
	
			
class Aimbotgun:
	
	def __init__(self , pos , width , height):
		self.width = width
		self.height = height
		self.offset = pygame.Vector2(50 , 0)
		self.length = pygame.Vector2(50 , 0)
		self.pos = pos
		self.startpos = self.pos + self.offset
		self.endpos =  self.startpos + self.length
		self.color = 'red'
		self.direction = pygame.Vector2(-1 , 0)
		self.magazine=[]
		
	def update(self , direction , target , isactive ,dt):
		if isactive and not target.enemies:
			self.direction = direction.normalize()
		elif target.enemies:
			minenemies = min(target.enemies , key = lambda e : e.pos.distance_to(self.pos))
			self.direction = (minenemies.pos - self.pos).normalize()
		if self.direction.length_squared() != 0:
			angle = self.direction.angle_to(pygame.Vector2(1 , 0))
			rotation = self.offset.rotate(- angle ).normalize()
			self.startpos = self.pos + (rotation * self.offset.length())
			self.endpos = self.startpos + (rotation * self.length.length())
		for bullet in self.magazine[:]:
			bullet.update(dt)
		self.magazine = [bullet for bullet in self.magazine if 0 < bullet.pos.x < self.width and 0 < bullet.pos.y < self.height]
				
	def loadbullets(self):
		bullets = Aimbotbullet(self.endpos , self.direction)
		self.magazine.append(bullets)
		
	def draw(self , surface):
		pygame.draw.line(surface , self.color , self.startpos , self.endpos , 10)
		for bullet in self.magazine:
			bullet.draw(surface)

class Player:
	
	def __init__(self , width , height):
		self.width = width
		self.height = height
		self.radius = self.width // 18
		self.color = 'white'
		self.blastradius = self.radius
		self.rgb = 255
		self.minpos = pygame.Vector2(self.radius , self.radius)
		self.maxpos = pygame.Vector2(self.width - (self.radius) , self.height//1.25)
		self.pos = pygame.Vector2(self.width // 2 , self.height // 2)
		self.speed = 600
		gun = [Playergun , Aimbotgun]
		self.gun = gun [1] (self.pos , self.width , self.height)
		self.score = 0
		self.health = 100
		self.maxhealth = 100
		self.target = None
		self.vision = 500
		
	def clamping(self):
		self.pos.x = max(self.minpos.x , min(self.pos.x , self.maxpos.x))
		self.pos.y = max(self.minpos.y , min(self.pos.y , self.maxpos.y))
		
	def update(self , joystick , target , dt):
		self.target = target
		self.clamping()
		direction = joystick.getdirection()
		movement = direction / joystick.baseradius if joystick.isactive else pygame.Vector2()
		self.pos += movement * self.speed * dt
		self.gun.update(direction , target , joystick.isactive , dt)
		
	def healthmeter(self , surface):
		ratio = self.health/self.maxhealth
		minlength = pygame.Vector2(0 , 0)
		maxlength = pygame.Vector2(int(self.health / self.maxhealth * self.width) , 0)
		r = int(255 * (1 - ratio))
		g = int(255 * ratio)
		b = 0
		color = (r , g ,b)
		pygame.draw.line(surface , color , minlength , maxlength , 25)
	
	def shoot(self , sound):
		if self.target and self.target.enemies:
			closest = min(self.target.enemies , key = lambda e : e.pos.distance_to(self.pos))
			if closest.pos.distance_to(self.pos) <= self.vision:
				self.gun.loadbullets()
				sound.play()
				self.shootanimation()
		else:
			return
		
	def isdead(self):
		return self.health <= 0
			
	def shootanimation(self):
		firingradius = 25
		screen = pygame.display.get_surface()
		pygame.draw.circle(screen , 'yellow' , self.gun.endpos  , firingradius)
		
	def draw(self , surface):
		self.healthmeter(surface)
		self.gun.draw(surface)
		pygame.draw.circle(surface , self.color , self.pos , self.radius , 25)
	
	def deathanimation(self , surface , dt):
		self.blastradius += 200 * dt
		self.rgb = max(self.rgb - 250 * dt , 0)
		col = int(self.rgb)
		color = (col , col , col)
		pygame.draw.circle(surface , color , self.pos , self.blastradius , 5)
		
		