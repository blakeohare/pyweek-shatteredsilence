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
		pass
	
	def ShouldShowMessage(self, counter, conversionProgress):
		return None
	
	def MoveToNextLevel(self, counter, conversionProgress):
		return conversionProgress >= 80
	
	def DoSomethingInteresting(self, coutner, auxCounter, conversionProgress, playScene, level):
		pass
	
	def DoSetup(self, playScene, level):
		pass
	
class Level1Specializer(SpecializerBase):
	def __init__(self):
		pass
	
	def DoSetup(self, playScene, level):
		level.citizens[0].color = 0
	
	def ShouldShowMessage(self, counter, conversionProgress):
		if counter == 1:
			return [(255, 107, 0),
				"*sniffle* She's been gone for a while but I",
				"still miss Gran, you know Lapis?"]
		elif counter == 2:
			return [(243, 98, 210),
				"Yea, cleaning out her house isn't helping, ",
				"brings back memories of playing here as kids."]
		elif counter == 40:
			return [(255, 107, 0),
				"Why don't you go make us some lunch, I'll be ",
				"in there in a moment."]
		elif counter == 130:
			return [(255, 107, 0),
				"Huh, I wonder what this is..."]
	
	def MoveToNextLevel(self, counter, conversionProgress):
		return False
	
	
	def DoSomethingInteresting(self, counter, auxCounter, conversionProgress, playScene, level):
		
		maple = level.citizens[0]
		if counter == 41:
			lapis = level.citizens[1]
			
			maple.targetX = 15 * 32
			maple.targetY = 10 * 32
			lapis.targetX = 9 * 32
			lapis.targetY = 3 * 32
		
		elif counter == 120: # when lapis reaches the door
			level.citizens = level.citizens[:1]
			level.sprites = level.sprites[:1]
			
		elif counter == 145:
			level.tiles[15][9] = GamePlay.MakeTile('int/phonograph', 15, 9)
		
		elif counter == 175:
			pygame.mixer.music.load(os.path.join('Media', 'Music', '98time.mp3'))
			pygame.mixer.music.set_volume(0.5)
			pygame.mixer.music.play(-1)
			
		elif counter >= 220 or counter <= 220 + 255:
			v = counter - 220
			y = 2
			while y <= 11:
				x = 3
				while x <= 16:
					level.tiles[x][y].SetMinColorIntensity(v)
					x += 1 
				y += 1
	
		
class Level2Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level3Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level4Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level5Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level6Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level7Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level8Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level9Specializer(SpecializerBase):
	def __init__(self):
		pass
	