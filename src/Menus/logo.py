import Menus

from Game import GameSceneBase
from Resources import ImageLibrary
import pygame

class Logo(GameSceneBase):
    
    def __init__(self):
        GameSceneBase.__init__(self)
        self.counter = 0
        self.duration = 60
        self.fadeRatio = 6.0 # 1/4th of the total length of the logo display is fade in
        self.intermediateScreen = pygame.Surface((640, 480))
    
    def ProcessInput(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                newcounter = self.duration * (self.fadeRatio - 1) / self.fadeRatio
                if newcounter > self.counter:
                    self.counter = newcounter
    
    def Update(self):
        self.counter += 1
        if self.counter > self.duration:
            self.next = Menus.Title()
    
    def Opacity(self):
        
        if self.counter < self.duration / self.fadeRatio:
            opacity = self.counter / (self.duration / self.fadeRatio)
        elif self.counter > self.duration * (self.fadeRatio-1) / self.fadeRatio:
            opacity = 1 - (self.counter - (self.fadeRatio - 1) * self.duration / self.fadeRatio) / (self.duration / self.fadeRatio)
        else:
            opacity = 1
        
        opacity = int(opacity * 255)
        
        if opacity < 0: return 0
        if opacity > 255: return 255
        return opacity
    
    def Render(self, screen):
        screen.fill((0, 0, 0))
        logo = ImageLibrary.Get('logo.png')
        
        opacity = self.Opacity()
        self.intermediateScreen.blit(logo, (200, 100))
        self.intermediateScreen.set_alpha(opacity)
        screen.blit(self.intermediateScreen, (0, 0))