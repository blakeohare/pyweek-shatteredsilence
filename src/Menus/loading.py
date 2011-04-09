import os
import time
import Game
import GamePlay
import Resources
import Menus

class LoadingScreen(Game.GameSceneBase):
	
	def __init__(self):
		Game.GameSceneBase.__init__(self)
		self.counter = 0
		self.font = Resources.GetFont(255, 255, 255)
		self.x = None
		self.progress = 0
		self.cacheExists = Resources.ImageLibrary.CacheExists()
		if self.cacheExists:
			Resources.ImageLibrary.PrepForLoadCache()
	
	
	def ProcessInput(self, events):
		pass
	
	def LoadNextImage(self):
		if self.cacheExists:
			start = time.time()
			end = start
			while end - start < .02:
				notdone = Resources.ImageLibrary.LoadNextCache()
				progress = Resources.ImageLibrary.CacheLoadProgress()
				if notdone and progress == 100:
					progress = 99
					
				end = time.time()

		else:
			progress = GamePlay.LoadNextThing()
		return progress
	
	def Update(self):
		while True:
			progress = self.LoadNextImage()
			if progress == None or progress >= 100:
				self.MoveToNextScene()
				Resources.ImageLibrary.fullyInitialized = True
				
				self.progress = 100
				return
			else:
				self.progress = progress
		self.counter += 1
	
	def MoveToNextScene(self):
		if os.path.exists('cookie.txt'):
			
			self.next = Menus.Title()
		else:
			self.next = Menus.Intro()
	
	def Render(self, screen):
		
		text = 'Loading' + ('.' * ((self.counter) % 4))
		text2 = str(self.progress) + '%'
		image = self.font.Render(text)
		screen.fill((0, 0, 0))
		
		return
		
		if self.x == None:
			self.x = (640 - image.get_width()) / 2
		y = (480 - image.get_height()) / 2 - 50
		screen.blit(image, (self.x, y))
		screen.blit(self.font.Render(text2), (self.x + 20, y + 20))
	