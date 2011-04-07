import pygame
import os

def _buildPath(path):
   path = path.replace('\\', '/')
   return ('Fonts/' + path).replace('/', os.sep).replace(os.sep + os.sep, os.sep)

class TTF_Font:
   def __init__(self, file, sz=28):
      #TODO: cache
      self._font = pygame.font.Font(_buildPath(file), sz)
   
   def Render(self, txt, color = pygame.Color(0, 0, 0)):
      return self._font.render(txt, True, color)