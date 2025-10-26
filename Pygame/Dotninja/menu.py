import pygame
import random
from jnius import autoclass
from android import activity
class Menu:
	def __init__(self,f,white,w,h):
		self.c=white
		self.w=w
		self.h=h
		self.f=f
		self.out=self.f.render('GAME OVER!',False,self.c)
		self.outpos=self.out.get_rect(center=(self.w//2,self.h//3))
		self.restart=self.f.render('TAP TO RESTART',False,self.c)
		self.restartpos=self.restart.get_rect(center=(self.w//2,self.h//1.5))
		self.startrect= self.f.render('TAP TO START' , False , self.c)
		self.startpos = self.startrect.get_rect(center =(self.w//2 , self.h //1.5))
	def start(self , surface):
		if self.blink():
			surface.blit(self.startrect , self.startpos)
	def gameover(self,surface,s):
		surface.blit(self.out,self.outpos)
		if self.blink():
			surface.blit(self.restart,self.restartpos)
		score=self.f.render(f'{s.score}',False,self.c)
		scorepos=score.get_rect(center=(self.w//2,self.h//2))
		surface.blit(score,scorepos)
	def lag(self,surface,c):
		f=int(c.get_fps())
		if f<60:
			fps=self.f.render(f'{f}',False,self.c)
			fpspos=fps.get_rect(center=(self.w-100,100))
			surface.blit(fps,fpspos)
	def blink(self):
		return (pygame.time.get_ticks()//250)%2==0
	def score(self,surface,s):
		point=self.f.render(f'{s.score}',False,self.c)
		pointpos=point.get_rect(center=(100,100))
		surface.blit(point,pointpos)
	def vibrate(self,duration):
		activity=autoclass('org.kivy.android.PythonActivity')
		service=autoclass('android.content.Context')
		build=autoclass('android.os.Build$VERSION')
		vibrator=activity.mActivity.getSystemService(service.VIBRATOR_SERVICE)
		if vibrator.hasVibrator():
			if build.SDK_INT>=26:
				vibration=autoclass('android.os.VibrationEffect')
				effect=vibration.createOneShot(duration,vibration.DEFAULT_AMPLITUDE)
				vibrator.vibrate(effect)
			else:
				vibrator.vibrate(duration)
			
		
		
		
		