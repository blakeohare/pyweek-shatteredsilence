import pygame
import Resources

class Border:
   def __init__(self):
      self._border_cache = {}
      self.TL = 0
      self.TC = 1
      self.TR = 2
      self.MT = 3
      self.MC = 4
      self.MB = 5
      self.BL = 6
      self.BC = 7
      self.BR = 8
      self.Load()
   
   def Load(self):
      _borders = Resources.ImageLibrary.Get('borders.png')
      
      i = 0
      while i < 9:
         left = (i % 3) * 17 + 1
         top = (i // 3) * 17 + 1
         
         self._border_cache[i] = _borders.subsurface(pygame.Rect(left, top, 16, 16))
    
   def GetTile(self, tile):
      if (tile < 0) or (tile > 8):
         return None
      
      return self._border_cache[tile]
   
   def MakeSurface(self, width, height):
      if (width < 2) or (height < 2):
         raise "Invalid size."
      
      surf = pygame.Surface((width * 16, height * 16))
      
      _gt = self.GetTile
      for x in xrange(width):
         for y in xrange(height):
            tile = None
            
            if (x == 0):
               if (y == 0):
                  tile = _gt(self.TL)
               elif (y == (height - 1)):
                  tile = _gt(self.BL)
               else:
                  tile = _gt(self.ML)
            elif (x == (width - 1)):
               if (y == 0):
                  tile = _gt(self.TR)
               elif (y == (height - 1)):
                  tile = _gt(self.MR)
               else:
                  tile = _gt(self.BR)
            else:
               if (y == 0):
                  tile = _gt(self.MT)
               elif (y == (height - 1)):
                  tile = _gt(self.MB)
               else:
                  tile = _gt(self.MC)
            if not Tile:
               raise "No tile found for (%d,%d)" % (x, y)
            
            surf.blit(tile, (x * 16, y * 16))
      
      return surf