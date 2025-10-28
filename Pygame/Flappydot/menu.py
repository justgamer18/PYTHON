import pygame
#from jnius import autoclass
#from android import activity
class Menu:
	def __init__(self,c,w,h,f):
		self.white=c.white
		self.t=pygame.time.get_ticks()
		self.font=f
		self.w=w
		self.h=h
		self.out=self.font.render("GAME OVER!",False,self.white)
		self.outpos=self.out.get_rect(center=(self.w//2,self.h//3))
		self.restart=self.font.render("TAP TO RESTART",False,self.white)
		self.restartpos=self.restart.get_rect(center=(self.w//2,self.h//1.5))
		self.start=self.font.render('TAP TO START' , False , self.white)
		self.startpos = self.start.get_rect(center =(self.w//2 , self.h // 1.5))
		
	def blink(self):
		return (pygame.time.get_ticks()//250%2==0)
	def lag(self,surface,clock):
		frame=int(clock.get_fps())
		lag=self.font.render(f'{frame}',False,self.white)
		lagpos=lag.get_rect(center=(self.w-100,100))
		surface.blit(lag,lagpos)
	def score(self,surface,player,spawner):
		spawner.checkscore(player)
		point=self.font.render(f"{spawner.score}",False,self.white)
		pointpos=point.get_rect(center=(100,100))
		surface.blit(point,pointpos)
	def gameover(self,surface,spawner):
		surface.blit(self.out,self.outpos)
		p=self.font.render(f'{spawner.score}',False,self.white)
		ppos=p.get_rect(center=(self.w//2,self.h//2))
		surface.blit(p,ppos)
		if self.blink():
			surface.blit(self.restart,self.restartpos)
	def starter(self , surface):
		if self.blink():
			surface.blit(self.start , self.startpos)
	# def vibrate(self,duration):
	# 	activity=autoclass('org.kivy.android.PythonActivity')
	# 	service=autoclass('android.content.Context')
	# 	build=autoclass('android.os.Build$VERSION')
	# 	vibrator=activity.mActivity.getSystemService(service.VIBRATOR_SERVICE)
	# 	if vibrator.hasVibrator():
	# 		if build.SDK_INT>=26:
	# 			vibration=autoclass('android.os.VibrationEffect')
	# 			effect=vibration.createOneShot(duration,vibration.DEFAULT_AMPLITUDE)
	# 			vibrator.vibrate(effect)
	# 		else:
	# 			vibrator.vibrate(duration)
			
		

		
		