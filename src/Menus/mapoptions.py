import Menus
import time
import pygame
from Game import GameSceneBase
from GamePlay import PlayScene
import Resources
from GamePlay import LevelSeed
import MapGen

# Option stages
# Size
# Progress + Time
# Zoom level

ANIMATION_TIME = 500 #ms
ZOOM_LEVELS = [
	'House',
	'Street',
	'Neighborhood',
	'City',
	'State',
	'Region',
	'Country',
	'Continent',
	'World'
]

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
HOVER = pygame.Color(0, 110, 180)

NONE = 0
MAP_NEXT = 1
PROG_NEXT = 2
ZOOM_START = 3
ARROW_LEFT = 4
ARROW_RIGHT = 5

class MapOptions(GameSceneBase):
	def __init__(self):
		GameSceneBase.__init__(self)
		self._font = Resources.TTF_Font('Kallamar/KALLAMAR.TTF', 36)
		self._page = 0 # which BG page we're on
		self._bg = Resources.ImageLibrary.Get('MapOptions/sc2.png') # Background to draw
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

		self._zoom_level = 2
		self._zoom_size = 0
		self._zoom_right_r = None
		self._zoom_left_r = None

		
		#animation related
		self._transitioning = False #should we be animating to the next option screen?
		self._animStart = None
		self._nextbg = None #next background
		self._curScreenCache = None # previous bg
		self._hover = None

		# set stuff up
		self._SetDefaults()
	
	def ProcessInput(self, events):
		
		for event in events:
			if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
				self.next = Menus.Title()
		
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
			surf = self._Animate(self._curScreenCache, self._nextbg, self._animStart, time.time(), ANIMATION_TIME)
			if surf:
				screen.blit(surf, (0, 0))
				return
		
		screen.blit(self._bg, (0, 0))
		
		p = self._page
		if p == 0:
			self._BuildMapUI(screen)
		elif p == 1:
			self._BuildProgTimeUI(screen)
		elif p == 2:
			self._BuildZoomUI(screen)
	
		self._curScreenCache = screen.copy()
	
	
