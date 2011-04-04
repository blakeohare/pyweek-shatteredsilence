import pygame
from Game import GameSceneBase
from Resources import Font
import Menus

class Credits(GameSceneBase):
    def __init__(self):
        GameSceneBase.__init__(self)
        self.font = Font((255, 255, 0))
    
    def ProcessInput(self, events):
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.next = Menus.Title()
    
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((0, 0, 0))
        text = self.font.Render("Nothing here yet. -ENTER- to go back. ")
        screen.blit(text, (10, 10))
        
    