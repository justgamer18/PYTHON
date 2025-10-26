from config import *

class Player:
	
	def __init__(self , map):
		self.map = map
		self.pos = player_pos
		self.angle = player_angle
		
	def is_move(self , pos):
		return not self.map.is_collide(pos.x , pos.y , True)
	
	def update_movement(self , joystick , dt):
		direction = joystick.get_left_direction().rotate_rad(normalized_angle(self.angle - math.pi * 1.5))
		move = direction * player_speed * dt if joystick.is_left_active else pg.Vector2()
		newpos_x = pg.Vector2(self.pos.x + move.x , self.pos.y)
		if self.is_move(newpos_x):
			self.pos.x = newpos_x.x
		newpos_y = pg.Vector2(self.pos.x , self.pos.y + move.y)
		if self.is_move(newpos_y):
			self.pos.y = newpos_y.y
			
	def update_angle(self , joystick , dt):
		direction = joystick.get_right_direction()
		self.angle += direction * player_rotationspeed * dt if joystick.is_right_active else 0
	
	def update(self , joystick , dt):
		self.update_movement(joystick , dt)
		self.update_angle(joystick , dt)

	def draw(self , surface = screen):
		pg.draw.circle(surface , player_color , self.pos , player_radius)
		#pygame.draw.line(surface , color('red') , self.pos , (self.pos.x + math.cos(self.angle) *50 , self.pos.y + math.sin(self.angle) *50) , 5)