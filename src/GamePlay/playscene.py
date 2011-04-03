import pygame
from Game import GameSceneBase
import GamePlay

class PlayScene(GameSceneBase):
    
    def __init__(self):
        GameSceneBase.__init__(self)
        self.level = GamePlay.Level(64, 64)
        self.cameraX = 0
        self.cameraY = 0
        
    def ProcessInput(self, events):
        pass
    
    def Update(self):
        pass
    
    def Render(self, screen):
        self.level.RenderTiles(screen, self.cameraX, self.cameraY)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 10, 32, 32))
        