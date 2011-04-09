import pygame
from Game import GameSceneBase
import Resources
import Menus

_useFancyRender = False

_font = None
def FancyRender(text, color):
	global _font
	if _font == None:
		_font = Resources.TTF_Font('Kallamar/KALLAMAR.TTF', 18)
		
	c = pygame.Color(color[0], color[1], color[2])
	return _font.Render(text, c)

class Intro(GameSceneBase):
	def __init__(self):
		GameSceneBase.__init__(self)
	
	def ProcessInput(self, events):
		pass
	
	def Update(self):
		self.next = IntroA()
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
		

class IntroBase(GameSceneBase):
	def __init__(self):
		GameSceneBase.__init__(self)
		self.counter = 0
		self.text_blits = []
	
	def ProcessInput(self, events):
		skip = False
		for event in events:
			
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				skip = True
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				skip = True
		
		if skip:
			self.next = Menus.Title()
	
	def Update(self):
		self.counter += 1
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
	
	def ConcatenateImages(self, image_list):
		image = image_list[0]
		while len(image_list) > 1:
			a = image
			b = image_list[1]
			newimage = pygame.Surface((a.get_width() + b.get_width(), a.get_height()), pygame.SRCALPHA).convert_alpha()
			newimage.blit(a, (0, 0))
			newimage.blit(b, (a.get_width(), 0))
			image = newimage.convert_alpha()
			image_list[1] = image
			image_list = image_list[1:]
		return image
	
	def MakeText(self, color, text):
		global _useFancyRender
		if _useFancyRender:
			return FancyRender(text, color)
		else:
			font = Resources.GetFont(color[0], color[1], color[2])
			return font.Render(text).convert_alpha()
	
	def BlitText(self, text_image, loc, opacity):
		if opacity < 0: opacity = 0
		if opacity > 255: opacity = 255
		
		self.text_blits.append((text_image, loc, opacity))
	
	def DoBlits(self, screen):
		
		for blit in self.text_blits:
			image = blit[0]
			loc = blit[1]
			x = loc[0]
			y = loc[1]
			opacity = blit[2]
			
			if blit[2] == 255:
				screen.blit(image, loc)
			else:
				temp = pygame.Surface((image.get_width(), image.get_height()))
				temp.blit(screen, (-x, -y))
				temp.set_alpha(255 - opacity)
				screen.blit(image, loc)
				screen.blit(temp, loc)
		
		self.text_blits = []
		
		
