from config import *

class Raycast:
	
	def __init__(self , map):
		self.map = map
		self.drawmethod = [self.drawray_dda , self.drawray_grid , self.drawray_bruteforce]
		self.end_pos = pg.Vector2()
		
	def update(self , player):
		self.start_pos = player.pos
		self.angle = player.angle
		
	def castray_grid(self , angle):
		#horizontal_check
		raydir_y = math.sin(angle)
		horizontal_hit = False
		hithorizontal_x = 0
		hithorizontal_y = 0
		
		if raydir_y < 0:
			firsthorizontal_y = ((self.start_pos.y // tile_height) * tile_height) - 0.0001
		elif raydir_y > 0:
			firsthorizontal_y = ((self.start_pos.y // tile_height) * tile_height) + tile_height
		firsthorizontal_x = ((firsthorizontal_y - self.start_pos.y) / math.tan(angle)) + self.start_pos.x
		nexthorizontal_x = firsthorizontal_x
		nexthorizontal_y = firsthorizontal_y
		
		if raydir_y < 0:
			ya = -tile_height
		elif raydir_y > 0:
			ya = tile_height
		xa = ya / math.tan(angle)

		while 0 <= nexthorizontal_x < map_size * tile_width and 0 <= nexthorizontal_y < map_size * tile_height and not horizontal_hit:
			if not self.map.is_collide(nexthorizontal_x , nexthorizontal_y):
				nexthorizontal_x += xa
				nexthorizontal_y += ya
			else:
				hithorizontal_x = nexthorizontal_x
				hithorizontal_y = nexthorizontal_y
				horizontal_hit = True
				
		if horizontal_hit:
			horizontal_distance = point_distance(self.start_pos.x , self.start_pos.y , hithorizontal_x , hithorizontal_y)
		else:
			horizontal_distance = max_depth
				
		#vertical_check
		raydir_x =  math.cos(angle)
		vertical_hit = False
		hitvertical_x = 0
		hitvertical_y = 0
		
		if raydir_x < 0:
			firstvertical_x = ((self.start_pos.x // tile_width) * tile_width) - 0.0001
		elif raydir_x > 0:
			firstvertical_x = ((self.start_pos.x // tile_width) * tile_width) + tile_width
		firstvertical_y = ((firstvertical_x - self.start_pos.x) * math.tan(angle)) + self.start_pos.y
		nextvertical_x = firstvertical_x
		nextvertical_y = firstvertical_y
		
		if raydir_x < 0:
			xa = -tile_width
		elif raydir_x > 0:
			xa = tile_width
		ya = math.tan(angle) * xa
		
		while 0 <= nextvertical_x < map_size * tile_width and 0 <= nextvertical_y < map_size * tile_height and not vertical_hit:
			if not self.map.is_collide(nextvertical_x , nextvertical_y):
				nextvertical_x += xa
				nextvertical_y += ya
			else:
				hitvertical_x = nextvertical_x
				hitvertical_y = nextvertical_y
				vertical_hit = True
				
		if vertical_hit:
			vertical_distance = point_distance(self.start_pos.x , self.start_pos.y , hitvertical_x , hitvertical_y)
		else:
			vertical_distance = max_depth
		
		if horizontal_distance < vertical_distance:
			x = hithorizontal_x
			y = hithorizontal_y
			distance = horizontal_distance
		else:
			x = hitvertical_x
			y = hitvertical_y
			distance = vertical_distance
		
		return pg.Vector2(x , y) , distance
		
	def drawray_grid(self , surface):
		angle = self.angle - half_fov
		for i in range(num_rays):
			ray_angle = normalized_angle(angle + i * step_angle)
			self.end_pos , distance = self.castray_grid(ray_angle)
			#pygame.draw.line(surface , ray_color , self.start_pos , self.end_pos , 1)
			
			corrected_distance = distance * math.cos(self.angle - ray_angle)
			corrected_distance = max(corrected_distance , 0.1)
			projection_height = (tile_height * projection_distance * 0.6) / corrected_distance
			projection_height = min(projection_height , screen_height)
			shade = max(10 , 200 - int(corrected_distance))
			shade_color = color(shade , shade , shade)
			x = int(i * projection_width)
			y = int(screen_height * 0.5 - projection_height * 0.5)
			surface.fill(shade_color , (x , y , int(projection_width) + 1 , projection_height))
	
	def castray_dda(self , angle):
		raydir_x = math.cos(angle)
		map_x = int(self.start_pos.x / tile_width)
		deltadist_x = abs(tile_width / raydir_x) if raydir_x != 0 else float('inf')
		if raydir_x < 0:
			step_x = -1
			sidedist_x = (self.start_pos.x - map_x * tile_width) / abs(raydir_x)
		else:
			step_x = 1
			sidedist_x = ((map_x + 1) * tile_width - self.start_pos.x) / abs(raydir_x)
		
		raydir_y = math.sin(angle)
		map_y = int(self.start_pos.y // tile_height)
		deltadist_y = abs(tile_height / raydir_y) if raydir_y != 0 else float('inf')
		if raydir_y < 0:
			step_y = -1
			sidedist_y = (self.start_pos.y - map_y * tile_height) / abs(raydir_y)
		else:
			step_y = 1
			sidedist_y = ((map_y + 1) * tile_height - self.start_pos.y) / abs(raydir_y)
		
		hit = False
		side = 0
		
		while not hit:
			if sidedist_x < sidedist_y:
				map_x += step_x
				sidedist_x += deltadist_x
				side = 0
			else:
				map_y += step_y
				sidedist_y += deltadist_y
				side = 1
			
			if 0 <= map_x < map_size and 0 <= map_y < map_size:
				if self.map.is_collide(map_x , map_y , False):
					hit = True
				else:
					continue
			else:
				break
		if side == 0:
			distance = (map_x * tile_width - self.start_pos.x + (1 - step_x) * tile_width * 0.5) / raydir_x
		else:
			distance= (map_y * tile_height - self.start_pos.y + (1 - step_y) * tile_height * 0.5) / raydir_y
		distance = min(distance , max_depth)
		x = self.start_pos.x + raydir_x * distance
		y = self.start_pos.y + raydir_y * distance
		
		return pg.Vector2(x , y) , distance
		
	def drawray_dda(self , surface):
		angle = self.angle - half_fov 
		for i in range(num_rays):
			ray_angle = normalized_angle(angle + i * step_angle)
			self.end_pos , distance = self.castray_dda(ray_angle)
			#pygame.draw.line(surface , ray_color , self.start_pos , self.end_pos , 1)
			
			corrected_distance = distance * math.cos(self.angle - ray_angle)
			corrected_distance = max(corrected_distance , 0.1)
			projection_height = (tile_height * projection_distance * 0.6) / corrected_distance
			projection_height = min(projection_height , screen_height)
			shade = max(10 , 200 - int(corrected_distance))
			shade_color = color(shade , shade , shade)
			x = int(i * projection_width)
			y = int(screen_height * 0.5 - projection_height * 0.5)
			surface.fill(shade_color , (x , y , int(projection_width) + 1 , projection_height))

	def castray_bruteforce(self , angle):
		distance = max_depth
		raydir_y = math.sin(angle)
		raydir_x = math.cos(angle)
		for depth in range(0 , max_depth):
			x = self.start_pos.x + raydir_x * depth
			y = self.start_pos.y + raydir_y * depth
			map_x = int(x / tile_width)
			map_y = int(y / tile_height)
			if 0 <= map_x < map_size and 0 <= map_y < map_size:
				if self.map.is_collide(map_x , map_y , False):
					distance = point_distance(self.start_pos.x , self.start_pos.y , x , y)
					return pg.Vector2(x , y) , distance
		return pg.Vector2(self.start_pos.x + raydir_x * max_depth , self.start_pos.y + raydir_y * max_depth) , distance
	
	def drawray_bruteforce(self , surface):
		angle = self.angle - half_fov
		for i in range(num_rays):
			ray_angle = normalized_angle(angle + i * step_angle)
			self.end_pos , distance = self.castray_bruteforce(ray_angle)
			#pygame.draw.line(surface , ray_color , self.start_pos , self.end_pos , 1)
			
			corrected_distance = distance * math.cos(self.angle - ray_angle)
			corrected_distance = max(corrected_distance , 0.1)
			projection_height = (tile_height * projection_distance * 0.6) / corrected_distance
			projection_height = min(projection_height , screen_height)
			shade = max(10 , 200 - int(corrected_distance))
			shade_color = color(shade , shade , shade)
			x = int(i * projection_width)
			y = int(screen_height * 0.5 - projection_height * 0.5)
			surface.fill(shade_color , (x , y , int(projection_width) + 1 , (projection_height)))
		
	def draw(self , surface = screen):
		self.drawmethod[ray_method](surface)