import pygame
from Game import GameSceneBase
import Resources
import Menus
import time

BLAKE = 'Police'
RICHARD = 'Dude1'
ADRIAN = 'Dude2'
CHUN = 'Dude3'
NIELS = 'Dude4'
ANGEL = 'Girl3'
CHRISTINE = 'Girl4'

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

SP_SPEED = 3

#possible modes
WAITING = 1
PRESENT = 2
RETURN  = 3

WALK_COUNT = 65
RETURN_COUNT = WALK_COUNT - 1
FADE_COUNT = 30
TITLE_Y = 200

LINEUP = None
def _lineup():
	global LINEUP
	if not LINEUP:
		LINEUP = {
			ADRIAN : CState(ADRIAN, 290, 218),
			ANGEL : CState(ANGEL, 330, 218),
			RICHARD : CState(RICHARD, 370, 218),
			BLAKE : CState(BLAKE, 410, 218),
			CHUN : CState(CHUN, 450, 218),
			CHRISTINE : CState(CHRISTINE, 490, 218),
			NIELS : CState(NIELS, 530, 218)
		}
	return LINEUP

class Credits(GameSceneBase):
	def __init__(self):
		GameSceneBase.__init__(self)
		
	def ProcessInput(self, events):
		pass

	def Update(self):
		self.next = Programming2()
		#self.next = Art()
		
	def Render(self, screen):
		screen.fill((0, 0, 0))

class CreditsBase(GameSceneBase):		
	def __init__(self):
		GameSceneBase.__init__(self)
		
		self._header_font = Resources.GetFont(255, 0, 0)
		self._font = Resources.GetFont(255, 255, 255)
		self._start_time = time.time()
		self._tick = -1
		self._lineup = _lineup()
		self._blacks = pygame.Surface((220, 310))
	
	def ProcessInput(self, events):	
		for event in events:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				self.next = Menus.Title()
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				self.next = Menus.Title()

	def Update(self):
		self._tick += 1
		if (self._tick == 3):
			self._tick = 0
			for s in self._lineup:
				p = self._lineup[s]
				p.Step()
		else:
			return
	
	def Render(self, screen):
		for p in self._lineup:
			pstate = self._lineup[p]
			screen.blit(pstate.Frame(), pstate.GetPos())
	
	def _MakeHeader(self, txt):
		return self._header_font.Render(txt)
	def _MakeName(self, txt):
		return self._font.Render(txt)
		
	def RenderHeader(self, txt):
		surf = pygame.Surface((len(txt) * 16, 16))
		offset = 0
		for i in range(len(txt)):
			t = self._header_font.Render(txt[i])
			surf.blit(t, (offset, 0))
			offset += 3 + t.get_width()
		return surf.subsurface(pygame.Rect(0,0,offset-3,16))

class CBase2(CreditsBase):
	def __init__(self, header, nameList, pplList):
		CreditsBase.__init__(self)

		self._counter = 0
		self._header = self.RenderHeader(header)
		
		self._names = []
		for name in nameList:
			self._names.append(self._font.Render(name))
		self._people = pplList

	def Update(self):
		CreditsBase.Update(self)
		self._counter += 1
		
	def Render(self, screen):
		screen.fill((0,0,0))
		
		counter = self._counter
		
		screen.blit(self._header, ((200 - self._header.get_width()) / 2, TITLE_Y))
		
		yoffset = TITLE_Y + 20
		for i in range(len(self._names)):
			screen.blit(self._names[i], ((200 - self._names[i].get_width()) / 2, yoffset))
			yoffset += 20
		
		start = 80
		stop = start + WALK_COUNT
		back = stop + 60
		stop2 = back + RETURN_COUNT

		op = (1 - (counter / (2 * FADE_COUNT))) * 255
		if op < 0:
			op = 0
		if op > 255:
			op = 255
		
		if counter >= stop2:
			op = ((counter - 312) / FADE_COUNT) * 255
		
		self._blacks.set_alpha(op)
		screen.blit(self._blacks, (0, 100))

		if (counter == start):
			for p in self._people:
				p.SetMode(PRESENT)
		if (counter == stop):
			for p in self._people:
				p.SetMode(WAITING)
		if (counter == back):
			for p in self._people:
				p.SetMode(RETURN)
		if (counter == stop2):
			for p in self._people:
				p.SetMode(WAITING)
				p.ResetPos()
		
		CreditsBase.Render(self, screen)
		
		if (counter > 340 and op >= 255):
			self.next = self.NextScene()

class Art(CBase2):
	def __init__(self):
		CBase2.__init__(
			self,
			'Art',
			['Angel McLaughlin', 'Niels', 'Chun Y'],
			[_lineup()[ANGEL], _lineup()[NIELS], _lineup()[CHUN]]
			)
	
	def NextScene(self):
		return Music()

class Music(CBase2):
	def __init__(self):
		CBase2.__init__(
			self,
			'Music',
			['Adrian Cline'],
			[_lineup()[ADRIAN]]
		)
	
	def NextScene(self):
		return LevelDesign()

class LevelDesign(CBase2):
	def __init__(self):
		CBase2.__init__(
			self,
			'Level Design',
			['Blake O\'Hare'],
			[_lineup()[BLAKE]]
			)

	def NextScene(self):
		return GameDesign()

