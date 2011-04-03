import pygame
import os

class ImageLibrary:
    
    def __init__(self):
        self.images = {}
    
    def Get(self, path):
        image = self.images.get(path)
        if image == None:
            newpath = path.replace('\\', '/')
            image = self.images.get(newpath)
            if image != None:
                self.images[path] = image
                return image
            finalpath = ('Images/' + newpath).replace('/', os.sep).replace(os.sep + os.sep, os.sep)
            
            image = pygame.image.load(finalpath)
            self.images[path] = image
        return image