import pygame
from pygame.locals import *
import time
import os
import Resources

class GameLoop:
	
	def __init__(self, width, height, framesPerSecond):
		self.width = width
		self.height = height
		self.fps = framesPerSecond
		pygame.init()
		self.screen = pygame.display.set_mode((640, 480))
		self.DoHacks(self.screen)
		self.quitting = False
		self.show_fps_counter = True
		self.lastNFrames = []
		self.font = None
	
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
			
			end = time.time()
			
			diff = end - start
			
			targetSPF = 1.0 / self.fps
			if diff < targetSPF:
				delay = targetSPF - diff
				time.sleep(delay)
			
			if self.show_fps_counter and diff > 0:
				vfps = 1.0 / diff
				afps = 1.0 / (time.time() - start)
					
	
	def ProcessInput(self):
		
		if self.current != None:
			
			events = []
			for event in pygame.event.get():
				if event.type == QUIT:
					self.quitting = True
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					self.quitting = True
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
	
	
	
	
	
	
	
	def DoHacks(self, screen):
		
		# partition the house
		screen.fill((0, 0, 255))
		bighouse = Resources.ImageLibrary.Get('Tiles/house.png')
		for y in range(0, 7):
			for x in range(0, 5):
				i = y * 5 + x
				image = Resources.ImageLibrary.Get('Tiles/grass.png', 255).copy()
				image.blit(bighouse, (-x * 32, -y * 32))
				path = os.path.join('Images','Tiles','house','house'+str(i) + '.png')
				Resources.ImageLibrary.AddVirtualizedImage(path, image)