import time
import pygame
from Game import GameSceneBase
from GamePlay import PlayScene
import Resources
from GamePlay import LevelSeed

# Option stages
# Size
# Progress + Time
# Zoom level

ANIM_TIME = 4000 #ms

class MapOptions(GameSceneBase):
	def __init__(self):
		GameSceneBase.__init__(self)
		self._font = Resources.TTF_Font('Kallamar/KALLAMAR.TTF', 36)
		self._page = 0 # which BG page we're on
		self._bg = Resources.ImageLibrary.Get('MapOptions/sc1.png') # Background to draw
		self._args = {}
		
		self._map_size = 1
		self._map_sz1 = None
		self._font_r = None
		
		self._mode = 2
		self._mode_cont = None
		self._mode_cont_r = None
		self._mode_zoom_r = None
		
		self._time = -1
		self._time_right_r = None
		self._time_left_r = None

		
		#animation related
		self._transitioning = False #should we be animating to the next option screen?
		self._animStart = None
		
		# set stuff up
		self._SetDefaults()
	
	def ProcessInput(self, events):
		if (self._page == 0):
			self._MapUIInput(events)
		elif (self._page == 1):
			self._ProgTimeUIInput(events)			  
		elif (self._page == 2):
			self._ZoomLevelUIInput(events)
	
	def Update(self):
		pass
	
	def Render(self, screen):
		if (self._transitioning):
			screen.blit(self._screen_cache, (0, 0))
			delta = time.time() - self._animStart
			pct = delta * 1000 / ANIM_TIME
			if (pct > 1):
				pct = 1
			al = 255 * pct
			print("_bg.set_alpha(%s)" % al)
			self._bg.set_alpha(al)
			screen.blit(self._bg, (0, 0))
			return

		else:
			screen.blit(self._bg, (0, 0))
		
		if (self._page == 2):
			text = self._font.Render('Start')
		else:
			text = self._font.Render("Next")
			
		fx = _GetCenterX(screen, text)
		screen.blit(text, (fx, 400))
		if not self._font_r or self._page == 2:
			self._font_r = pygame.Rect(fx, 400, text.get_width(), text.get_height())

		p = self._page
		if p == 0:
			self._BuildMapUI(screen)

		elif p == 1:
			self._BuildProgTimeUI(screen)

		elif p == 2:
			self._BuildZoomUI(screen)
	
	
	
