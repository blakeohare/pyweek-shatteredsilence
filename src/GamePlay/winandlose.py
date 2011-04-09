import Menus
import Game
import pygame
import Resources

class WinScene(Game.GameSceneBase):
	
	def __init__(self, previousScene):
		Game.GameSceneBase.__init__(self)
		self.previousScene = previousScene
	
	def ProcessInput(self, events):
		pass
	
	def Update(self):
		self.next = Menus.GameWin(self.previousScene)
	
	def Render(self, screen):
		self.previousScene.Render(screen)
		
class LoseScene(Game.GameSceneBase):
	def __init__(self, previousScene):
		Game.GameSceneBase.__init__(self)
		self.previousScene = previousScene
	
	def ProcessInput(self, events):
		pass
	
	def Update(self):
		self.next = Menus.GameOver(self.previousScene)
	
	def Render(self, screen):
		self.previousScene.Render(screen)		