# Private methods

	def _Animate(self, frame1, frame2, startTime, curTime, totalTimeMS):
		delta = curTime - startTime
		pctDone = delta / (totalTimeMS / 1000.0)
		
		if (pctDone >= 1):
			return None
		
		surf = pygame.Surface((640, 480))
		offset = int(pctDone * 640)
		
		surf.blit(frame1, (0, 0), pygame.Rect(offset, 0, 640 - offset, 480))
		surf.blit(frame2, (640 - offset, 0), pygame.Rect(0, 0, offset, 480))
		
		return surf

	def _StartGame(self):
		gameBuilder = MapGen.CustomGameBuilder(self._args)
		self.next = gameBuilder.GetPlayScene()

	def _NextPage(self):
		if (self._page == 2):
			#TODO: animate transition to game-start
			#self._transitioning = True
			#self._animStart = time.time()
			self._UpdateArgs()
			self._StartGame()
		else:
			self._transitioning = True
			self._animStart = time.time()
			self._page += 1
			self._nextbg = pygame.Surface((640, 480))
			if (self._page == 1):
				self._bg = Resources.ImageLibrary.Get('MapOptions/sc3.png')
				self._nextbg.blit(self._bg, (0,0))
				self._BuildProgTimeUI(self._nextbg)
			elif (self._page == 2):
				self._bg = Resources.ImageLibrary.Get('MapOptions/sc4.png')
				self._nextbg.blit(self._bg, (0,0))
				self._BuildZoomUI(self._nextbg)

	def _BuildZoomUI(self, screen):
		gcy = _GetCenterY
		gcx = _GetCenterX
		
		text = self._font.Render("Start", (WHITE, HOVER)[self._hover == ZOOM_START])
		nextx = _GetCenterX(screen, text)
		screen.blit(text, (nextx, 400))
		self._font_r = pygame.Rect(nextx, 400, text.get_width(), text.get_height())

		text = self._font.Render("Zoom Level", BLACK)
		screen.blit(text, (gcx(screen, text), 50))
		yoffset = 50 + text.get_height()

		if self._zoom_size == 0:
			for s in ZOOM_LEVELS:
				t = self._font.Render(s).get_width()
				if t > self._zoom_size:
					self._zoom_size = t
		
		zsz = self._font.Render(ZOOM_LEVELS[self._zoom_level], BLACK)
		x = gcx(screen, zsz)
		screen.blit(zsz, (x, yoffset + 30))
		
		x1 = ((640 - self._zoom_size)/2) - self._time_left.get_width() - 20
		surf = (self._time_left, self._time_left_hover)[self._hover == ARROW_LEFT]
		screen.blit(surf, (x1, yoffset + 30))
		if (not self._zoom_left_r):
			self._zoom_left_r = pygame.Rect(x1, yoffset+30, self._time_left.get_width(), self._time_left.get_height())
		
		x2 = x1 + self._time_left.get_width() + self._zoom_size + 40
		surf = (self._time_right, self._time_right_hover)[self._hover == ARROW_RIGHT]
		screen.blit(surf, (x2, yoffset + 30))
		if (not self._zoom_right_r):
			self._zoom_right_r = pygame.Rect(x2, yoffset+30, self._time_right.get_width(), self._time_right.get_height())

		yoffset += 55
		
		self._screen_cache = screen.copy()
		
	def _ZoomLevelUIInput(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
				if not self._zoom_left_r:
					return
				x = e.pos[0]
				y = e.pos[1]
				if (self._font_r.collidepoint(x, y)):
					self._NextPage()
				elif (self._zoom_left_r.collidepoint(x, y)):
					self._decZoom()
				elif (self._zoom_right_r.collidepoint(x, y)):
					self._incZoom()
			if e.type == pygame.MOUSEMOTION:
				self._hover = None
				if not self._zoom_left_r:
					return
				x = e.pos[0]
				y = e.pos[1]
				if (self._font_r.collidepoint(x, y)):
					self._hover = ZOOM_START
				elif (self._zoom_left_r.collidepoint(x, y)):
					self._hover = ARROW_LEFT
				elif (self._zoom_right_r.collidepoint(x, y)):
					self._hover = ARROW_RIGHT
	
	def _incZoom(self):
		self._zoom_level += 1
		if self._zoom_level >= len(ZOOM_LEVELS):
			self._zoom_level = 0
	
	def _decZoom(self):
		self._zoom_level -= 1
		if self._zoom_level < 0:
			self._zoom_level = (len(ZOOM_LEVELS) - 1)

	def _BuildProgTimeUI(self, screen):
		gcy = _GetCenterY
		gcx = _GetCenterX
		
		text = self._font.Render("Next", (WHITE, HOVER)[self._hover == PROG_NEXT])
		nextx = _GetCenterX(screen, text)
		screen.blit(text, (nextx, 400))
		if not self._font_r:
			self._font_r = pygame.Rect(nextx, 400, text.get_width(), text.get_height())

		
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
			self._time_right_hover = Resources.ImageLibrary.Get('MapOptions/prog-time/right_hover.png')
			self._time_left_hover = Resources.ImageLibrary.Get('MapOptions/prog-time/left_hover.png')
		
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
		
		text = self._font.Render("Time Limit")
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
		surf = (self._time_left, self._time_left_hover)[self._hover == ARROW_LEFT]
		screen.blit(surf, (fx, y))
		if not self._time_left_r:
			self._time_left_r = pygame.Rect(fx, y, self._time_left.get_width(), self._time_left.get_height())
			
		fx = base + unl_width + delta
		surf = (self._time_right, self._time_right_hover)[self._hover == ARROW_RIGHT]
		screen.blit(surf, (fx, y))
		if not self._time_right_r:
			self._time_right_r = pygame.Rect(fx, y, self._time_right.get_width(), self._time_right.get_height())
		

	def _ProgTimeUIInput(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
				if not self._mode_cont_r:
					return
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
			elif e.type == pygame.MOUSEMOTION:
				self._hover = None
				if not self._time_left_r:
					return
				x = e.pos[0]
				y = e.pos[1]
				if (self._font_r.collidepoint(x, y)):
					self._hover = PROG_NEXT
				elif (self._time_left_r.collidepoint(x, y)):
					self._hover = ARROW_LEFT
				elif (self._time_right_r.collidepoint(x, y)):
					self._hover = ARROW_RIGHT

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
		
		text = self._font.Render("Next", (WHITE, HOVER)[self._hover == MAP_NEXT])
		nextx = _GetCenterX(screen, text)
		screen.blit(text, (nextx, 400))
		if not self._font_r:
			self._font_r = pygame.Rect(nextx, 400, text.get_width(), text.get_height())
		
		text = self._font.Render("Map Size", WHITE)
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
			if e.type == pygame.MOUSEMOTION:
				self._hover = NONE
				x = e.pos[0]
				y = e.pos[1]
				if (self._font_r and self._font_r.collidepoint(x, y)):
					self._hover = MAP_NEXT
			if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
				if (not self._font_r):
					return
				
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
			
	
	def _UpdateArgs(self):
		a = self._args
		if self._map_size == 1:
			a['width'] = 40
			a['height'] = 40
		elif self._map_size == 2:
			a['width'] = 64
			a['height'] = 64
		elif self._map_size == 3:
			a['width'] = 80
			a['height'] = 80
		
		a['map_size'] = self._map_size
		
		a['minutes'] = self._time
		
		if self._zoom_level < 4: # Room -> Neighborhood
			a['mode'] = 'individual'
		elif self._zoom_level < 7: # City -> Country
			a['mode'] = 'crowd'
		else: # Continent + World	
			a['mode'] = 'region'
		a['zoom_level'] = self._zoom_level
		
		a['progress'] = (self._mode == 2)
			
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