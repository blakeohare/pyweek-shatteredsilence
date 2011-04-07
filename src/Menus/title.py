from Game import GameSceneBase
from GamePlay import PlayScene
import Menus
import pygame
from Resources import ImageLibrary
import Resources
from GamePlay import LevelSeed

class Title(GameSceneBase):
	
	def __init__(self):
		GameSceneBase.__init__(self)
		self.whitefont = Resources.GetFont(255, 255, 255)
		self.yellowfont = Resources.GetFont(255, 255, 0)
		self.index = 0
		self.options = [
						'Story Mode',
						'Custom Game',
						'Intro',
						'Credits',
						'Quit',
						'[TEMP] Map Test Mode'
						]
	
	def ProcessInput(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if self.index == 0:
						self.next = PlayScene(LevelSeed('level1', None))
					elif self.index == 1:
						self.next = Menus.MapOptions()
					elif self.index == 2:
						self.next = Menus.Intro()
					elif self.index == 3:
						self.next = Menus.Credits()
					elif self.index == 4:
						self.next = None
					else:
						self.next = PlayScene(LevelSeed('testlevel', None))
				elif event.key == pygame.K_UP:
					self.index -= 1
					if self.index < 0:
						self.index = len(self.options) - 1
				elif event.key == pygame.K_DOWN:
					self.index += 1
					if self.index >= len(self.options):
						self.index = 0

	def Update(self):
		pass
	
	def Render(self, screen):
		screen.fill((80, 90, 100))
		titleimage = ImageLibrary.Get('title.png')
		screen.blit(titleimage, (10, 10))
		
		y = 320
		x = 100
		for i in range(len(self.options)):
			
			if i == self.index:
				font = self.yellowfont
				cursor = font.Render('>')
				screen.blit(cursor, (x - 12, y)) 
			else:
				font = self.whitefont
			
			screen.blit(font.Render(self.options[i]), (x, y))
			y += 20