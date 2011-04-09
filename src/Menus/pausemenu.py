import pygame
import Menus
import Game
import Resources

RESUME = 1
TITLE = 2

class GamePauseMenu(Game.GameSceneBase):
	
	def __init__(self, currentScene):
		Game.GameSceneBase.__init__(self)
		self.previousScene = currentScene
		self._font = Resources.TTF_Font('Kallamar/KALLAMAR.TTF')
		self.bg = pygame.Surface((640, 480))
		self.bg.set_alpha(50)
		
		self._resume_r = pygame.Rect(0,0,0,0)
		self._title_r = pygame.Rect(0,0,0,0)
		self._hover = None
	
	def ProcessInput(self, events):
		for e in events:
			if e.type == pygame.MOUSEMOTION:
				self._hover = None
				x = e.pos[0]
				y = e.pos[1]
				if self._resume_r.collidepoint(x,y):
					self._hover = RESUME
				elif self._title_r.collidepoint(x,y):
					self._hover = TITLE
			if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
				x = e.pos[0]
				y = e.pos[1]
				if self._resume_r.collidepoint(x,y):
					self.ReturnToGame()
				elif self._title_r.collidepoint(x,y):
					self.ReturnToMainMenu()
			if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				self.ReturnToGame()
	
	def Update(self):
		pass
	
	def ReturnToGame(self):
		self.next = self.previousScene
		self.previousScene.next = self.previousScene
	
	def ReturnToMainMenu(self):
		self.next = Menus.Title()
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
		self.previousScene.Render(self.bg)
		screen.blit(self.bg, (0, 0))
		
		f = self._font.Render
		basic = pygame.Color(255, 255, 255)
		hover = pygame.Color(0, 110, 180)
		t = f('Resume Game', (basic, hover)[self._hover == RESUME])
		x = (640-t.get_width()) / 2
		y = 220
		screen.blit(t, (x, y))
		self._resume_r = pygame.Rect(x, y, t.get_width(), t.get_height())
		t = f('Exit To Main Menu', (basic, hover)[self._hover == TITLE])
		x = (640-t.get_width()) / 2
		y = 220 + 2 * t.get_height()
		screen.blit(t, (x, y))
		self._title_r = pygame.Rect(x, y, t.get_width(), t.get_height())