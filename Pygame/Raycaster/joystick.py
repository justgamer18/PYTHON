from config import *

class Joystick:
	
	def __init__(self):
		self.leftstick_pos = left_pos
		self.rightstick_pos = right_pos
		self.leftfinger_pos = pg.Vector2()
		self.rightfinger_pos = pg.Vector2()
		self.is_left_active = False
		self.is_right_active = False
		self.left_id = None
		self.right_id = None
		self.color = joystick_color
		
	def is_left_touch(self , touch_pos):
		return (touch_pos - left_pos).length() <= stick_radius
		
	def is_right_touch(self , touch_pos):
		return base_rect.collidepoint(touch_pos)
		
	def handle_event(self , event):
		if event.type == pg.FINGERDOWN:
			fx = event.x * screen_width
			fy = event.y * screen_height
			touch_pos = pg.Vector2(fx , fy)
			if self.is_left_touch(touch_pos) and self.left_id == None:
				self.left_id = event.finger_id
				self.is_left_active = True
				self.leftfinger_pos = touch_pos
			elif self.is_right_touch(touch_pos) and self.right_id == None:
				self.right_id = event.finger_id
				self.is_right_active = True
				self.rightfinger_pos = touch_pos
			
		elif event.type == pg.FINGERMOTION:
			if event.finger_id == self.left_id:
				fx = event.x * screen_width
				fy = event.y * screen_height
				self.leftfinger_pos = pg.Vector2(fx , fy)
			elif event.finger_id == self.right_id:
				fx = event.x * screen_width
				fy = event.y * screen_height
				self.rightfinger_pos = pg.Vector2(fx , fy)
				
		elif event.type == pg.FINGERUP:
			if event.finger_id == self.left_id:
				self.left_id = None
				self.is_left_active = False
			elif event.finger_id == self.right_id:
				self.right_id = None
				self.is_right_active = False
	
	def get_left_direction(self):
		direction = self.leftfinger_pos - left_pos
		mindistance = min(direction.length() , base_radius)
		if direction.length() != 0:
			direction = direction.normalize() * mindistance
			return direction
		return pg.Vector2()
	
	def get_right_direction(self):
		direction = self.rightfinger_pos.x - base_rect.centerx
		self.half_width = base_rect.width * 0.5
		mindistance = max(-self.half_width , min(direction , self.half_width))
		direction = mindistance / self.half_width
		return direction
		
	def update_left(self):
		self.leftstick_pos = left_pos + self.get_left_direction() if self.is_left_active else left_pos	
	
	def update_right(self):
		self.rightstick_pos = pg.Vector2(right_pos.x + self.get_right_direction() * self.half_width , right_pos.y) if self.is_right_active else pg.Vector2(right_pos)
		
	def draw_left(self , surface):
		pg.draw.circle(surface , self.color , left_pos , base_radius , base_thick)
		pg.draw.circle(surface , self.color , self.leftstick_pos , stick_radius)
		
	def draw_right(self , surface):
		pg.draw.rect(surface , self.color , base_rect , base_thick , 100)
		pg.draw.circle(surface , self.color , self.rightstick_pos , stick_radius)
		
	def update(self):
		self.update_left()
		self.update_right()
		
	def draw(self , surface = screen):
		self.draw_left(surface)
		self.draw_right(surface)