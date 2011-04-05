from Resources import ImageLibrary

class TileTemplate:
    
    def __init__(self, image, passable):
        self.image = 'Tiles/' + image + '.png'
        self.passable = passable

    def GetImage(self, colorization):
        return ImageLibrary.Get(self.image, colorization)

_tileStore = {
            'sidewalk' : TileTemplate('sidewalk', True),
            'grass' : TileTemplate('grass', True),
            'asphault' : TileTemplate('street', True),
            'yellow_line_horizontal' : TileTemplate('streetlines2', True),
            'yellow_line_vertical' : TileTemplate('streetlines1', True),
            'sidewalk_corner1' : TileTemplate('sidewalkcorner1', True),
            'sidewalk_corner2' : TileTemplate('sidewalkcorner2', True),
            'sidewalk_corner3' : TileTemplate('sidewalkcorner3', True),
            'sidewalk_corner4' : TileTemplate('sidewalkcorner4', True),
            'vertical_crosswalk' : TileTemplate('crosswalk1', True),
            'horizontal_crosswalk' : TileTemplate('crosswalk2', True)         
            }

def MakeTile(key, x, y):
    global _tileStore
    if key == None: key = 'grass'
    return Tile(x, y, _tileStore[key])

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