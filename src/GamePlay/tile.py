from Resources import ImageLibrary

class TileTemplate:
    
    def __init__(self):
        pass
    
    def GetImage(self, colorization):
        return ImageLibrary.Get('Tiles/grass.png', colorization)

class Tile:
    
    def __init__(self, x, y, template):
        self.template = template
        self.X = x
        self.PixelX = x * 32
        self.Y = y
        self.PixelY = y * 32
        self.colorization = -999
        self.image = template.GetImage(0)
        self.get_image = self.template.GetImage
    
    def Update(self, counter):
        self.colorization -= 5
    
    def GetImage(self, counter):
        
        return self.get_image((self.colorization - counter) * 3 + 255)
    
    def SetColorization(self, value):
        if self.colorization < value:
            self.colorization = value