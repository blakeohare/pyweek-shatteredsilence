import pygame
from pygame.locals import *
import time

class GameLoop:
    
    def __init__(self, width, height, framesPerSecond):
        self.width = width
        self.height = height
        self.fps = framesPerSecond
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.quitting = False
    
    def Start(self, startingScene):
        self.current = startingScene
        
        self.DoLoop()
    
    
    def DoLoop(self):
        
        while not self.quitting:
            start = time.time()
            
            end = time.time()
            
            self.ProcessInput()
            
            self.Update()
            
            self.Render()    
            
            self.current = self.current.next
            
            if self.current == None:
                self.quitting = True
            
            diff = end - start
            
            targetSPF = 1.0 / self.fps
            if diff < targetSPF:
                delay = targetSPF - diff
                time.sleep(delay)
    
    def ProcessInput(self):
        
        if self.current != None:
            
            events = []
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quitting = True
                else:
                    events.append(event)
            self.current.ProcessInput(events)
    
    def Update(self):
        if self.current != None:
            self.current.Update()
        
    def Render(self):
        if self.current != None:
            self.current.Render(self.screen)
            pygame.display.flip()
    
    
    