# Private methods

	def _NextPage(self):
		if (self._page == 2):
			print("TODO: update args")
			print("TODO: set next scene")
			print("TODO: animate transition to game-start")
			self._transitioning = True
			self._animStart = time.time()
		else:
			self._page += 1

	def _BuildZoomUI(self, screen):
		gcy = _GetCenterY
		gcx = _GetCenterX
		
		text = self._font.Render("Zoom Level")
		screen.blit(text, (gcx(screen, text), 50))
		yoffset = 50 + text.get_height()
		
		screen.blit(self._mode_cont_selected, (150, 150))
		
		self._screen_cache = screen.copy()
		
	def _ZoomLevelUIInput(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
				x = e.pos[0]
				y = e.pos[1]
				if (self._font_r.collidepoint(x, y)):
					self._NextPage()

	def _BuildProgTimeUI(self, screen):
		gcy = _GetCenterY
		gcx = _GetCenterX
		
		text = self._font.Render("Game Mode")
		screen.blit(text, (gcx(screen, text), 50))
		yoffset = 50 + text.get_height()
		
		if not self._mode_cont:
			self._mode_cont = Resources.ImageLibrary.Get('MapOptions/prog-time/continuous.png')
			self._mode_zoom = Resources.ImageLibrary.Get('MapOptions/prog-time/progress.png')
			self._mode_cont_selected = Resources.ImageLibrary.Get('MapOptions/prog-time/continuous_selected.png')
			self._mode_zoom_selected = Resources.ImageLibrary.Get('MapOptions/prog-time/progress_selected.png')
			self._time_right = Resources.ImageLibrary.Get('MapOptions/prog-time/right.png')
			self._time_left = Resources.ImageLibrary.Get('MapOptions/prog-time/left.png')
		
		cont = self._mode_cont
		zoom = self._mode_zoom
		
		if (self._mode == 1):
			cont = self._mode_cont_selected
		elif (self._mode == 2):
			zoom = self._mode_zoom_selected
		
		x = (640 - 2 * cont.get_width()) / 2 - 18
		y = yoffset + 20
		screen.blit(cont, (x, y))
		if (not self._mode_cont_r):
			self._mode_cont_r = pygame.Rect(x, y, cont.get_width(), cont.get_height())
		
		x += cont.get_width() + 18
		screen.blit(zoom, (x, y))
		if (not self._mode_zoom_r):
			self._mode_zoom_r = pygame.Rect(x, y, cont.get_width(), cont.get_height())
		
		yoffset = y + cont.get_height()
		
		text = self._font.Render("Time Limit", pygame.Color(255, 255, 255))
		screen.blit(text, (gcx(screen, text), 230))
		yoffset = 230 + text.get_height()
		
		text = self._font.Render("Untimed")
		base = gcx(screen, text)
		unl_width = text.get_width()
		
		if (self._time != -1):
			text = self._font.Render("%d min" % self._time)
		screen.blit(text, (gcx(screen, text), yoffset + 30))
		
		delta = 40
		fx = base - self._time_left.get_width() - delta
		y = yoffset + 30
		screen.blit(self._time_left, (fx, y))
		if not self._time_left_r:
			self._time_left_r = pygame.Rect(fx, y, self._time_left.get_width(), self._time_left.get_height())
			
		fx = base + unl_width + delta
		screen.blit(self._time_right, (fx, y))
		if not self._time_right_r:
			self._time_right_r = pygame.Rect(fx, y, self._time_right.get_width(), self._time_right.get_height())
		

	def _ProgTimeUIInput(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
				x = e.pos[0]
				y = e.pos[1]
				if (self._font_r.collidepoint(x, y)):
					self._NextPage()
				elif (self._mode_cont_r.collidepoint(x, y)):
					self._mode = 1
				elif (self._mode_zoom_r.collidepoint(x, y)):
					self._mode = 2
				elif (self._time_right_r.collidepoint(x, y)):
					self._incTime()
				elif (self._time_left_r.collidepoint(x, y)):
					self._decTime()
				
	def _incTime(self):
		if (self._time == -1):
			self._time = 2
		elif (self._time < 10):
			self._time += 1
		elif (self._time < 30):
			self._time += 5
		else:
			self._time = -1
			
	def _decTime(self):
		if (self._time == -1):
			self._time = 30
		elif (self._time == 2):
			self._time = -1
		elif (self._time <= 10):
			self._time -= 1
		elif (self._time <= 30):
			self._time -= 5


	def _BuildMapUI(self, screen):
		gcy = _GetCenterY
		gcx = _GetCenterX
		
		text = self._font.Render("Map Size")
		screen.blit(text, (gcx(screen, text), 50))
		yoffset = 50 + text.get_height()

		
		if not self._map_sz1:
			self._map_sz1 = Resources.ImageLibrary.Get('MapOptions/map-size/sz1.png')
			self._map_sz2 = Resources.ImageLibrary.Get('MapOptions/map-size/sz2.png')
			self._map_sz3 = Resources.ImageLibrary.Get('MapOptions/map-size/sz3.png')
			self._map_sz1_selected = Resources.ImageLibrary.Get('MapOptions/map-size/sz1_selected.png')
			self._map_sz2_selected = Resources.ImageLibrary.Get('MapOptions/map-size/sz2_selected.png')
			self._map_sz3_selected = Resources.ImageLibrary.Get('MapOptions/map-size/sz3_selected.png')

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