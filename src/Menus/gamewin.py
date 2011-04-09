import pygame
import Menus
import Game
import Resources

WHITE = 1
RED = 2
YELLOW = 3
OFFWHITE = 4
GREEN = 5

BG_FADE_TIME = 80
TEXT_FADE_SPEED = 30
READ_DELAY = 60

class GameWin(Game.GameSceneBase):
	def __init__(self, cur):
		Game.GameSceneBase.__init__(self)
		self.cur = cur
	
	def ProcessInput(self, events):
		pass
	
	def Update(self):
		self.next = Win1(self.cur)
	
	def Render(self, screen):
		self.cur.Render(screen)

class GameWinBase(Game.GameSceneBase):
	def __init__(self):
		Game.GameSceneBase.__init__(self)
		self._fontof = Resources.GetFont(220,220,255)
		self._fontw = Resources.GetFont(255,255,255)
		self._fontr = Resources.GetFont(255,0,0)
		self._fonty = Resources.GetFont(255,255,0)
		self._fontg = Resources.GetFont(0, 255, 0)
		self._counter = 0
		
		self._advance = None

		pygame.mixer.music.stop()
		
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

	def MakeText(self, txt, color = WHITE, kern = 0):
		if color == WHITE:
			f = self._fontw.Render
		elif color == OFFWHITE:
			f = self._fontof.Render
		elif color == RED:
			f = self._fontr.Render
		elif color == YELLOW:
			f = self._fonty.Render
		elif color == GREEN:
			f = self._fontg.Render
		return f(txt, kern)
	
	def Update(self):
		self._counter += 1
		if self._advance:
			self.next = self._advance

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

def _dupe(surf):
	return pygame.Surface((surf.get_width(), surf.get_height()))


def _drawon(target, text, loc, op):
	s = _dupe(text)
	s.set_alpha(op)
	s.blit(
		target.subsurface(pygame.Rect(
			loc[0], loc[1],
			text.get_width(), text.get_height())), 
		(0,0))
	s.blit(text, (0,0))
	target.blit(s, loc)


# prev -> black
class Win1(GameWinBase):
	def __init__(self, curScene):
		GameWinBase.__init__(self)
		self.previousScene = curScene
		self.bg = pygame.Surface((640, 480))
		
	def Render(self, screen):
		cnt = self._counter
		
		delay = 15
		fade1Done = BG_FADE_TIME
		
		if cnt <= fade1Done:
			screen.fill((0, 0, 0))
			op = _f2op(1 - _op(cnt, BG_FADE_TIME))
			self.bg.set_alpha(op)
			
			if op > 0:
				self.previousScene.Render(self.bg)
				screen.blit(self.bg, (0,0))
				return
		self._advance = Win2()

