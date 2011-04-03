from Game import GameSceneBase
import pygame

class Title(GameSceneBase):
    
    def __init__(self):
        GameSceneBase.__init__(self)
        self.x = 0
        self.y = 0
    
    def ProcessInput(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.next = None

    def Update(self):
        self.x += 1
        self.y += 2
        self.x = self.x % 640
        self.y = self.y % 480
    
    def Render(self, screen):
        screen.fill((0, 0, 0))
        for xoffset in (0, -1):
            for yOffset in (0, -1):
                pygame.draw.rect(screen, (0, 100, 255), pygame.Rect(self.x + xoffset, self.y + yOffset, 32, 32))
        