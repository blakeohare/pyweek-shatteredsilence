"""
It's natural to fear change.
"""

import pygame
import Menus
import Game
import Resources

WHITE = 1
RED = 2
YELLOW = 3

class GameWin(Game.GameSceneBase):
	def __init__(self, currentScene):
		Game.GameSceneBase.__init__(self)
		self.previousScene = currentScene
		self.bg = pygame.Surface((640, 480))
		
		self._fontof = Resources.GetFont(220,220,255)
		self._fontw = Resources.GetFont(255,255,255)
		self._fontr = Resources.GetFont(255,0,0)
		self._fonty = Resources.GetFont(255,255,0)
		self._counter = 0
		
		self._done = False
		
		pygame.mixer.music.stop()
		
	def Render(self, screen):
		cnt = self._counter
		
		bg_fade_time = 80
		delay = 15
		
		fade1Done = bg_fade_time
		fade2Start = fade1Done + delay
		fade2Done = fade2Start + 80
		
		
		if cnt <= fade1Done:
			screen.fill((0, 0, 0))
			op = _f2op(1 - _op(cnt, fade1Done))
			self.bg.set_alpha(op)
			
			if op > 0:
				self.previousScene.Render(self.bg)
				screen.blit(self.bg, (0,0))
				return
		
		if cnt < fade2Start:
			screen.fill((0,0,0))
			return
		
		bgimg = Resources.ImageLibrary.Get('MapOptions/sc4.png')
		if cnt >= fade2Start and cnt <= fade2Done:
			screen.fill((0, 0, 0))
			offset_cnt = cnt - fade2Start
			op = _f2op(_op(offset_cnt, bg_fade_time))
			self.bg.blit(bgimg, (0,0))
			self.bg.set_alpha(op)
			screen.blit(self.bg, (0, 0))
			return

		screen.blit(bgimg, (0,0))
		
		txt = self._fontof.Render("A winner is you.", 2)
		screen.blit(txt, (_gcxpx(250, txt), 50))
		self._done = True

	def ProcessInput(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
				self.RollCredits()
			if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				self.RollCredits()

	def Concat(self, lines):
		wd = 0
		h = 0
		for l in lines:
			wd += l.get_width()
			h = l.get_height()
		surf = pygame.Surface((wd, h))
		
		offset = 0
		for l in lines:
			surf.blit(l, (offset, 0))
			offset += l.get_width()
		
		return surf

	def MakeText(self, txt, color = WHITE):
		if color == WHITE:
			f = self._fontw.Render
		elif color == RED:
			f = self._fontr.Render
		elif color == YELLOW:
			f = self._fonty.Render
		return f(txt)
	
	def Update(self):
		self._counter += 1

	def RollCredits(self):
		self.next = Menus.Credits()

def _gcxpx(px, s2):
	return (px - s2.get_width()) // 2

def _gcx(s1, s2):
	return (s1.get_width() - s2.get_width()) // 2
	
def _op(counter, frame):
	op = (float(counter) / frame)
	if (op < 0):
		op = 0
	if (op > 1):
		op = 1
	return op

def _f2op(op):
	op = op * 255
	if (op < 0):
		return 0
	if (op >= 255):
		return 255
	return op