class IntroA(IntroBase):
	def __init__(self):
		IntroBase.__init__(self)
		white = (255, 255, 255)
		green = (0, 255, 0)
		yellow = (255, 255, 0)
		
		self.lineA = self.ConcatenateImages([
											self.MakeText(white, "This is the story of a "),
											self.MakeText(green, "future"),
											self.MakeText(white, '.')
											])
		self.lineB = self.ConcatenateImages([
											self.MakeText(white, "Not the only "),
											self.MakeText(green, 'future')
											])
		self.lineC = self.MakeText(white, "but one")
		self.lineD = self.ConcatenateImages([
											self.MakeText(white, 'of '),
											self.MakeText(yellow, 'many'),
											self.MakeText(white, '...')
											])
		
		self.bg = Resources.ImageLibrary.Get('Intro/intro_0.png')
		self.fgA = Resources.ImageLibrary.Get('Intro/intro_0a.png')
		self.fgB = Resources.ImageLibrary.Get('Intro/intro_0b.png')
		self.temp = pygame.Surface((640, 480))
		
		self.nar_lineA = '`Good morning, Citizens.'
		self.nar_lineB = 'Today is Ineo 1:1, Utopia Year 27.'
		self.nar_lineC = "Today's weather is sunny.\"" 
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
		counter = self.counter
		
		bcounter = counter - 90
		ccounter = bcounter - 60
		dcounter = ccounter - 60
		
		finalFadeBegin = dcounter - 90
		
		ecounter = finalFadeBegin - 60
		
		if finalFadeBegin >= 0:
			dimValue = finalFadeBegin * 10
		else:
			dimValue = 0
		
		if dimValue > 300:
			pass #self.next = IntroB()
		
		# Line A "This is the story of a future"
		av = counter * 10
		if av > 255: av = 255
		ax = 100
		ay = 100
		self.BlitText(self.lineA, (ax, ay), av - dimValue)
		
		# Line B "Not the only future"
		if bcounter >= 0: 
			bv = bcounter * 10
			if bv > 255: bv = 255
			bx = 250
			by = 130
			self.BlitText(self.lineB, (bx, by), bv - dimValue) 
		
		# Line C "but one"
		if ccounter >= 0:
			cv = ccounter * 10
			if cv > 255: cv = 255
			cx = 407
			cy = 150
			self.BlitText(self.lineC, (cx, cy), cv - dimValue)
		
		# Line D "of many..."
		if dcounter >= 0:
			dv = dcounter * 10
			if dv > 255: dv = 255
			dx = 467
			dy = 170
			self.BlitText(self.lineD, (dx, dy), dv - dimValue)
			self.temp.blit(self.bg, (0, 0))
			self.temp.blit(self.fgA, (220 - dcounter // 4, 0))
			self.temp.blit(self.fgB, (280 - dcounter // 2, 0))
			self.temp.set_alpha(dv)
			screen.blit(self.temp, (0, 0))
		
		if ecounter >= 0:
			text = '\n'.join([self.nar_lineA, self.nar_lineB, self.nar_lineC])
			limit = ecounter
			if limit > len(text): limit = len(text)
			display = text[:limit].split('\n')
			y = 400 - ecounter // 2
			x = 200
			for d in display:
				self.BlitText(self.MakeText((160, 225, 255), d), (x, y), 255)
				x += 100
				y += 40
		
		fcounter = ecounter - 150
		gcounter = fcounter - 60
		
		if fcounter > 0 and gcounter < 0:
			self.temp.blit(screen, (0, 0))
			v = 255 - fcounter * 10
			if v < 0:
				v = 0
			self.temp.set_alpha(v)
			screen.fill((0, 0, 0))
			screen.blit(self.temp, (0, 0))
		
		if gcounter >= 0:
			screen.fill((0, 0, 0))
		
		self.DoBlits(screen)
		
		if gcounter >= 0:
			self.temp.fill((0, 0, 0))
			self.temp.blit(screen, (0, 0))
			v = 255 - gcounter * 10
			if v < 0:
				v = 0
				self.next = IntroB()
			self.temp.set_alpha(v)
			screen.fill((0, 0, 0))
			screen.blit(self.temp, (0, 0))
			
		
class IntroB(IntroBase):
	def __init__(self):
		IntroBase.__init__(self)
		white = (255, 255, 255)
		self.bg = Resources.ImageLibrary.Get('Intro/intro_1.png').convert()
		self.temp = pygame.Surface((640, 480))
		
		self.lineA = self.MakeText(white, "In all honesty it's not a bad place to be.")
		self.lineB = self.ConcatenateImages([
											self.MakeText((100, 200, 130), 'Food'),
											self.MakeText(white, ' is plentiful.')
											])
		self.lineC = self.ConcatenateImages([
											self.MakeText((200, 100, 100), 'Crime'),
											self.MakeText(white, ' is rare.')
											])
		self.lineD = self.MakeText(white, "You can't beat that when the rest of the")
		self.lineE = self.MakeText(white, "world has only craters and despair to offer.")
		
		self.nar = '`Citizens,\nPlease extend Your thanks\nto each other for working hard\nfor Our happiness every day.\"'
		
	def GetBG(self, counter):
		scale = counter / 2000.0 + 1.0
		return pygame.transform.smoothscale(self.bg, (int(640 * scale), int(480 * scale)))
		
	def Render(self, screen):
		screen.fill((0, 0, 0))
		counter = self.counter
		
		bgOpacity = counter * 5
		#self.bg.set_alpha(bgOpacity)
		bg = self.GetBG(counter)
		bg.set_alpha(bgOpacity)
		screen.blit(bg, (0, 480 - bg.get_height()))
		
		acounter = counter - 255 // 5
		bcounter = acounter - 60
		ccounter = bcounter - 40
		dcounter = ccounter - 77
		ecounter = dcounter - 30
		fcounter = ecounter - 120
		gcounter = fcounter - 30
		hcounter = gcounter - 150
		
		if dcounter >= 0:
			dimValue = dcounter * 8
		else:
			dimValue = 0
		
		if fcounter >= 0:
			dimVal2 = fcounter * 10
		else:
			dimVal2 = 0
		
		
		if acounter >= 0:
			av = acounter * 10
			if av > 255: av = 255
			ax = 131
			ay = 159
			self.BlitText(self.lineA, (ax, ay), av - dimValue)
		
		if bcounter >= 0:
			bv = bcounter * 10
			if bv > 255: bv = 255
			bx = 380
			by = 90
			self.BlitText(self.lineB, (bx, by), bv - dimValue)
		
		if ccounter >= 0:
			cv = ccounter * 10
			if cv > 255: cv = 255
			cx = 130
			cy = 280
			self.BlitText(self.lineC, (cx, cy), cv - dimValue)
			
		if ecounter >= 0:
			ev = ecounter * 10
			if ev > 255: ev = 255
			ex = 180
			ey = 310
			self.BlitText(self.lineD, (ex, ey), ev - dimVal2)
			self.BlitText(self.lineE, (ex, ey + 20), ev - dimVal2)
		
		if gcounter >= 0:
			text = self.nar
			limit = gcounter
			if limit > len(text): limit = len(text)
			display = text[:limit].split('\n')
			y = 300 - gcounter // 2
			x = 50
			for d in display:
				self.BlitText(self.MakeText((160, 225, 255), d), (x, y), 255)
				x += 100
				y += 40
		
		self.DoBlits(screen)
		
		if hcounter >= 0:
			v = hcounter * 5
			if v > 255:
				v = 255
				self.next = IntroC()
			self.temp.fill((0, 0, 0))
			self.temp.blit(screen, (0, 0))
			self.temp.set_alpha(255 - v)
			screen.fill((0, 0, 0))
			screen.blit(self.temp, (0, 0))



class IntroC(IntroBase):
	def __init__(self):
		IntroBase.__init__(self)
		white = (255, 255, 255)
		gray = (160, 170, 190)
		red = (255, 0, 0)
		self.neverbefore = self.MakeText(gray, 'never      before')
		self.lineA = self.MakeText(white, 'But to get something we       had')
		self.lineB = self.MakeText(white, 'We have to do something we have       done')
		self.lineC = self.MakeText(white, "No one enters utopia without proper ")
		self.sacrifice = self.MakeText(red, "sacrifice.")
		
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
		counter = self.counter
		
		x = 100
		y = 300
		
		acounter = counter - 0
		bcounter = acounter - 96
		ccounter = bcounter - 96
		dcounter = ccounter - 30
		ecounter = dcounter - 58
		fcounter = ecounter - 90
		
		dimVal = 0
		if bcounter >= 0:
			dimVal = bcounter * 10
			
		dimVal2 = 0
		if ccounter >= 0:
			dimVal2 = ccounter * 10
		
		dimVal3 = 0
		if fcounter >= 0:
			dimVal3 = fcounter * 10
			if dimVal3 > 300:
				self.next = IntroD()
		
		if acounter >= 0:
			av = acounter * 10
			if av > 255: av = 255
			self.BlitText(self.neverbefore, (x + 300, y - 18 + counter // 3), av - dimVal2)
			self.BlitText(self.lineA, (x + 111, y), av - dimVal)
		
		if bcounter >= 0:
			bv = bcounter * 10
			if bv > 255: bv = 255
			self.BlitText(self.lineB, (x + 111 - 65, y + 40), bv - dimVal2)
		
		if dcounter >= 0:
			dv = dcounter * 10
			if dv > 255: dv = 255
			dx = 100 + dcounter // 4
			dy = 200
			self.BlitText(self.lineC, (dx, dy), dv - dimVal3)
			
			if ecounter >= 0:
				ev = ecounter * 10
				if ev > 255: ev = 255
				ex = dx + self.lineC.get_width()
				self.BlitText(self.sacrifice, (ex, dy), ev - dimVal3)
				
		
		self.DoBlits(screen)
		

class IntroD(IntroBase):
	def __init__(self):
		IntroBase.__init__(self)
		white = (255, 255, 255)
		self.lineA = self.MakeText(white, 'As resources became less scarce people')
		self.lineB = self.MakeText(white, "stopped striving to stand out above their peers.")
		self.lineC = self.MakeText(white, 'As differences were eliminated to calm an angry')
		self.lineD = self.MakeText(white, 'populace, creativity seemed to go with them.')
		
	def Render(self, screen):
		screen.fill((0, 0, 0))
		
		counter = self.counter
		
		acounter = counter 
		bcounter = acounter - 190
		ccounter = bcounter - 200
		
		
		dimValue = bcounter - 190
		if dimValue < 0: dimValue = 0
		dimValue = dimValue * 7
		if dimValue > 255:
			dimValue = 255
		
		if acounter >= 0:
			av = acounter * 10
			if av > 255: av = 255
			ax = 60 + acounter//3
			ay = 300
			self.BlitText(self.lineA, (ax, ay), av - dimValue)
			self.BlitText(self.lineB, (ax, ay + 20), av - dimValue)
			
		if bcounter >= 0:
			bv = bcounter * 10
			if bv > 255: bv = 255
			bx = 60 + bcounter//3
			by = 400
			self.BlitText(self.lineC, (bx, by), bv - dimValue)
			self.BlitText(self.lineD, (bx, by + 20), bv - dimValue)
		
		if dimValue == 255:
			#print 'CHANGE!'
			self.next = IntroE()
			
		self.DoBlits(screen)

class IntroE(IntroBase):
	def __init__(self):
		IntroBase.__init__(self)
		self.nar = '\n'.join(["`We would like to take a moment",
					"to remind all Citizens that",
					"Items of Objection are to be",
					"left alone and reported immediately",
					"for the safety of All.\""])
		self.bg = Resources.ImageLibrary.Get('Intro/intro_2.png').convert_alpha()
		self.temp = pygame.Surface((640, 480))
		
	def Render(self, screen):
		screen.fill((0, 0, 0))
		self.temp.fill((0, 0, 0))
		counter = self.counter
		acounter = counter - 30
		bcounter = acounter - 300
		
		dim2 = bcounter * 10
		if dim2 > 255: dim2 = 255
		if dim2 < 0: dim2 = 0
		
		bga = counter * 10
		if bga > 255: bga = 255
		
		bga = bga - dim2
		if bga < 0: bga = 0
		f = bga - dim2
		if f < 0: f = 0
		if f > 255: f = 255
		print f
		self.temp.blit(self.bg, (0, 0))
		self.temp.set_alpha(f)
		screen.blit(self.temp, (0, 0))
		#self.bg.set_alpha(f)
		#pygame.draw.rect(screen, pygame.Color(0, 0, 0, 255 - f), pygame.Rect(0, 0, 640, 480))
		
		if bcounter > 0 and bga == 0:
			self.next = IntroF()
		
		
		if acounter >= 0:
			text = self.nar
			limit = acounter
			if limit > len(text): limit = len(text)
			display = text[:limit].split('\n')
			y = 300 - acounter // 2
			x = 50
			for d in display:
				self.BlitText(self.MakeText((160, 225, 255), d), (x, y), 255)
				x += 100
				y += 40
		
		self.DoBlits(screen)


class IntroF(IntroBase):
	def __init__(self):
		IntroBase.__init__(self)
		self.lineA = self.MakeText((255, 255, 255), '`On the sacrificial altar of unity and utopia we')
		self.lineB = self.ConcatenateImages([
							self.MakeText((255, 255, 255), 'placed '),
							self.MakeText((255, 0, 0), 'music'),
							self.MakeText((255, 255, 255), ', '),
							self.MakeText((255, 180, 0), 'theatre'),
							self.MakeText((255, 255, 255), ', '),
							self.MakeText((0, 100, 255), 'dance'),
							self.MakeText((255, 255, 255), ', '),
							self.MakeText((100, 200, 100), 'literature'),
							self.MakeText((255, 255, 255), '. ')])
		self.lineC = self.MakeText((140, 140, 140), '--Anonymous Author, Before Utopia Year 3')
		self.bg = pygame.Surface((640, 480))
		self.bg_open = pygame.Surface((640, 480))
		self.bg_open.blit(Resources.ImageLibrary.Get('Intro/intro_3.png'), (0, 0))
		self.bg_closed = pygame.Surface((640, 480))
		self.bg_closed.blit(Resources.ImageLibrary.Get('Intro/intro_4.png'), (0, 0))
		self.nar = '\n'.join([
							"`Thank you for keeping Our", 
							"society harmonious for",
							"a bright future. " + (' '*120),
							"Please enjoy Your day.\""
							])
		self.RenderBG(0)
	
	def RenderBG(self, opacity):
		self.bg.blit(self.bg_open, (0, 0))
		self.bg_closed.set_alpha(opacity)
		if opacity > 0:
			self.bg.blit(self.bg_closed, (0, 0))
		
	def Render(self, screen):
		counter = self.counter
		
		screen.fill((0, 0, 0))
		
		acounter = counter
		bcounter = acounter - 50
		ccounter = bcounter - 300
		dcounter = ccounter - 255 // 6 + 20
		ecounter = dcounter - 4 * 30 - 7 * 30
		
		dimVal = 0
		if ccounter >= 0:
			dimVal = ccounter * 10
			if dimVal > 255:
				dimVal = 255
			if dimVal < 0: dimVal = 0
		
		if acounter >= 0:
			av = acounter * 7
			if av > 255: av = 255
			self.bg.set_alpha(av)
		
		if bcounter >= 0:
			av = bcounter * 10
			ax = 100
			ay = 300 - bcounter // 3
			if av > 255: av = 255
			self.BlitText(self.lineA, (ax, ay), av - dimVal)
			self.BlitText(self.lineB, (ax, ay + 20), av - dimVal)
			self.BlitText(self.lineC, (ax + 100, ay + 40), av - dimVal)
		
		if ccounter >= 0:
			cv = ccounter * 6
			if cv > 255: cv = 255
			self.RenderBG(cv)
		
		screen.blit(self.bg, (0, 0))
		
		dim2 = 0
		if ecounter >= 0:
			#self.bg.blit(screen, (0, 0))
			opacity = 255 - ecounter * 4
			if opacity < 0: opacity = 0
			self.bg.set_alpha(opacity)
			screen.fill((0, 0, 0))
			screen.blit(self.bg, (0, 0))
			dim2 = ecounter * 8
			if dim2 > 255: dim2 = 255
			if ecounter >= 110:
				self.next = Menus.Title()
		
		if dcounter >= 0:
		
			text = self.nar
			limit = dcounter
			if limit > len(text): limit = len(text)
			display = text[:limit].split('\n')
			y = 300 - dcounter // 2
			x = 50
			for d in display:
				print 255 - dim2, ecounter
				self.BlitText(self.MakeText((160, 225, 255), d), (x, y), 255 - dim2)
				x += 100
				y += 40
		
		self.DoBlits(screen)