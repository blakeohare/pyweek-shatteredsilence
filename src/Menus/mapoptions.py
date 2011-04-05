import pygame
from Game import GameSceneBase
from GamePlay import PlayScene
import Resources
from GamePlay import LevelSeed

class MapOptions(GameSceneBase):
	def __init__(self):
		GameSceneBase.__init__(self)
		self.font = Resources.GetFont(255, 255, 0)
	
	def ProcessInput(self, events):
		
		for event in events:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				args = {
						'width' : 64, #these are tiles, not pixels
						'height' : 64,
						'mode' : 'individual', # individual, crowd, or region
						'progress' : False, # True if you want to move up to the next zoom level when you complete 80% conversion
						'minutes' : -1, # -1 for un-timed mode. Otherwise, it's the number of minutes you have to complete 80% conversion
						
						# individual mode settings
						'citizens' : 100,
						'police' : 20,
						
						# crowd mode settings
						'city_centers' : 1
						
						# region mode settings
						# ????????
						}
				self.next = PlayScene(LevelSeed(None, args))
	
	def Update(self):
		pass
	
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
		text = self.font.Render("Just press enter for now")
		screen.blit(text, (10, 10))
		
	