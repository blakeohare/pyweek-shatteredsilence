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
			'building/building6' : TileTemplate('building/building6', False),
			'building/doodad' : TileTemplate('building/roofdoodad', False),
			'building/door' : TileTemplate('building/buildingdoor', False),
			'sidewalkchalkboy' : TileTemplate('sidewalkchalkboy', True),
			'sidewalkchalkgirl' : TileTemplate('sidewalkchalkgirl', True),
			'sidewalkchalkunicorn' : TileTemplate('sidewalkchalkunicorn', True),
			'house0' : TileTemplate('house/house0', True),
			'house1' : TileTemplate('house/house1', False),
			'house2' : TileTemplate('house/house2', True),
			'house3' : TileTemplate('house/house3', True),
			'house4' : TileTemplate('house/house4', True),
			'house5' : TileTemplate('house/house5', False),
			'house6' : TileTemplate('house/house6', False),
			'house7' : TileTemplate('house/house7', False),
			'house8' : TileTemplate('house/house8', True),
			'house9' : TileTemplate('house/house9', True),
			'house10' : TileTemplate('house/house10', False),
			'house11' : TileTemplate('house/house11', False),
			'house12' : TileTemplate('house/house12', False),
			'house13' : TileTemplate('house/house13', False),
			'house14' : TileTemplate('house/house14', True),
			'house15' : TileTemplate('house/house15', False),
			'house16' : TileTemplate('house/house16', False),
			'house17' : TileTemplate('house/house17', False),
			'house18' : TileTemplate('house/house18', False),
			'house19' : TileTemplate('house/house19', False),
			'house20' : TileTemplate('house/house20', False),
			'house21' : TileTemplate('house/house21', False),
			'house22' : TileTemplate('house/house22', False),
			'house23' : TileTemplate('house/house23', False),
			'house24' : TileTemplate('house/house24', False),
			'house25' : TileTemplate('house/house25', False),
			'house26' : TileTemplate('house/house26', False),
			'house27' : TileTemplate('house/house27', False),
			'house28' : TileTemplate('house/house28', False),
			'house29' : TileTemplate('house/house29', False),
			'house30' : TileTemplate('house/house30', False),
			'house31' : TileTemplate('house/house31', False),
			'house32' : TileTemplate('house/house32', False),
			'house33' : TileTemplate('house/house33', False),
			'house34' : TileTemplate('house/house34', False)
			}

def MakeTile(key, x, y):
	global _tileStore
	if key == None: key = 'grass'
	return Tile(x, y, _tileStore[key])

class Tile:
	
	def __init__(self, x, y, template):
		self.template = template
		self.IsPassable = template.passable
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