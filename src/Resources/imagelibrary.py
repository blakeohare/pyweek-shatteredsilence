import pygame
import os

class ImageLibrary:
    
    def __init__(self):
        self.intervals = 50
        self.images = []
        for i in range(self.intervals):
            self.images.append({})
            
    # opacity is 0-255
    def Get(self, path, opacity=None):
        if opacity == None:
            field = self.intervals - 1
        else:
            perInterval = 255.0 / self.intervals
            
            field = int(opacity / perInterval)
            
        if field > self.intervals - 1: field = self.intervals - 1
        images = self.images[field]
        image = images.get(path)
        if image == None:
            newpath = path.replace('\\', '/')
            image = images.get(newpath)
            if image != None:
                self.MirrorImage(path, newpath)
                return images.get(newpath)
            finalpath = ('Images/' + newpath).replace('/', os.sep).replace(os.sep + os.sep, os.sep)
            
            image = pygame.image.load(finalpath).convert_alpha()
            image = self.InitializeImages(path, image, opacity == None)
            return self.Get(path, opacity)
            
        return image
    
    def MirrorImage(self, targetPath, sourcePath):
        for i in range(self.intervals):
            self.images[i][targetPath] = self.images[i][sourcePath]
    
    def InitializeImages(self, path, colorImage, disableGrayscale):
        if disableGrayscale:
            for i in range(0, self.intervals):
                self.images[i][path] = colorImage
            return
        
        width = colorImage.get_width()
        height = colorImage.get_height()
        grayImage = self.ConvertToGrayscale(colorImage)
        self.images[0][path] = grayImage
        self.images[self.intervals - 1][path] = colorImage
        onePixel = pygame.Surface((1, 1)).convert()
        mask = pygame.mask.from_surface(colorImage)
        for i in range(1, self.intervals - 1):
            copy = grayImage.copy()
            copy.blit(grayImage, (0, 0))
            onePixel.set_alpha(i * 255 // self.intervals)
            y = 0
            while y < height:
                x = 0
                while x < width:
                    if mask.get_at((x, y)) != 0:
                        onePixel.blit(colorImage, (-x, -y))
                        copy.blit(onePixel, (x, y))
                    x += 1
                y += 1

            self.images[i][path] = copy
            
    
    def ConvertToGrayscale(self, image):
        
        width =  image.get_width()
        height = image.get_height()
        
        colorpixels = pygame.surfarray.pixels3d(image)
        grayimage = image.copy()
        graypixels = pygame.surfarray.pixels3d(grayimage)
        
        x = 0
        while x < width:
            
            y = 0
            while y < height:
                
                v = colorpixels[x][y]
                gray = int((0.0 + v[0] + v[1] + v[2]) / 3)
                graypixels[x][y][0] = gray
                graypixels[x][y][1] = gray
                graypixels[x][y][2] = gray
                
                y += 1
            x += 1
        
        return grayimage