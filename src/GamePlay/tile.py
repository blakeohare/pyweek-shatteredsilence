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
            'horizontal_crosswalk' : TileTemplate('crosswalk2', True),
            'building/roof1' : TileTemplate('building/roof1', False),
            'building/roof2' : TileTemplate('building/roof2', False),
            'building/roof3' : TileTemplate('building/roof3', False),
            'building/roof4' : TileTemplate('building/roof4', False),
            'building/roof5' : TileTemplate('building/roof5', False),
            'building/roof6' : TileTemplate('building/roof6', False),
            'building/roof7' : TileTemplate('building/roof7', False),
            'building/roof8' : TileTemplate('building/roof8', False),
            'building/roof9' : TileTemplate('building/roof9', False),
            'building/building1' : TileTemplate('building/building1', False),
            'building/building2' : TileTemplate('building/building2', False),
            'building/building3' : TileTemplate('building/building3', False),
            'building/building4' : TileTemplate('building/building4', False),
            'building/building5' : TileTemplate('building/building5', False),
            'building/building6' : TileTemplate('building/building6', False)         
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