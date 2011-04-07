import pygame
import Resources

_border_cache = {}

class Border:
	def __init__(self):
		self.TL = 0
		self.TC = 1
		self.TR = 2
		self.ML = 3
		self.MC = 4
		self.MR = 5
		self.BL = 6
		self.BC = 7
		self.BR = 8
		self.Load()
	
	def Load(self):
		global _border_cache
		_borders = Resources.ImageLibrary.Get('borders.png')
		
		i = 0
		while i < 9:
			left = (i % 3) * 17 + 1
			top = (i // 3) * 17 + 1
			
			_border_cache[i] = pygame.Surface((16, 16))
			key = pygame.Color(0, 0, 255)
			_border_cache[i].fill(key)
			_border_cache[i].set_colorkey(key)
			_border_cache[i].blit(_borders, (0, 0), pygame.Rect(left, top, 16, 16))
			
			i += 1
	 
	def GetTile(self, tile):
		global _border_cache
		if (tile < 0) or (tile > 8):
			return None
		
		return _border_cache[tile]
	
	def MakeSurf(self, width, height):
		if (width < 2) or (height < 2):
			raise "Invalid size."
		
		surf = pygame.Surface((width * 16, height * 16))
		key = pygame.Color(0, 0, 255)
		surf.fill(key)
		surf.set_colorkey(key)
		
		_gt = self.GetTile
		x = 0
		while x < width:
			y = 0
			while y < height:
				tile = None
				
				if (x == 0):
					if (y == 0):
						tile = _gt(self.TL)
					elif (y == (height - 1)):
						tile = _gt(self.BL)
					else:
						tile = _gt(self.ML)
				elif (x == (width - 1)):
					if (y == 0):
						tile = _gt(self.TR)
					elif (y == (height - 1)):
						tile = _gt(self.BR)
					else:
						tile = _gt(self.MR)
				else:
					if (y == 0):
						tile = _gt(self.TC)
					elif (y == (height - 1)):
						tile = _gt(self.BC)
					else:
						tile = _gt(self.MC)
				if not tile:
					raise "No tile found for (%d,%d)" % (x, y)
				
				surf.blit(tile, (x * 16, y * 16))
				y += 1
			x += 1
		
		return surf