import time
import pygame
import os
#import random

_conversion_mode = True

class ImageLibrary:
	
	def __init__(self):
		self.intervals = 25
		self.images = []
		self.virtualizedImages = {}
		self.folderCheck = {}
		self.fullyInitialized = False
		self.total = 0
		self.loadPos = 0
		self.cacheImages = []
		for i in range(self.intervals):
			self.images.append({})
	
	def SaveCache(self):
		if not os.path.exists('cache'):
			os.mkdir('cache')
			
			paths = self.AllPaths()
			manifest = '\n'.join(paths)
			
			for i in range(self.intervals):
				cacheImage = self.GenCacheForInterval(paths, i)
				pygame.image.save(cacheImage, 'cache' + os.sep + str(i) + '.png')
			
			c = open('cache' + os.sep + 'manifest.txt', 'wt')
			c.write(manifest)
			c.close()
			
	def GenCacheForInterval(self, paths, interval):
		
			width = int(len(paths) ** .5)
			height = len(paths) // width + 1
			
			bg = pygame.Surface((width * 32, height * 32), pygame.SRCALPHA).convert_alpha()
			
			pathsCopy = paths[:]
			dict = self.images[interval]
			y = 0
			while y < height:
				x = 0
				while x < width:
					if len(pathsCopy) > 0:
						path = pathsCopy[0]
						pathsCopy = pathsCopy[1:]
						img = dict.get(path)
						if img != None:
							bg.blit(img, (x * 32, y * 32))
					else:
						return bg
					x += 1
				y += 1
	def AllPaths(self):
		dict = self.images[0]
		keys = dict.keys()
		unique = {}
		for key in keys:
			img = dict[key]
			if img.get_width() == 32 and img.get_height() == 32:
				unique[key] = True
		output = unique.keys()[:]
		return output
	
	
	def CacheExists(self):
		return os.path.exists('cache' + os.sep + 'manifest.txt')
	
	def trim(self, string):
		while len(string) > 0 and string[0] in ' \r\t\n':
			string = string[1:]
		while len(string) > 0 and string[-1] in ' \r\t\n':
			string = string[:-1]
		return string
	
	def PrepForLoadCache(self):
		c = open('cache' + os.sep + 'manifest.txt', 'rt')
		t = c.read().split('\n')
		c.close()
		
		self.imagesToLoadFromCache = []
		
		for line in t:
			key = self.trim(line)
			if len(key) > 0:
				self.imagesToLoadFromCache.append(key)
		self.total = len(self.imagesToLoadFromCache)
		
		for i in range(self.intervals):
			self.cacheImages.append(pygame.image.load('cache' + os.sep + str(i) + '.png'))
	
	def CacheLoadProgress(self):
		if self.total == 0: return 100
		return 100 - 100 * len(self.imagesToLoadFromCache) // self.total
		
	def LoadNextCache(self):
		if len(self.imagesToLoadFromCache) == 0:
			return False
		
		imageToLoad = self.imagesToLoadFromCache[0]
		self.imagesToLoadFromCache = self.imagesToLoadFromCache[1:]
		
		width = self.cacheImages[0].get_width() // 32
		x = self.loadPos % width
		y = self.loadPos // width
		
		i = 0
		while i < self.intervals:
			img = pygame.Surface((32, 32), pygame.SRCALPHA).convert_alpha()
			img.blit(self.cacheImages[i], (-x * 32, -y * 32))
			self.images[i][imageToLoad] = img
			i += 1
		
		self.loadPos += 1
				
		return True
	
	
	# opacity is 0-255
	def Get(self, path, opacity=None):
		if opacity == None:
			field = self.intervals - 1
		else:
			perInterval = 255.0 / self.intervals
			
			field = int(opacity / perInterval)
		
		if field > self.intervals - 1: field = self.intervals - 1
		if field < 0: field = 0
		images = self.images[field]
		image = images.get(path)
		if image == None:
			newpath = path.replace('\\', '/')
			image = images.get(newpath)
			if image != None:
				self.MirrorImage(path, newpath)
				return images.get(newpath)
			
			finalpath = ('Images/' + newpath).replace('/', os.sep).replace(os.sep + os.sep, os.sep)
			
			if os.path.exists(finalpath):
				image = pygame.image.load(finalpath).convert_alpha()
			else:
				image = self.GetVirtualizedImageFile(finalpath).convert_alpha()
			image = self.InitializeImages(path, image, opacity == None)
			return self.Get(path, opacity)
			
		return image
	
	def GetVirtualizedImageFile(self, path):
		return self.virtualizedImages[path]
	
	def AddVirtualizedImage(self, path, image):
		self.virtualizedImages[path] = image.copy()
	
	def MirrorImage(self, targetPath, sourcePath):
		for i in range(self.intervals):
			self.images[i][targetPath] = self.images[i][sourcePath]
	
	def InitializeImages(self, path, colorImage, disableGrayscale):
		if disableGrayscale:
			#for i in range(0, self.intervals):
			#	self.images[i][path] = colorImage
			self.images[self.intervals - 1][path] = colorImage
			return
		
		width = colorImage.get_width()
		height = colorImage.get_height()
		grayImage = self.ConvertToGrayscale(colorImage, path)
		self.images[0][path] = grayImage
		self.images[self.intervals - 1][path] = colorImage
		onePixel = pygame.Surface((1, 1)).convert()
		mask = pygame.mask.from_surface(colorImage)
		for i in range(1, self.intervals - 1):
			copy = grayImage.copy()
			copy.blit(grayImage, (0, 0))
			onePixel.set_alpha(i * 255 // self.intervals)
			y = 0
			while y < height:
				x = 0
				while x < width:
					if mask.get_at((x, y)) != 0:
						onePixel.blit(colorImage, (-x, -y))
						copy.blit(onePixel, (x, y))
					x += 1
				y += 1

			self.images[i][path] = copy
			
	
	def ConvertToGrayscale(self, image, path):
		grayfile = 'GrayImages' + os.sep + path.replace('/', os.sep).replace('\\', os.sep)
		if os.path.exists(grayfile):
			return pygame.image.load(grayfile).convert_alpha()
		return self.GetVirtualizedImageFile(grayfile)
