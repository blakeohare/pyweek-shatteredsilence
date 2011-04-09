import Menus
import Game
import pygame
import Resources

class WinScene(Game.GameSceneBase):
	
	def __init__(self, previousScene):
		Game.GameSceneBase.__init__(self)
		self.previousScene = previousScene
		self.tSurf = pygame.Surface((640, 480))
		self.tSurf.set_alpha(30)
		self.font = Resources.GetFont(255, 255, 255)
	
	def ProcessInput(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
					self.next = Menus.Title()
	
	def Update(self):
		pass
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
		self.previousScene.Render(self.tSurf)
		screen.blit(self.tSurf, (0, 0))
		text = self.font.Render('The winner is you!')
		screen.blit(text, ((640 - text.get_width())// 2, (480 - text.get_height()) // 2))
		
class LoseScene(Game.GameSceneBase):
	
	def __init__(self, previousScene):
		Game.GameSceneBase.__init__(self)
		self.previousScene = previousScene
		self.tSurf = pygame.Surface((640, 480))
		self.tSurf.set_alpha(30)
		self.font = Resources.GetFont(255, 255, 255)
	
	def ProcessInput(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
					self.next = Menus.Title()
	
	def Update(self):
		pass
	
	def Render(self, screen):
		screen.fill((0, 0, 0))
		self.previousScene.Render(self.tSurf)
		screen.blit(self.tSurf, (0, 0))
		text = self.font.Render("You're not very good at this.")
		screen.blit(text, ((640 - text.get_width())// 2, (480 - text.get_height()) // 2))
		