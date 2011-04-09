import os
import pygame
import GamePlay

def GetSpecializer(levelName):
	if levelName == 'level1': return Level1Specializer()
	if levelName == 'level2': return Level2Specializer()
	if levelName == 'level3': return Level3Specializer()
	if levelName == 'level4': return Level4Specializer()
	if levelName == 'level5': return Level5Specializer()
	if levelName == 'level6': return Level6Specializer()
	if levelName == 'level7': return Level7Specializer()
	if levelName == 'level8': return Level8Specializer()
	if levelName == 'level9': return Level9Specializer()
	return SpecializerBase()

class SpecializerBase:
	
	def __init__(self):
		self.narrator_color = (80, 140, 210)
		self.nar_color = self.narrator_color
	
	def ShouldShowMessage(self, counter, conversionProgress):
		return None
	
	def MoveToNextLevel(self, counter, conversionProgress):
		return conversionProgress >= 80
	
	def DoSomethingInteresting(self, coutner, auxCounter, conversionProgress, playScene, level):
		pass
	
	def DoSetup(self, playScene, level):
		pass
	
	def Shortcircuited(self, levelName):
		return levelName in ['level6', 'level7', 'level8']
		return False
	
	def SetMinColor(self, level, left, top, right, bottom, value):
		
		x = left
		while x <= right:
			y = top
			while y <= bottom:
				level.tiles[x][y].SetMinColorIntensity(value)
				y += 1
			x += 1
	
class Level1Specializer(SpecializerBase):
	def __init__(self):
		SpecializerBase.__init__(self)
		self.lapis = None
		
		self.lapis_color = (243, 98, 210)
		self.maple_color = (255, 107, 0)
		self.magic_counter = 852
		self.foo = True #OMG HAX
	
	def DoSetup(self, playScene, level):
		level.citizens[0].color = 0
		a = level.citizens[0]
		b = level.citizens[1]
		self.level = level
		a.tgV = a.gV
		b.tgV = b.gV
		
		a.gV = a.cV
		b.gV = b.cV
	
	def ShouldShowMessage(self, counter, conversionProgress):
		if counter == 1:
			return [self.maple_color,
				"*sniffle* She's been gone for a while but I",
				"still miss Gran, you know Lapis?"]
		elif counter == 2:
			return [self.lapis_color,
				"Yea, cleaning out her house isn't helping, ",
				"brings back memories of playing here as kids."]
		elif counter == 40:
			return [self.maple_color,
				"Why don't you go make us some lunch, I'll be ",
				"in there in a moment."]
		elif counter == 130:
			return [self.maple_color,
				"Huh, I wonder what this is..."]
		elif counter == 220 + 255:
			return [self.narrator_color,
				"(Once a person has been `cultured\" you may",
				"select them by clicking on them and move ",
				"them around by right-clicking destinations)"]
		
		elif counter == 780:
			return [self.narrator_color,
				"(A cultured citizen emits a contagious aura.)"]
		
		elif counter == 830:
			return [self.lapis_color,
				"Maple! Lunch is ready..."]
		
		elif counter == 840:
			return [self.lapis_color,
				"Wha...What is that?!?"]
		
		elif counter == 850:
			return [self.narrator_color,
				"(To spread culture, simply stand next to an",
				"uninitiated citizen)"]
		
		elif self.foo and counter > 851 and conversionProgress == 100:
			self.magic_counter = counter
			self.foo = False
			return [self.lapis_color,
				"It's...beautiful..."]
		
		elif counter == self.magic_counter + 1 and conversionProgress == 100:
			return [self.maple_color,
				"I think it's that stuff Gran used to ",
				"talk about...`music\"?"]
		
		elif counter == self.magic_counter + 60 and conversionProgress == 100:
			return [self.narrator_color,
				"(To select multiple people, click and drag",
				"a box around them)"]
		
		elif counter == self.magic_counter + 250 and conversionProgress == 100:
			a = self.level.citizens[0]
			b = self.level.citizens[1]
			a.gV = a.tgV
			b.gV = b.tgV
			return [self.lapis_color,
				"We should really let others know about this..."]
			
	def MoveToNextLevel(self, counter, conversionProgress):
		return counter == self.magic_counter + 255 and conversionProgress == 100
	
	
	def DoSomethingInteresting(self, counter, auxCounter, conversionProgress, playScene, level):
		
		maple = level.citizens[0]
		if counter == 41:
			self.lapis = level.citizens[1]
			
			maple.targetX = 15 * 32
			maple.targetY = 10 * 32
			self.lapis.targetX = 9 * 32
			self.lapis.targetY = 3 * 32
		
		elif counter == 120: # when lapis reaches the door
			level.citizens = level.citizens[:1]
			level.sprites = level.sprites[:1]
			
		elif counter == 145:
			level.tiles[15][9] = GamePlay.MakeTile('int/phonograph', 15, 9)
			level.tiles[15][9].SetMinColorIntensity(255)
		
		elif counter == 175:
			pygame.mixer.music.load(os.path.join('Media', 'Music', '98time.mp3'))
			pygame.mixer.music.set_volume(0.5)
			pygame.mixer.music.play(-1)
			
		elif counter >= 220 and counter <= 220 + 255:
			v = counter - 220
			maple.color = v
			
			
		elif counter >= 220 + 255 and counter <= 220 + 255 + 255: # 730
			
			v = (counter - 220 - 255) // 2
			y = 2
			while y <= 11:
				x = 3
				while x <= 16:
					level.tiles[x][y].SetMinColorIntensity(v)
					x += 1 
				y += 1
	
		elif counter == 829:
			self.lapis.direction = 'down'
			level.citizens.append(self.lapis)
			level.sprites.append(self.lapis)
		
