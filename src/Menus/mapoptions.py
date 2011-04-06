import time
import pygame
from Game import GameSceneBase
from GamePlay import PlayScene
import Resources
from GamePlay import LevelSeed

# Option stages
# Size
# Progress
# Time
# Zoom level

RIGHT = 1
LEFT = 2
ANIMATION_TIME = 2500 #ms

class MapOptions(GameSceneBase):
	def __init__(self):
		GameSceneBase.__init__(self)
		self._font = Resources.TTF_Font('Kallamar/KALLAMAR.TTF', 30)
		self._images = [
			'sc1.png',
			'sc2.png',
			'sc3.png',
			'sc4.png'
		]
		self._page = 0 # which BG page we're on
		self._bg = Resources.ImageLibrary.Get('MapOptions/%s' % self._images[self._page]) # Background to draw
		self._args = {}
		
		#animation related
		self._transitioning = False #should we be animating to the next option screen?
		self._direction = None # which direction should we transition in?
		self._animStart = None
		self._nextbg = None #next background
		
		# set stuff up
		self._SetDefaults()
	
	def ProcessInput(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_RIGHT):
					self._NextPage()
				elif (event.key == pygame.K_LEFT):
					self._PrevPage()
				elif (event.key == pygame.K_RETURN):
					self.next = PlayScene(LevelSeed(None, self._args))
	
	def Update(self):
		pass
	
	
	def Render(self, screen):
		if (self._transitioning):
			composite = self._BuildFrame(self._bg, self._nextbg, self._direction, self._animStart, time.time(), ANIMATION_TIME)
		
			if composite:
				screen.blit(composite, (0, 0))
				return
			else:
				self._StopAnimation()

		screen.blit(self._bg, (0, 0))
		text = self._font.Render("Just press enter for now")
		screen.blit(text, (10, 10))
		
	
	def _StopAnimation(self):
		self._bg = self._nextbg
		self._nextbg = None
		self._direction = None
		self._animStart = None
		self._transitioning = False

	def _BuildFrame(self, frame1, frame2, direction, startTime, curTime, totalTimeMS):
		delta = curTime - startTime
		pctDone = delta / (totalTimeMS / 1000)
		
		if (pctDone >= 1):
			return None
		
		surf = pygame.Surface((640, 480))
		offset = int(pctDone * 640)
		
		if (direction == RIGHT):
			surf.blit(frame1, (0, 0), pygame.Rect(offset, 0, 640 - offset, 480))
			surf.blit(frame2, (640 - offset, 0), pygame.Rect(0, 0, offset, 480))
		else:
			surf.blit(frame1, (0 + offset, 0), pygame.Rect(0, 0, 640 - offset, 480))
			frame2 = frame2.subsurface(pygame.Rect(640 - offset, 0, offset, 480))
			surf.blit(frame2, (0, 0))
		
		return surf
		
	
	def _NextPage(self):
		self._page += 1
		if (self._page >= len(self._images)):
			self._page = 0
		self._nextbg = Resources.ImageLibrary.Get('MapOptions/%s' % self._images[self._page])
		self._transitioning = True
		self._direction = RIGHT
		self._animStart = time.time()
	
	def _PrevPage(self):
		self._page -= 1
		if (self._page < 0):
			self._page = (len(self._images) - 1)
		self._nextbg = Resources.ImageLibrary.Get('MapOptions/%s' % self._images[self._page])
		self._transitioning = True
		self._direction = LEFT
		self._animStart = time.time()
	
	def _SetDefaults(self):
		self._args = {
			'width' : 64, #these are tiles, not pixels
			'height' : 64,
			'mode' : 'individual', # individual, crowd, or region
			'progress' : False, # True if you want to move up to the next zoom level when you complete 80% conversion
			'minutes' : -1, # -1 for un-timed mode. Otherwise, it's the number of minutes you have to complete 80% conversion
			
			# individual mode settings
			'citizens' : 100,
			'police' : 20,
			
			# crowd mode settings
			'city_centers' : 1
			
			# region mode settings
			# ????????
		}