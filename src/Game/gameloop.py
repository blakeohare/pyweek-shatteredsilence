import pygame
from pygame.locals import *
import time
import os
import Resources

class GameLoop:
	
	def __init__(self, title, width, height, framesPerSecond):
		self.width = width
		self.height = height
		self.fps = framesPerSecond
		pygame.init()
		self.screen = pygame.display.set_mode((640, 480))
		pygame.display.set_caption(title)
		self.DoHacks(self.screen)
		self.quitting = False
		self.show_fps_counter = False
		self.lastNFrames = []
		self.font = None
		self.sound_cache = {}
	
	def Start(self, startingScene):
		self.current = startingScene
		
		self.DoLoop()
	
	
	def DoLoop(self):
		vfps = 0.0
		afps = 0.0
		
		while not self.quitting:
			start = time.time()
			
			self.ProcessInput()
			
			self.Update()
			
			self.Render(vfps, afps)
			
			self.current = self.current.next
			
			if self.current == None:
				self.quitting = True
			
			self.PlaySounds()
			
			end = time.time()
			
			diff = end - start
			
			targetSPF = 1.0 / self.fps
			if diff < targetSPF:
				delay = targetSPF - diff
				time.sleep(delay)
			
			if self.show_fps_counter and diff > 0:
				vfps = 1.0 / diff
				afps = 1.0 / (time.time() - start)
		
		if Resources.ImageLibrary.fullyInitialized:
			Resources.ImageLibrary.SaveCache()			
	
	def ProcessInput(self):
		
		if self.current != None:
			
			events = []
			for event in pygame.event.get():
				if event.type == QUIT:
					self.quitting = True
				#elif event.type == KEYDOWN and event.key == K_ESCAPE:
				#	self.quitting = True
				else:
					events.append(event)
			self.current.ProcessInput(events)
	
	def Update(self):
		if self.current != None:
			self.current.Update()
		
	def Render(self, vfps, afps):
		if self.current != None:
			self.current.Render(self.screen)
			
			if self.show_fps_counter:
				if self.font == None:
					self.font = Resources.GetFont(255, 255, 255)
				text = self.font.Render("FPS: " + str(vfps))
				self.screen.blit(text, (4, 480 - text.get_height()))
			pygame.display.flip()
	
	def PlaySounds(self):
		if self.current != None and len(self.current.sounds) != 0:
			sounds = self.current.sounds
			self.current.sounds = []
			for sound in sounds:
				path = 'Media' + os.sep + '%SOUNDFOLDER%' + os.sep + sound.replace('/', os.sep).replace('\\', os.sep)
				path = path.replace(os.sep + os.sep, os.sep)
				self.PlaySound(path)
	
	
	def PlaySound(self, path):
		sound = self.sound_cache.get(path)
		if sound == None:
			finalPath =  path.replace('%SOUNDFOLDER%', 'Sounds')
			if not os.path.exists(finalPath):
				finalPath = path.replace('%SOUNDFOLDER%', 'TEMP_Sounds')
			sound = pygame.mixer.Sound(finalPath)
			self.sound_cache[path] = sound
		sound.play()
	
	
	def DoHacks(self, screen):
		
		grass = Resources.ImageLibrary.Get('Tiles/grass.png', 255)
		graygrass = Resources.ImageLibrary.Get('Tiles/grass.png', 0)
		
		wall = Resources.ImageLibrary.Get('Tiles/Interior/wallpaper.png', 255)
		graywall = Resources.ImageLibrary.Get('Tiles/Interior/wallpaper.png', 0)
		
		floor = Resources.ImageLibrary.Get('Tiles/Interior/floor.png', 255)
		grayfloor = Resources.ImageLibrary.Get('Tiles/Interior/floor.png', 0)
		
		# partition the house
		for foo in (('',''), ('p','pink'), ('b','blue')):
			path = os.path.join('Images', 'Tiles', foo[1] + 'house.png')
			bighouse = pygame.image.load(path)
			grayhouse = pygame.image.load('Gray' + path)
			for y in range(0, 7):
				for x in range(0, 5):
					i = y * 5 + x
					image = grass.copy()
					grayimage = graygrass.copy()
					image.blit(bighouse, (-x * 32, -y * 32))
					grayimage.blit(grayhouse, (-x * 32, -y * 32))
					path = os.path.join('Images','Tiles','house',foo[0]+'house'+str(i) + '.png')
					Resources.ImageLibrary.AddVirtualizedImage(path, image)
					Resources.ImageLibrary.AddVirtualizedImage('Gray' + path, grayimage)
		
		
		for foo in ((2, 4, 'green'),(2, 3, 'red'),(2, 3, 'orange')):
			path = os.path.join('Images', 'Tiles', foo[2] + 'tree.png')
			tree = pygame.image.load(path)
			graytree = pygame.image.load('Gray' + path)
			for x in range(0, foo[0]):
				for y in range(0, foo[1]):
					
					i = y * 2 + x
					image = grass.copy()
					grayimage = graygrass.copy()
					image.blit(tree, (-x * 32, -y * 32))
					grayimage.blit(graytree, (-x * 32, -y * 32))
					path = os.path.join('Images', 'Tiles', foo[2] + 'tree' + str(i) + '.png')
					Resources.ImageLibrary.AddVirtualizedImage(path, image)
					Resources.ImageLibrary.AddVirtualizedImage('Gray' + path, grayimage)
					
		
		applyBackgroundAndRename = [
						('grass', 'Images/Tiles/bush1.png', 'Images/Tiles/bush_left.png'),
						('grass', 'Images/Tiles/bush2.png', 'Images/Tiles/bush_center.png'),
						('grass', 'Images/Tiles/bush3.png', 'Images/Tiles/bush_right.png'),
						('wall', 'Images/Tiles/Interior/bed_top.png', 'Images/Tiles/Interior/bedtop.png'),
						('floor', 'Images/Tiles/Interior/bed_bottom.png', 'Images/Tiles/Interior/bedbottom.png'),
						('wall', 'Images/Tiles/Interior/dresser.png', 'Images/Tiles/Interior/dresserA.png'),
						('floor', 'Images/Tiles/Interior/chair.png', 'Images/Tiles/Interior/chairA.png'),
						('floor', 'Images/Tiles/Interior/table.png', 'Images/Tiles/Interior/tableA.png'),
						('floor', 'Images/Tiles/Interior/dresser.png', 'Images/Tiles/Interior/dresserB.png'),
						('grass', 'Images/Tiles/mailbox.png', 'Images/Tiles/mailboxB.png'),
						('grass', 'Images/Tiles/Crowd/bluehouse.png', 'Images/Tiles/Crowd/bhouse.png'),
						('grass', 'Images/Tiles/Crowd/pinkhouse.png', 'Images/Tiles/Crowd/phouse.png'),
						('grass', 'Images/Tiles/Crowd/greenhouse.png', 'Images/Tiles/Crowd/ghouse.png'),
						]
		
		for conversion in applyBackgroundAndRename:
			if conversion[0] == 'grass':
				image = grass.copy()
				grayimage = graygrass.copy()
			elif conversion[0] == 'wall':
				image = wall.copy()
				grayimage = graywall.copy()
			elif conversion[0] == 'floor':
				image = floor.copy()
				grayimage = grayfloor.copy()
			
			origpath = conversion[1].replace('/', os.sep).replace('\\', os.sep)
			origgraypath = 'Gray' + origpath
			
			image.blit(pygame.image.load(origpath).convert_alpha(), (0, 0))
			grayimage.blit(pygame.image.load(origgraypath).convert_alpha(), (0, 0))
			
			fakepath = conversion[2].replace('/', os.sep).replace('\\', os.sep)
			fakegraypath = 'Gray' + fakepath
			Resources.ImageLibrary.AddVirtualizedImage(fakepath, image)
			Resources.ImageLibrary.AddVirtualizedImage(fakegraypath, grayimage)
			