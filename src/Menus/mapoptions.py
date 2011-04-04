import pygame
from Game import GameSceneBase
from GamePlay import PlayScene
from Resources import Font
from GamePlay import LevelSeed

class MapOptions(GameSceneBase):
    def __init__(self):
        GameSceneBase.__init__(self)
        self.font = Font((255, 255, 0))
    
    def ProcessInput(self, events):
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.next = PlayScene(LevelSeed())
    
    def Update(self):
        pass
    
    
    def Render(self, screen):
        screen.fill((0, 0, 0))
        text = self.font.Render("Just press enter for now")
        screen.blit(text, (10, 10))
        
    