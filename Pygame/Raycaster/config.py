import pygame as pg , math , sys

pg.init()

color = pg.Color
#screen
info = pg.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen_size = (screen_width , screen_height)
screen_color = color('gray4')
fps = 60

screen = pg.display.set_mode(screen_size)
clock = pg.time.Clock()

base = min(screen_width , screen_height)

font_size = base * 0.1
font = pg.freetype.Font(None , font_size)

debug_color = color('red')

#map
map_size = 20
tile_width = base // map_size
tile_height = base // map_size
wall_color = color('grey80')
ground_color = color('grey50')

#joystick
base_radius = base * 0.15
stick_radius = base * 0.1
left_pos = pg.Vector2(screen_width * 0.1 , screen_height * 0.8)
base_thick = 5
right_pos = pg.Vector2(screen_width * 0.83 , screen_height * 0.8)
base_width = base * 0.4
base_height = base * 0.1
base_rect = pg.Rect(0 , 0 , base_width , base_height)
base_rect.center = right_pos
joystick_color = color('grey30')

#player
player_radius = base * 0.005
player_speed = base * 0.0005
player_pos = pg.Vector2(tile_width + 20 , tile_height + 20)
player_color = color('white')
player_angle = math.pi * 0.5
player_rotationspeed = base * 0.0015

#raycast
fov = math.pi * 0.33
half_fov = fov * 0.5
num_rays = 600
step_angle = fov / num_rays
ray_color = color('white')
'''ray_method 
   0 = dda_method
   1 = grid_method
   2 = brureforce_method
'''
ray_method = 0
max_depth = 9999 

#projection
projection_distance = (screen_width * 0.5) / math.tan(half_fov)
projection_width = screen_width / num_rays

#functions
def normalized_angle(angle):
	angle = angle % (2 * math.pi)
	if angle <= 0:
		angle = angle + (2 * math.pi)
	return angle

def point_distance(x1 , y1 , x2 , y2):
	return pg.Vector2(x1 , y1).distance_to(pg.Vector2(x2 , y2))