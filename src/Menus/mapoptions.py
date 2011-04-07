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

class MapOptions(GameSceneBase):
	def __init__(self):
		GameSceneBase.__init__(self)
		self._font = Resources.TTF_Font('Kallamar/KALLAMAR.TTF', 36)
		self._page = 0 # which BG page we're on
		self._bg = Resources.ImageLibrary.Get('MapOptions/sc1.png') # Background to draw
		self._args = {}
		
		self._map_sz1 = None
		self._map_size = 1
		self._font_r = None

		
		#animation related
		self._transitioning = False #should we be animating to the next option screen?
		
		# set stuff up
		self._SetDefaults()
	
	def ProcessInput(self, events):
			if (self._page == 0):
				self._MapUIInput(events)
				return

			for event in events:
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_RIGHT):
						self._page += 1
						if (self._page >= 4):
							self._page = 0
					elif (event.key == pygame.K_LEFT):
						self._page -= 1
						if (self._page < 0):
							self._page = 3
					elif (event.key == pygame.K_RETURN):
						self.next = PlayScene(LevelSeed(None, self._args))
	
	def Update(self):
		pass
	
	def Render(self, screen):
		screen.blit(self._bg, (0, 0))
		text = self._font.Render("Next")
		fx = _GetCenterX(screen, text)
		screen.blit(text, (fx, 400))
		if not self._font_r:
			self._font_r = pygame.Rect(fx, 400, text.get_width(), text.get_height())

		p = self._page
		if p == 0:
			surf = self._BuildMapUI(screen)

		elif p == 1:
			text = "Progress Mode"
		elif p == 2:
			text = "Time Limit"
		elif p == 3:
			text = "Zoom Level"
	
	
	
# Private methods

	def _NextPage(self):
		self._page += 1

	def _BuildMapUI(self, screen):
		gcy = _GetCenterY
		gcx = _GetCenterX
		
		text = self._font.Render("Map Size")
		screen.blit(text, (gcx(screen, text), 50))
		yoffset = 50 + text.get_height()

		
		if not self._map_sz1:
			self._map_sz1 = Resources.ImageLibrary.Get('MapOptions/sz1.png')
			self._map_sz2 = Resources.ImageLibrary.Get('MapOptions/sz2.png')
			self._map_sz3 = Resources.ImageLibrary.Get('MapOptions/sz3.png')
			self._map_sz1_selected = Resources.ImageLibrary.Get('MapOptions/sz1_selected.png')
			self._map_sz2_selected = Resources.ImageLibrary.Get('MapOptions/sz2_selected.png')
			self._map_sz3_selected = Resources.ImageLibrary.Get('MapOptions/sz3_selected.png')
		sz1 = self._map_sz1
		sz2 = self._map_sz2
		sz3 = self._map_sz3
		if self._map_size == 1:
			sz1 = self._map_sz1_selected
		elif self._map_size == 2:
			sz2 = self._map_sz2_selected
		elif self._map_size == 3:
			sz3 = self._map_sz3_selected
		
		screen.blit(sz1, (180, yoffset + 20))
		self._sz1_r = pygame.Rect(180, yoffset + 20, sz1.get_width(), sz1.get_height())
		
		screen.blit(sz2, (275, yoffset + 20))
		self._sz2_r = pygame.Rect(275, yoffset + 20, sz2.get_width(), sz2.get_height())
		
		screen.blit(sz3, (390, yoffset + 20))
		self._sz3_r = pygame.Rect(390, yoffset + 20, sz3.get_width(), sz3.get_height())
		
		yoffset += 20 + sz3.get_height()
	
	def _MapUIInput(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
				x = e.pos[0]
				y = e.pos[1]
				if (self._font_r.collidepoint(x, y)):
					self._NextPage()
				elif (self._sz1_r.collidepoint(x, y)):
					self._map_size = 1
				elif (self._sz2_r.collidepoint(x, y)):
					self._map_size = 2
				elif (self._sz3_r.collidepoint(x, y)):
					self._map_size = 3
			
	
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

# Utility methods
def _GetCenterX(surf1, surf2):
	return (surf1.get_width() - surf2.get_width()) / 2

def _GetCenterY(surf1, surf2):
	return (surf1.get_height() - surf2.get_height()) / 2