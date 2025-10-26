import pygame

class Menu:
	
	def __init__(self , width , height , font):
		self.width = width
		self.height = height
		self.font = font
		self.screen = pygame.display.get_surface()
		self.color = 'white'
		self.startsurf , self.startrect = self.font.render('TAP TO START' , fgcolor = self.color)
		self.startrect.center = (self.width // 2 , self.height // 1.5)
		self.restartsurf , self.restartrect = self.font.render('TAP TO RESTART' , fgcolor = self.color)
		self.restartrect.center = (self.width // 2 , self.height // 1.5)
		self.outsurf , self.outrect = self.font.render('GAME OVER!' , fgcolor = self.color)
		self.outrect.center = (self.width // 2 , self.height // 3)
		self.lastscore = None
		
	def blink(self):
		return (pygame.time.get_ticks() // 350) % 2 == 0
			
	def start(self):
		if self.blink():
			self.screen.blit(self.startsurf , self.startrect)
			
	def restart(self):
		if self.blink():
			self.screen.blit(self.restartsurf , self.restartrect)
		
	def out(self):
		self.screen.blit(self.outsurf , self.outrect)
		
	def score(self , player):
		if player.score != self.score:
			self.lastscore = player.score
			self.scoresurf , self.scorerect = self.font.render(str(self.lastscore) , fgcolor = self.color)
			self.scorerect.center = (100 , 100)
		self.screen.blit(self.scoresurf , self.scorerect)
	
	def totalscore(self):
		self.scorerect.center = (self.width // 2 , self.height // 2)
		self.screen.blit(self.scoresurf , self.scorerect)
		
	def fps(self , clock):
		fps = int(clock.get_fps())
		fpssurf , fpsrect = self.font.render(str(fps) , fgcolor = 'red')
		fpsrect.center = (self.width // 1.2 , 100)
		self.screen.blit(fpssurf , fpsrect)
		
	def gameover(self):
		self.out()
		self.restart()
		self.totalscore()
		
		