class GameDesign(CBase2):
	def __init__(self):
		CBase2.__init__(
			self,
			'Game Design',
			['Chun Y', 'Richard Bailey', 'Blake O\'Hare'],
			[_lineup()[CHUN], _lineup()[RICHARD], _lineup()[BLAKE]]
		)

	def NextScene(self):
		return SpecialThanks()
		
class SpecialThanks(CBase2):
	def __init__(self):
		CBase2.__init__(
			self,
			'Special Thanks To',
			['Christine Sandquist', 'Bad Kitty'],
			[_lineup()[CHRISTINE]]
		)
	
	def NextScene(self):
		return Programming2()

class Programming2(CBase2):
	def __init__(self):
		CBase2.__init__(
			self,
			'Development',
			['Blake O\'Hare', 'Richard Bailey'],
			[_lineup()[BLAKE], _lineup()[RICHARD]]
		)
	
	def NextScene(self):
		return Art()

class Programming(CreditsBase):
	def __init__(self):
		CreditsBase.__init__(self)
		
		self._counter = 0
		self._txt = []
		
		hf = self._header_font.Render
		f = self._font.Render
		self._dev = self.RenderHeader('Development')
		self._names = [
			f('Blake O\'Hare'),
			f('Richard Bailey')
		]
		
		self._t = pygame.Surface((640, 480))

	def Update(self):
		CreditsBase.Update(self)
		self._counter += 1

		
	def Render(self, screen):
		screen.fill((0,0,0))
		
		counter = self._counter
		blake = _lineup()[BLAKE]
		richard = _lineup()[RICHARD]
		
		screen.blit(self._dev, ((200 - self._dev.get_width()) / 2, TITLE_Y))
		screen.blit(self._names[0], ((200 - self._names[0].get_width()) / 2, 220))
		screen.blit(self._names[1], ((200 - self._names[1].get_width()) / 2, 240))

		start = 80
		stop = start + WALK_COUNT
		back = stop + 60
		stop2 = back + RETURN_COUNT
		
		op = (1 - (counter / FADE_COUNT)) * 255
		if op > 255:
			op = 255
		
		if counter >= stop2:
			op = ((counter - 312) / FADE_COUNT) * 255
			
		
		self._blacks.set_alpha(op)
		screen.blit(self._blacks, (0, 100))

		if (counter == start):
			blake.SetMode(PRESENT)
			richard.SetMode(PRESENT)
		if (counter == stop):
			blake.SetMode(WAITING)
			richard.SetMode(WAITING)
		if (counter == back):
			blake.SetMode(RETURN)
			richard.SetMode(RETURN)
		if (counter == stop2):
			blake.SetMode(WAITING)
			blake.ResetPos()
			richard.SetMode(WAITING)
			richard.ResetPos()

		CreditsBase.Render(self, screen)
		
		if (counter > 340 and op >= 255):
			self.next = Art()



# class CState:
	# Step()
	#  -- returns a drawable frame, a
	#  -- advances location
	# Frame()
	# GetPos()
	# SetPos(x, y)
	# Face(direction)
	# SetMode(mode)
	# GetMode()





class CState:
	def __init__(self, name, x, y):
		self.__name = name
		self.__direction = None
		self.__frame = 0
		c = self._cache
		self.__cache = {
			UP    : c( UP),
			DOWN  : c(DOWN),
			RIGHT : c(RIGHT),
			LEFT  : c(LEFT)
		}
		
		self.__mode = WAITING
		self.__modeStart = None
		
		self.__x = x
		self.__y = y
		self.__ox = x
		self.__oy = y
	
		self.__dx = 0
		self.__dy = 0
		
		self.Face(DOWN)
	
	def Name(self):
		return self.__name

	def Frame(self):
		return self.__cache[self.__direction][self.__frame]

	def SetMode(self, mode):
		if (mode == self.__mode):
			self.__mode = WAITING
			self.Face(DOWN)
		else:
			self.__mode = mode	
		if mode == PRESENT or mode == WAITING:
			self.Face(DOWN)
		elif mode == RETURN:
			self.Face(UP)

	def GetMode(self):
		return self.__mode

	def Face(self, direction):
		self.__direction = direction
		self.__frame = 0
		
		if direction == UP:
			self.__dy = -SP_SPEED
			self.__dx = 0
		elif direction == DOWN:
			self.__dy = SP_SPEED
			self.__dx = 0
		elif direction == RIGHT:
			self.__dy = 0
			self.__dx = SP_SPEED
		elif direction == LEFT:
			self.__dy = 0
			self.__dx = -SP_SPEED
	
	def Step(self):
		if self.__mode == WAITING:
			return
		
		self.__frame += 1
		if (self.__frame == 3):
			self.__frame = 0
		
		self.__x += self.__dx
		self.__y += self.__dy
		
		return self.Frame()

	def ResetPos(self):
		self.__x = self.__ox
		self.__y = self.__oy

	def GetPos(self):
		return (self.__x, self.__y)

	def SetPos(self, x, y):
		self.__x = x
		self.__y = y

	def _cache(self, direction):
		person = self.__name
		return [
			Resources.ImageLibrary.Get('Sprites/%s/%s0.png' % (person, direction)),
			Resources.ImageLibrary.Get('Sprites/%s/%s1.png' % (person, direction)),
			Resources.ImageLibrary.Get('Sprites/%s/%s2.png' % (person, direction))
		]