class Level2Specializer(SpecializerBase):
	def __init__(self):
		SpecializerBase.__init__(self)
	
	def DoSetup(self, playScene, level):
		level.citizens[0].Colorize()
		level.citizens[1].Colorize()
		
		self.SetMinColor(level, 10, 10, 18, 19, 128)
		self.SetMinColor(level, 11, 11, 17, 18, 255)
	
	def ShouldShowMessage(self, counter, conversionProgress):
		if counter == 2:
			return [self.nar_color,
				"Once you culture at least 80% of the", 
				"population in the current area, the bounds",
				"of the level will expand, increasing the",
				"area by a factor of Nine Times."]
	
class Level3Specializer(SpecializerBase):
	def __init__(self):
		SpecializerBase.__init__(self)
	
	def ShouldShowMessage(self, counter, conversionProgress):
		
		if counter == 2:
			return [self.nar_color,
				"Watch out for police.",
				"They probably won't approve of you",
				"disrupting the peace."]
	
	def DoSetup(self, playScene, level):
		level.citizens[0].Decolorize()
	
class Level4Specializer(SpecializerBase):
	def __init__(self):
		SpecializerBase.__init__(self)
		
	def DoSetup(self, playScene, level):
		level.citizens[0].Decolorize()
class Level5Specializer(SpecializerBase):
	def __init__(self):
		SpecializerBase.__init__(self)
		
	def DoSetup(self, playScene, level):
		level.citizens[0].Decolorize()
class Level6Specializer(SpecializerBase):
	def __init__(self):
		SpecializerBase.__init__(self)
		
	def DoSetup(self, playScene, level):
		level.citizens[0].Colorize()
		
class Level7Specializer(SpecializerBase):
	def __init__(self):
		SpecializerBase.__init__(self)
		
	def DoSetup(self, playScene, level):
		level.citizens[0].Decolorize()
		
class Level8Specializer(SpecializerBase):
	def __init__(self):
		SpecializerBase.__init__(self)
	
	def DoSetup(self, playScene, level):
		level.citizens[0].Decolorize()
		
class Level9Specializer(SpecializerBase):
	def __init__(self):
		SpecializerBase.__init__(self)
	
	def DoSetup(self, playScene, level):
		level.citizens[0].Decolorize()