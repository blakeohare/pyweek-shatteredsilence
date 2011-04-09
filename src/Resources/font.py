import pygame
import Resources

_letter_image = None
_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcd0123456789.,\'!?`"-/%&()[]*:;~>'
_foreground = None
_outline = None
_width_by_letter = {}
_initialized = False

def _initialize():
	global _outline, _width_by_letter, _letter_image, _foreground
	_letter_image = Resources.ImageLibrary.Get('letters.png')
	_foreground = pygame.mask.from_threshold(_letter_image, (255, 0, 0, 255), (10, 10, 10, 255))
	_outline = pygame.mask.from_threshold(_letter_image, (0, 0, 0, 255), (10, 10, 10, 255))
	i = 0
	while i < len(_chars):
		left = (i % 10) * 17 + 1
		top = (i // 10) * 17 + 1
		char = _chars[i]
		
		max_right = 0
		x = 0
		while x < 16:
			y = 0
			while y < 16:
				
				if _outline.get_at((x + left, y + top)) != 0:
					max_right = x

				y += 1
			x += 1
		
		_width_by_letter[char] = max_right + 1
		i += 1


_fonts = {}

def GetFont(r, g, b):
	global _fonts
	key = str(r) + '_' + str(g) + '_' + str(b)
	font = _fonts.get(key)
	if font == None:
		font = FontPrivate((r, g, b))
		_fonts[key] = font
	return font


class FontPrivate:
	def __init__(self, color):
		global _initialized
		if not _initialized:
			_initialize()
		self.letters = {}
		self.cache = {}
		self.createImages(color)
		
	def createImages(self, color):
		global _width_by_letter, _foreground, _outline, _chars
		i = 0
		onepixel = pygame.Surface((1, 1))
		black = pygame.Surface((1, 1))
		pygame.draw.rect(onepixel, color, pygame.Rect(0, 0, 2, 2))
		pygame.draw.rect(black, (0, 0, 0), pygame.Rect(0, 0, 1, 1))
		while i < len(_chars):
			char = _chars[i]
			letter = pygame.Surface((_width_by_letter[char], 16)).convert_alpha()
			letter.fill((0, 0, 0, 0))
			width = letter.get_width()
			left = (i % 10) * 17 + 1
			top = (i // 10) * 17 + 1
			x = 0
			while x < width:
				y = 0
				while y < 16:
					if _foreground.get_at((x + left, y + top)) != 0:
						letter.blit(onepixel, (x, y))
					elif _outline.get_at((x + left, y + top)) != 0:
						letter.blit(black, (x, y))
					y += 1
				x += 1
			self.letters[char] = letter
			i += 1
	
	def Render(self, text, kerning=0):
		
		if text == '': text = ' '
		text = text.upper()
		
		output = self.cache.get(text)
		if output != None:
			return output
		
		
		images = []
		for char in text:
			if char == ' ':
				images.append(None)
			else:
				letter = self.letters.get(char)
				if letter == None:
					letter = self.letters['?']
				images.append(letter)
		
		total = 0
		
		for image in images:
			if image == None:
				total += 8 + kerning
			else:
				total += image.get_width() + kerning
		
		output = pygame.Surface((total, 16)).convert_alpha()
		output.fill((0, 0, 0, 0))
		x = 0
		for image in images:
			if image == None:
				x += 8 + kerning
			else:
				output.blit(image, (x, 0))
				x += image.get_width() + kerning
		self.cache[text] = output
		
		return output