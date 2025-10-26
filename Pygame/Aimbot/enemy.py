import pygame
from random import randint , choice

class Enemy:
	
	def __init__(self , width , height):
		self.width = width
		self.height = height
		color = ['red' , 'green' , 'blue' , 'yellow' , 'cyan' , 'turquoise' , 'deeppink' , 'hotpink' , 'lime' , 'aquamarine' , 'blueviolet' , 'darkolivegreen1' , 'palegreen' , 'orange' , 'gold' , 'lightpink' , 'lightsalmon' , 'lightseagreen']
		self.color = choice(color)
		self.radius = self.width // 22
		self.speed = 300
		side = choice(['top' , 'bottom' , 'left' , 'right'])
		if side in ['top' , 'bottom']:
			self.x = randint(0 , self.width)
			self.y = -(self.radius) if side == 'top' else self.height + (self.radius)
		elif side in ['left' , 'right']:
			self.x = -(self.radius) if side == 'left' else self.width + (self.radius)
			self.y = randint(0 , self.height)
		self.pos = pygame.Vector2(self.x , self.y)
		self.shrink = True
	
	def animation(self , dt):
		minrad = self.width // 35
		maxrad = self.width // 25
		animationspeed = 50
		if self.shrink:
			self.radius -= animationspeed * dt
			if self.radius <= minrad:
				self.radius = minrad
				self.shrink = False
		else:
			self.radius += animationspeed * dt
			if self.radius >= maxrad:
				self.radius = maxrad
				self.shrink = True
	
	def update(self , target , dt):
		self.animation(dt)
		direction = target.pos - self.pos
		if direction.length_squared() != 0:
			direction = direction.normalize()
			self.pos += direction * self.speed * dt
		
	def collide(self , target):
		return self.pos.distance_to(target.pos) <= self.radius + target.radius
			
	def draw(self , surface):
		pygame.draw.circle(surface , self.color , self.pos , self.radius)
	
class Enemies:
	
	def __init__(self , width , height):
		self.width = width 
		self.height = height
		self.enemies = []
		self.damage = 2
		self.maxenemies = 1
		self.time = pygame.time.get_ticks()
		self.difftime = 1000
		
	def addenemies(self):
		if len(self.enemies) < self.maxenemies:
			enemy = Enemy(self.width , self.height)
			self.enemies.append(enemy)
		
	def update(self , player , dt):
		self.incdiff()
		for enemy in self.enemies[:]:
			enemy.update(player , dt)
			for bullet in player.gun.magazine[:]:
				if enemy.collide(bullet):
					if enemy in self.enemies:
						self.enemies.remove(enemy)
					player.gun.magazine.remove(bullet)
					player.score += 1
			if enemy.collide(player):
				player.health = max(0 , player.health - self.damage * dt)
	
	def incdiff(self):
		now = pygame.time.get_ticks()
		if (now - self.time) > self.difftime:
			self.time = now
			self.maxenemies = min(self.maxenemies + 1 , 50)
			self.difftime = min(self.difftime + 1000 , 10000)
			
	def draw(self , surface):
		for enemy in self.enemies:
			enemy.draw(surface)