# black bg, + text
class Win2(GameWinBase):
	def __init__(self):
		GameWinBase.__init__(self)
		self.bg = pygame.Surface((640, 480))
		self.line1 = self.Concat([
			self.MakeText("It's natural to resist "),
			self.MakeText("change", YELLOW),
			self.MakeText(".")])
		self.line2 = self.Concat([
			self.MakeText("It's natural to "),
			self.MakeText("fear", RED),
			self.MakeText(" the unknown", YELLOW),
			self.MakeText(".")
			])
		self.line3 = self.MakeText("And yet ")
		self.line4 = self.MakeText("that doesn't mean it's right.")
	

	def Render(self, screen):
		cnt = self._counter
		l1 = self.line1
		l2 = self.line2
		l3 = self.line3
		l4 = self.line4
		
		screen.fill((0,0,0))
		
		readDelay = READ_DELAY
		line1Enter = 0
		line1Fin = TEXT_FADE_SPEED
		line2Enter = line1Fin + readDelay
		line2Fin = line2Enter + TEXT_FADE_SPEED
		line3Enter = line2Fin + readDelay
		line3Fin = line3Enter + TEXT_FADE_SPEED
		line4Enter = line3Enter + (readDelay // 2)
		line4Fin = line4Enter + TEXT_FADE_SPEED
		finalFade = line4Fin + int(2.2 * readDelay)
		progress = finalFade + TEXT_FADE_SPEED

		l1p = (144, 130)
		l2p = (180, 160)
		l3p = (220, 190)
		l4p = (220 + l3.get_width(), l3p[1])

		if cnt < line1Fin:
			surf = _dupe(l1)
			surf.set_alpha(_f2op(_op(cnt, TEXT_FADE_SPEED)))
			surf.blit(l1, (0,0))
			screen.blit(surf, l1p)
			return
		elif cnt < finalFade:
			screen.blit(l1, l1p)
			
		if cnt < line2Enter:
			return

		if cnt < line2Fin:
			ocnt = cnt - line2Enter
			surf = _dupe(l2)
			surf.set_alpha(_f2op(_op(ocnt, TEXT_FADE_SPEED)))
			surf.blit(l2, (0,0))
			screen.blit(surf, l2p)
			return
		elif cnt < finalFade:
			screen.blit(l2, l2p)
		
		if cnt < line3Enter:
			return

		if cnt < line3Fin:
			ocnt = cnt - line3Enter
			surf = _dupe(l3)
			surf.set_alpha(_f2op(_op(ocnt, TEXT_FADE_SPEED)))
			surf.blit(l3, (0,0))
			screen.blit(surf, l3p)
			return
		elif cnt < finalFade:
			screen.blit(l3, l3p)
		
		if cnt < line4Fin:
			ocnt = cnt - line4Enter
			surf = _dupe(l4)
			surf.set_alpha(_f2op(_op(ocnt, TEXT_FADE_SPEED)))
			surf.blit(l4, (0,0))
			screen.blit(surf, l4p)
			return
		elif cnt < finalFade:
			screen.blit(l4, l4p)
		
		if cnt >= finalFade:
			ocnt = cnt - finalFade
			op = _f2op(1 - _op(ocnt, TEXT_FADE_SPEED))

			s = _dupe(l1)
			s.set_alpha(op)
			s.blit(l1, (0,0))
			screen.blit(s, l1p)
			s = _dupe(l2)
			s.set_alpha(op)
			s.blit(l2, (0,0))
			screen.blit(s, l2p)
			s = _dupe(l3)
			s.set_alpha(op)
			s.blit(l3, (0,0))
			screen.blit(s, l3p)
			s = _dupe(l4)
			s.set_alpha(op)
			s.blit(l4, (0,0))
			screen.blit(s, l4p)
		
		if cnt >= progress:
			if not self._advance:
				self._advance = Win3(self)

# black -> bg
class Win3(GameWinBase):
	def __init__(self, bg):
		GameWinBase.__init__(self)
		self.bg = pygame.Surface((640, 480))
		
	def Render(self, screen):
		cnt = self._counter
		
		fadeDone = 80
		
		bgimg = Resources.ImageLibrary.Get('MapOptions/sc4.png')
		if cnt <= fadeDone:
			screen.fill((0, 0, 0))
			op = _f2op(_op(cnt, BG_FADE_TIME))
			self.bg.blit(bgimg, (0,0))
			self.bg.set_alpha(op)
			screen.blit(self.bg, (0, 0))
			return

		screen.blit(bgimg, (0,0))
		if not self._advance:
			self._advance = Win5()

class Win5(GameWinBase):
	def __init__(self):
		GameWinBase.__init__(self)
		self.bg = pygame.Surface((640, 480))
		self.bg.fill((0,0,0))
		
		c = OFFWHITE
		self.line1 = self.MakeText('All that was lost will never be restored', c, 1)
		self.line2 = self.MakeText('And the battle is not yet fully won', c, 1)
		self.line3 = self.MakeText('But at last there is ', c, 1)
		self.line4 = self.MakeText('hope', GREEN, 1)
		self.line5 = self.MakeText('.', c, 1)

	def Render(self, screen):
		cnt = self._counter
		
		l1 = self.line1
		l2 = self.line2
		l3 = self.line3
		l4 = self.line4
		l5 = self.line5
		
		l1p = (90, 175)
		l2p = (155, 230)
		l3p = (260, 285)
		l4p = (l3p[0] + l3.get_width(), l3p[1])
		l5p = (l4p[0] + l4.get_width(), l3p[1])
		
		fspeed = int(TEXT_FADE_SPEED * 1.5)
		
		line1Start = 0
		line1Fin = fspeed
		line2Start = line1Fin + READ_DELAY
		line2Fin = line2Start + fspeed
		line3Start = line2Fin + READ_DELAY
		line3Fin = line3Start + fspeed
		line4Start = line3Fin + (READ_DELAY // 4)
		line4Fin = line4Start + fspeed
		line5Start = line4Fin
		line5Fin = line5Start + fspeed
		
		fadeStart = line5Fin + (2 * READ_DELAY)
		fadeFin = fadeStart + fspeed
		
		hopeFadeStart = fadeFin + (READ_DELAY // 2)
		hopeFadeFin = hopeFadeStart + fspeed
		
		progress = fadeFin + fspeed
		
		bgimg = Resources.ImageLibrary.Get('MapOptions/sc4.png')
		screen.blit(bgimg, (0,0))
		
		l = l1
		p = l1p
		if cnt < line1Fin:
			ocnt = cnt - line1Start
			op = _f2op(_op(ocnt, fspeed))
			_drawon(screen, l, p, op)
			return
		elif cnt < fadeStart:
			screen.blit(l, p)
		
		l = l2
		p = l2p
		if cnt < line2Fin:
			ocnt = cnt - line2Start
			op = _f2op(_op(ocnt, fspeed))
			_drawon(screen, l, p, op)
			return
		elif cnt < fadeStart:
			screen.blit(l, p)			
		
		l = l3
		p = l3p
		if cnt < line3Fin:
			ocnt = cnt - line3Start
			op = _f2op(_op(ocnt, fspeed))
			_drawon(screen, l, p, op)
			return
		elif cnt < fadeStart:
			screen.blit(l, p)
		
		l = l4
		p = l4p
		if cnt < line4Fin:
			ocnt = cnt - line4Start
			op = _f2op(_op(ocnt, fspeed))
			_drawon(screen, l, p, op)
			return
		elif cnt < fadeStart:
			screen.blit(l, p)
			
		l = l5
		p = l5p
		if cnt < line5Fin:
			ocnt = cnt - line5Start
			op = _f2op(_op(ocnt, fspeed))
			_drawon(screen, l, p, op)
			return
		elif cnt < fadeStart:
			screen.blit(l, p)

		if cnt < fadeFin:
			ocnt = cnt - fadeStart
			op = _f2op(1 - _op(ocnt, fspeed))
			_drawon(screen, l1, l1p, op)
			_drawon(screen, l2, l2p, op)
			_drawon(screen, l3, l3p, op)
			_drawon(screen, l5, l5p, op)
		screen.blit(l4, l4p)
		
		if cnt >= progress:
			if not self._advance:
				self._advance = Win4(screen)



#fill screen
#bg.set-alpha
#fill the bg
#blit the bg


class Win4(GameWinBase):
	def __init__(self, bg):
		GameWinBase.__init__(self)
		self.bg = pygame.Surface((640, 480))
		self.bg.fill((0,0,0))
		self.prev = bg
		self.preHope = self.MakeText('But at last there is ', GREEN, 1)
		self.hope = self.MakeText('hope', GREEN, 1)

	def Render(self, screen):
		cnt = self._counter
		fadeDone = BG_FADE_TIME
		
		bgimg = Resources.ImageLibrary.Get('MapOptions/sc4.png')

		l3p = (260, 285)
		l4p = (l3p[0] + self.preHope.get_width(), 285)
		bgimg.blit(self.hope, l4p)

		if cnt < fadeDone:
			screen.fill((0,0,0))
			offsetcnt = cnt
			op = _f2op(1 - _op(offsetcnt, BG_FADE_TIME))
			self.bg.set_alpha(op)
			self.bg.blit(bgimg, (0,0))
			screen.blit(self.bg, (0,0))
			return
		
		if not self._advance:
			self._advance = Menus.Credits()