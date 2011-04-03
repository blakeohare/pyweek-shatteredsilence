from Game import GameSceneBase
from GamePlay import PlayScene
import pygame
from Resources import ImageLibrary

class Title(GameSceneBase):
    
    def __init__(self):
        GameSceneBase.__init__(self)
    
    def ProcessInput(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.next = PlayScene()

    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((0, 0, 0))
        titleimage = ImageLibrary.Get('title.png')
        screen.blit(titleimage, (10, 10))
        