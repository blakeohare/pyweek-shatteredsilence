from Resources import ImageLibrary

class TileTemplate:
    
    def __init__(self):
        pass
    
    def GetImage(self, colorization):
        return ImageLibrary.Get('temp_grass.png', colorization)

class Tile:
    
    def __init__(self, x, y, template):
        self.template = template
        self.X = x
        self.PixelX = x * 32
        self.Y = y
        self.PixelY = y * 32
        self.colorization = 0
        self.image = template.GetImage(0)
    
    def Update(self, counter):
        self.colorization -= 5
    
    def GetImage(self, opacity):
        return self.template.GetImage(opacity)
        