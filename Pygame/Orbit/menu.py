import pygame
class Ui:
	def __init__(self,f):
		self.w,self.h=pygame.display.get_window_size()
		self.font=f;self.currentscore=0
		self.start=self.font.render('TAP TO START',False,'white')
		self.startrect=self.start.get_rect(center=(self.w//2,self.h//1.5))
		self.gameover=self.font.render('GAME OVER!',False,'white')
		self.gameoverrect=self.gameover.get_rect(center=(self.w//2,self.h//3))
		self.restart=self.font.render('TAP TO RESTART',False,'white')
		self.restartrect=self.restart.get_rect(center=(self.w//2,self.h//1.5))
		self.point=self.font.render(f'{self.currentscore}',False,'white')
		self.pointrect=self.point.get_rect(center=(self.w//9,self.w//9))
		self.scorerect=self.point.get_rect(center=(self.w//2,self.h//2))
	def blink(self):return (pygame.time.get_ticks()//250%2)==0
	def fps(self,surface,clock):
		frame=int(clock.get_fps())
		fpssurf=self.font.render(f'{frame}',False,'white')
		fpsrect=fpssurf.get_rect(center=(self.w - self.w//9,self.w//9))
		surface.blit(fpssurf,fpsrect)
	def outupdate(self,surface):
		surface.blit(self.gameover,self.gameoverrect)
		if self.blink():surface.blit(self.restart,self.restartrect)
		surface.blit(self.point,self.scorerect)
	def startupdate(self,surface):
		if self.blink():surface.blit(self.start,self.startrect)
	def scoreupdate(self,surface,spawner,ball):
		spawner.checkscore(ball)
		if self.currentscore!=spawner.score:
			self.currentscore=spawner.score
			self.point=self.font.render(f'{self.currentscore}',False,'white')
		surface.blit(self.point,self.pointrect)
		
		
		