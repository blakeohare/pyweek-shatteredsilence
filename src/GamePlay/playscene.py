import pygame
from Game import GameSceneBase
import GamePlay

class PlayScene(GameSceneBase):
    
    def __init__(self):
        GameSceneBase.__init__(self)
        self.level = GamePlay.Level(64, 64)
        self.cameraX = 0
        self.cameraY = 0
        self.dragStart = None
        self.selection = []
        self.cursorLogicalPosition = (0, 0)
        self.cursorScreenPosition = (0, 0)
        self.suppressDragDraw = True
        
    def ProcessInput(self, events):
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                x = event.pos[0] + self.cameraX
                y = event.pos[1] + self.cameraY
                
                self.SetSelection(self.dragStart, (x, y))
                self.dragStart = None
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = event.pos[0] + self.cameraX
                y = event.pos[1] + self.cameraY
                self.dragStart = (x, y)
                self.suppressDragDraw = False
            
            elif event.type == pygame.MOUSEMOTION:
                self.cursorScreenPosition = event.pos
                x = event.pos[0] + self.cameraX
                y = event.pos[1] + self.cameraY
                self.cursorLogicalPosition = (x, y)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.MoveSelectionToTarget(event.pos[0] - self.cameraX, event.pos[1] - self.cameraY)
    
    def MoveSelectionToTarget(self, targetX, targetY):
        for sprite in self.selection:
            sprite.SetTarget(targetX, targetY)
    
    def SetSelection(self, startDrag, endDrag):
        left = startDrag[0]
        top = startDrag[1]
        right = endDrag[0]
        bottom = endDrag[1]
        
        if left > right:
            t = left
            left = right
            right = t
        if top > bottom:
            t = top
            top = bottom
            bottom = t
        
        if right - left < 16 and bottom - top < 16:
            sprite = self.level.GetSpriteHitTest((right + left) // 2, (bottom + top) // 2)
            if sprite != None:
                self.selection =  [sprite]
            else:
                self.selection = [] 
        else:
            self.selection = self.level.GetSpritesInRange(left, top, right, bottom)
            
    def Update(self):
        
        for sprite in self.level.sprites:
            sprite.Update()
    
    def Render(self, screen):
        self.level.RenderTiles(screen, self.cameraX, self.cameraY)
        self.RenderSelection(screen)
        self.level.RenderSprites(screen, self.cameraX, self.cameraY)
        self.RenderDrag(screen)
    
    def RenderSelection(self, screen):
        for sprite in self.selection:
            coords = sprite.RenderCoordinates(self.cameraX, self.cameraY)
            left = coords[0] - 4
            top = coords[1] + sprite.R - 3
            width = sprite.R * 2 + 8
            height = sprite.R + 6
            
            pygame.draw.ellipse(screen, (255, 255, 0), pygame.Rect(left, top, width, height), 2)
    
    def RenderDrag(self, screen):
        
        if self.suppressDragDraw: return
        if self.dragStart == None: return
        
        left = self.dragStart[0] - self.cameraX
        right = self.cursorScreenPosition[0]
        top = self.dragStart[1] - self.cameraY
        bottom = self.cursorScreenPosition[1]
        
        if left > right:
            t = left
            left = right
            right = t
        if bottom < top:
            t = bottom
            bottom = top
            top = t
        
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(left, top, right - left, bottom - top), 1)