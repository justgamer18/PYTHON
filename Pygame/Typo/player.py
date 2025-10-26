import pygame

class Letterbullet:
	
	def __init__(self , width , height , font , pos , letter , direction):
		self.width = width
		self.height = height
		self.font = font
		self.letter = letter
		self.pos = pos
		dir = direction
		self.direction = dir.copy()
		self.surf , self.rect = self.font.render(self.letter , fgcolor = 'orange')
		self.rect.center = self.pos
		self.movement = self.direction.normalize() if self.direction.length_squared() != 0 else pygame.Vector2(0 , -1)
		self.speed = 1200
	
	def update(self , dt):
		self.pos += self.movement * self.speed * dt
		self.rect.center = self.pos
	
	def draw(self , surface):
		surface.blit(self.surf , self.rect)
		
class Player:
	
	def __init__(self , width , height):
		self.width = width
		self.height = height
		self.radius = self.width // 25
		self.pos = pygame.Vector2(self.width // 2 , self.height // 1.5)
		self.length = pygame.Vector2(0 , - 75)
		self.endpos = self.pos + self.length
		self.color = 'white'
		self.direction = pygame.Vector2(0 , - 1)
		self.magazine = []
		self.health = 1
		self.maxhealth = 5
		self.blastradius = self.radius
		self.rgb = 255
		self.score = 0
		
	def update(self , target , dt):
		if target.enemies is None:
			self.direction = self.direction.normalize()
		elif target.enemies:
			minenemies = min(target.enemies , key = lambda x : x.pos.distance_to(self.pos))
			self.direction = minenemies.pos - self.pos
		if self.direction.length_squared() != 0:
			angle = self.direction.normalize().angle_to(pygame.Vector2(0 , -1))
			rotation = self.length.rotate(-angle)
			self.endpos = self.pos + rotation
		for letter in self.magazine:
			letter.update(dt)
		self.magazine = [letter for letter in self.magazine if 0 < letter.pos.x < self.width and 0 < letter.pos.y < self.height]

	def loadbullet(self , font , letter):
		bullet = Letterbullet(self.width , self.height , font , self.endpos , letter , self.direction)
		self.magazine.append(bullet)
	
	def shoot(self , font , letter , sound):
		self.loadbullet(font , letter)
		sound.play()
		self.shootanimation()
		
	def shootanimation(self):
		screen = pygame.display.get_surface()
		radius = 30
		pygame.draw.circle(screen , 'yellow' , self.endpos , radius)
		
	def healthmeter(self , surface):
		ratio = self.health / self.maxhealth
		minlength = pygame.Vector2(0 , 0)
		maxlength = pygame.Vector2(int(self.health / self.maxhealth * self.width) , 0)
		r = int(255 * (1 - ratio))
		g = int(255 * ratio)
		b = 0
		color = (r , g , b)
		pygame.draw.line(surface , color , minlength , maxlength , 25)
		
	def isdead(self):
		return self.health <= 0
	
	def deathanimation(self , surface , dt):
		self.blastradius += 200 * dt
		self.rgb = max(self.rgb - 250 * dt , 0)
		col = int(self.rgb)
		color = (col , col , col)
		pygame.draw.circle(surface , color , self.pos , self.blastradius , 5)
		
	def draw(self , surface):
		self.healthmeter(surface)
		pygame.draw.circle(surface , self.color , self.pos , self.radius)
		pygame.draw.line(surface , self.color , self.pos , self.endpos , 10)
		for bullet in self.magazine:
			bullet.draw(surface)