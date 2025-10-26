import pygame
from random import choice , randint

class Enemy:
	
	def __init__(self , width , height , font , length):
		self.width = width
		self.height = height
		self.font = font
		self.length = length
		with open('text.txt' , 'r' , encoding = 'utf-8') as file:
			list = file.read().splitlines()
		words = [word for word in list if len(word) <= self.length]
		self.word = choice(words)
		color = ['red' , 'green' , 'blue' , 'yellow' , 'cyan' , 'turquoise' , 'deeppink' , 'hotpink' , 'lime' , 'aquamarine' , 'blueviolet' , 'darkolivegreen1' , 'palegreen' , 'orange' , 'gold' , 'lightpink' , 'lightsalmon' , 'lightseagreen']
		self.color = choice(color)
		self.pos = pygame.Vector2(randint(0 , self.width) , 0)
		self.speed = 0
		self.rect = None
	
	def update(self , player , dt):
		direction = (player.pos - self.pos).normalize()
		self.pos += direction * self.speed * dt
	
	def attack(self , player):
		if self.rect is None:
			return 
		elif self.rect:
			collidex = max(self.rect.left , min(player.pos.x , self.rect.right))
			collidey = max(self.rect.top , min(player.pos.y , self.rect.bottom))
			collision = pygame.Vector2(collidex , collidey)
			if collision.distance_squared_to(player.pos) <= player.radius * player.radius:
				player.health = max(0 , player.health - 1)
				return True
			else:
				return False
	
	def collide(self , bullet):
		if self.rect and bullet.rect:
			if self.rect.colliderect(bullet.rect):
				if bullet.letter == self.word[0]:
					self.word = self.word[1:]
				return True
			return False
	
	def isdead(self , player):
		if len(self.word) <= 0:
			player.score += 1
			return True
		return False
	
	def draw(self , surface):
		surf , self.rect = self.font.render(str(self.word) , fgcolor = self.color , size = self.width // 25)
		self.rect.center = self.pos
		surface.blit(surf , self.rect)
		
class Enemies:
		
	def __init__(self , width , height , font):
		self.width = width
		self.height = height
		self.font = font
		self.enemies = []
		self.time = pygame.time.get_ticks()
		self.length = 1
		self.difftime = 2500
		self.speed = 300
	
	def addenemies(self):
		enemy = Enemy(self.width , self.height , self.font , self.length)
		enemy.speed = self.speed
		self.enemies.append(enemy)
	
	def update(self , player , dt):
		for enemy in self.enemies[:]:
			enemy.update(player , dt)
			player.magazine = [bullet for bullet in player.magazine if not enemy.collide(bullet)]
		self.enemies = [enemy for enemy in self.enemies if not enemy.isdead(player) and not enemy.attack(player)]
		self.incdiff(player)
		
	def incdiff(self , player):
		now = pygame.time.get_ticks()
		if (now - self.time) > self.difftime:
			self.time = now
			player.health = min(player.health + 1 , player.maxhealth)
			self.length = min(self.length + 1 , 20)
			self.speed = min(self.speed + 25 , 600)
			self.difftime = min(self.difftime + 2500 , 20000)
			
	def draw(self , surface):
		for enemy in self.enemies:
			enemy.draw(surface)
		