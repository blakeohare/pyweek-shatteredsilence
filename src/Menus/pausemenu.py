import pygame
import Menus
import Game


class GamePauseMenu(Game.GameSceneBase):
	
	def __init__(self, currentScene):
		Game.GameSceneBase.__init__(self)
		self.previousScene = currentScene
		self.bg = pygame.Surface((640, 480))
		self.bg.set_alpha(50)
	
	def ProcessInput(self, events):
		
		
		pass
	
	def Update(self):
		pass
	
	def ReturnToGame(self):
		self.next = self.previousScene
		self.previousScene.next = self.previousScene
	
	def ReturnToMainMenu(self):
		self.next = Menus.Title()
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
		self.previousScene.Render(self.bg)
		screen.blit(self.bg, (0, 0))
		
		# draw two mouse-clickable options: "Return to game" and "Exit to Main Menu"
		