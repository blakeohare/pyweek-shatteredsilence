import pygame
import Menus
import Game
import Resources

WHITE = 1
RED = 2
YELLOW = 3

class GameOver(Game.GameSceneBase):
	def __init__(self, currentScene):
		Game.GameSceneBase.__init__(self)
		self.previousScene = currentScene
		self.bg = pygame.Surface((640, 480))
		
		self._fontw = Resources.GetFont(255,255,255)
		self._fontr = Resources.GetFont(255,0,0)
		self._fonty = Resources.GetFont(255,255,0)
		self._counter = 0
		
		pygame.mixer.music.stop()
		
		self.line1 = self.Concat([
			self.MakeText("Despite your efforts people remained "),
			self.MakeText("terrified", YELLOW),
			self.MakeText(" of the past,")
		])
		self.line2 = self.MakeText("insistent that learning from it meant forsaking all it contained ")
		self.line3 = self.Concat([
			self.MakeText("out of "),
			self.MakeText("fear", RED),
			self.MakeText(" of repeating its mistakes.")
		])
		self.line4 = self.MakeText("GAME OVER", RED)

	def Render(self, screen):
		fade1Done = 80
		text_fade = 60
		delay = 0
		
		startText = fade1Done + delay
		
		l1_startText = startText
		l2_startText = l1_startText + text_fade
		l3_startText = l2_startText + text_fade
		l4_startText = l3_startText + (int(1.3 * text_fade))
		
		cnt = self._counter
		
		screen.fill((0, 0, 0))
		
		if cnt <= fade1Done:
			op = (1 - (float(cnt) / fade1Done)) * 255
			if op > 255:
				op = 255
			if op < 0:
				op = 0

			self.bg.set_alpha(op)
			
			if op > 0:
				self.previousScene.Render(self.bg)
				screen.blit(self.bg, (0,0))
				return
		else:
			self.bg.set_alpha(0)
		screen.blit(self.bg, (0, 0))
		
		bg = self.bg
		bg.set_alpha(0)
		
		l1 = self.line1
		l2 = self.line2
		l3 = self.line3
		l4 = self.line4
	
		if False:
			if cnt >= l1_startText:
				txtcnt = (cnt - l1_startText)
				op = makealpha(txtcnt, text_fade)
				print("op: %d" % op)
				l1.set_alpha(op)
				screen.blit(l1, (_gcx(bg, l1), 100))
			
			if cnt >= l2_startText:
				txtcnt = (cnt - l2_startText)
				op = makealpha(txtcnt, text_fade)
				#print("txtcnt: %d, text_fade: %d, op: %d" % (txtcnt, text_fade, op))
				l2.set_alpha(op)
				screen.blit(l2, (_gcx(bg, l2), 120))
			
			if False and cnt >= l3_startText:
				txtcnt = (cnt - l3_startText)
				op = makealpha(txtcnt, text_fade)
				l3.set_alpha(op)
				screen.blit(l3, (_gcx(bg, l3), 140))
			
			if cnt >= l4_startText:
				screen.blit(l4, (_gcx(bg, l4), 180))
		else:
			if cnt >= l1_startText:
				screen.blit(l1, (_gcx(bg, l1), 100))
			
			if cnt >= l2_startText:
				screen.blit(l2, (_gcx(bg, l2), 120))
			
			if cnt >= l3_startText:
				screen.blit(l3, (_gcx(bg, l3), 140))
			
			if cnt >= l4_startText:
				screen.blit(l4, (_gcx(bg, l4), 180))

	
	def ProcessInput(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
				self.ReturnToMainMenu()
			if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				self.ReturnToMainMenu()

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

	def ReturnToMainMenu(self):
		self.next = Menus.Title()
	
def _gcx(s1, s2):
	return (s1.get_width() - s2.get_width()) / 2
	
def makealpha(counter, frame):
	op = (float(counter) / frame) * 255
	if (op < 0):
		op = 0
	if (op > 255):
		op = 255
	return op
