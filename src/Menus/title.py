import math
from Game import GameSceneBase
from GamePlay import PlayScene
import Menus
import pygame
from Resources import ImageLibrary
import Resources
from GamePlay import LevelSeed

COLOR = [pygame.Color(0, 0, 0), pygame.Color(0, 110, 180)]

NONE = 0
STORY = 1
CUSTOM = 2
INTRO = 3
CREDITS = 4
QUIT = 5

OPTIONS = [
	'',
	'Story Mode',
	'Custom Game',
	'Rewatch Intro',
	'Credits',
	'Quit'
]

class Title(GameSceneBase):
	
	def __init__(self):
		GameSceneBase.__init__(self)
		self.whitefont = Resources.GetFont(255, 255, 255)
		self.yellowfont = Resources.GetFont(255, 255, 0)
		self._font = Resources.TTF_Font('Kallamar/KALLAMAR.TTF', 28)
	
		self.counter = 0
		
		self._story_r = None
		self._custom_r = None
		self._intro_r = None
		self._credits_r = None
		self._quit_r = None
		self._hover = NONE
		
		self.text = Resources.ImageLibrary.Get('txt.png')
		self.shattered = pygame.Surface((435, 117), pygame.SRCALPHA).convert_alpha()
		self.shattered.blit(self.text, (0, 0))
		self.silence = pygame.Surface((286, 124), pygame.SRCALPHA).convert_alpha()
		self.silence.blit(self.text, (-91, -222))
		
	def ProcessInput(self, events):
		for event in events:
			if event.type == pygame.MOUSEMOTION and self._story_r:
				x = event.pos[0]
				y = event.pos[1]
				
				if (self._story_r.collidepoint(x, y)):
					self._hover = STORY
				elif (self._custom_r.collidepoint(x, y)):
					self._hover = CUSTOM
				elif (self._intro_r.collidepoint(x, y)):
					self._hover = INTRO
				elif (self._credits_r.collidepoint(x, y)):
					self._hover = CREDITS
				elif (self._quit_r.collidepoint(x, y)):
					self._hover = QUIT
				else:
					self._hover = NONE

			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				x = event.pos[0]
				y = event.pos[1]
				
				if (self._story_r.collidepoint(x, y)):
					self.next = PlayScene(LevelSeed('level2', None))
				elif (self._custom_r.collidepoint(x, y)):
					self.next = Menus.MapOptions()
				elif (self._intro_r.collidepoint(x, y)):
					self.next = Menus.Intro();
				elif (self._credits_r.collidepoint(x, y)):
					self.next = Menus.Credits()
				elif (self._quit_r.collidepoint(x, y)):
					self.next = None

	def Update(self):
		self.counter += 1
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
		
		v = int(120 + math.sin(self.counter * 3.14159 * 2 / 220.0) * 50)
		pygame.draw.rect(screen, (v, v, v), pygame.Rect(0, 0, 640, 480)) 
		
		screen.blit(self.shattered, (0, 0))
		screen.blit(self.silence, (297, 45))
		
		titleimage = ImageLibrary.Get('title_bg.png')
		screen.blit(titleimage, (0, 0))
		
		f = self._font.Render
		h = self._hover
		x = 44
		y = 316
		text = f('Story Mode', COLOR[h == STORY])
		screen.blit(text, (x, y))
		if (not self._story_r):
			self._story_r = pygame.Rect(x, y, text.get_width(), text.get_height())
		x = 39
		y = 353
		text = f('Custom Game', COLOR[h == CUSTOM])
		screen.blit(text, (x, y))
		if (not self._custom_r):
			self._custom_r = pygame.Rect(x, y, text.get_width(), text.get_height())
		x = 43
		y = 394
		text = f('Rewatch Intro', COLOR[h == INTRO])
		screen.blit(text, (x, y))
		if (not self._intro_r):
			self._intro_r = pygame.Rect(x, y, text.get_width(), text.get_height())
		x = 67
		y = 433
		text = f('Credits', COLOR[h == CREDITS])
		screen.blit(text, (x, y))
		if (not self._credits_r):
			self._credits_r = pygame.Rect(x, y, text.get_width(), text.get_height())
		x = 570
		y = 433
		text = f('Quit', COLOR[h == QUIT])
		screen.blit(text, (x, y))
		if (not self._quit_r):
			self._quit_r = pygame.Rect(x, y, text.get_width(), text.get_height())

		
		#y = 320
		#x = 100
		#for i in range(len(self.options)):
		#	
		#	if i == self.index:
		#		font = self.yellowfont
		#		cursor = font.Render('>')
		#		screen.blit(cursor, (x - 12, y)) 
		#	else:
		#		font = self.whitefont
		#	
		#	screen.blit(font.Render(self.options[i]), (x, y))
		#	y += 20