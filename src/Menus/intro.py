import pygame
from Game import GameSceneBase
import Resources
import Menus



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
		pass # You have to sit and watch the whoooooole thing
	
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
		
		self.nar_lineA = '`Good morning, citizens.'
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
	
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
		counter = self.counter
		