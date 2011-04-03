from Resources import ImageLibrary

class TileTemplate:
    
    def __init__(self):
        pass
    
    def GetImage(self, colorization):
        return ImageLibrary.Get('temp_grass.png')

class Tile:
    
    def __init__(self, x, y, template):
        self.template = template
        self.x = x
        self.y = y
        self.colorization = 0
        self.image = template.GetImage(0)
    
    def Update(self, counter):
        self.colorization -= 5
        self.image = None
    
    def GetImage(self):
        self.image = self.template.GetImage(self.colorization)