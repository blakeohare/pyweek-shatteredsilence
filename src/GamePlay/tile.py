import os
from Resources import ImageLibrary

class TileTemplate:
	
	def __init__(self, image, passable):
		self.image = 'Tiles/' + image + '.png'
		self.passable = passable

	def GetImage(self, colorization):
		return ImageLibrary.Get(self.image, colorization)

_tilesToBeLoaded = {}

_tileStore = {
			#suburbia
			'cobblestone' : TileTemplate('cobblestone', True),
			'mailbox' : TileTemplate('mailboxB', False),
			
			# Interior
			'int/black' : TileTemplate('black', False),
			'int/bedtop' : TileTemplate('Interior/bedtop', False),
			'int/bedbottom' : TileTemplate('Interior/bedbottom', False),
			'int/chair' : TileTemplate('Interior/chairA', False),
			'int/dresser' : TileTemplate('Interior/dresserA', False),
			'int/dresserfloor' : TileTemplate('Interior/dresserB', False),
			'int/table' : TileTemplate('Interior/tableA', False),
			'int/bookcase' : TileTemplate('Interior/bookcase', False),
			'int/door' : TileTemplate('Interior/door', False),
			'int/wall' : TileTemplate('Interior/wallpaper', False),
			'int/floor' : TileTemplate('Interior/floor', True),
			'int/phonograph' : TileTemplate('Interior/phonograph', True),
			
			'int/trim1' : TileTemplate('Interior/trim1', False),
			'int/trim2' : TileTemplate('Interior/trim2', False),
			'int/trim3' : TileTemplate('Interior/trim3', False),
			'int/trim4' : TileTemplate('Interior/trim4', False),
			'int/trim6' : TileTemplate('Interior/trim6', False),
			'int/trim7' : TileTemplate('Interior/trim7', False),
			'int/trim8' : TileTemplate('Interior/trim8', False),
			'int/trim9' : TileTemplate('Interior/trim9', False),
			
			# Outside
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
			'bush_left' : TileTemplate('bush_left', False),
			'bush_center' : TileTemplate('bush_center', False),
			'bush_right' : TileTemplate('bush_right', False),
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
			'house34' : TileTemplate('house/house34', False),
			'bhouse0' : TileTemplate('house/bhouse0', True),
			'bhouse1' : TileTemplate('house/bhouse1', False),
			'bhouse2' : TileTemplate('house/bhouse2', True),
			'bhouse3' : TileTemplate('house/bhouse3', True),
			'bhouse4' : TileTemplate('house/bhouse4', True),
			'bhouse5' : TileTemplate('house/bhouse5', False),
			'bhouse6' : TileTemplate('house/bhouse6', False),
			'bhouse7' : TileTemplate('house/bhouse7', False),
			'bhouse8' : TileTemplate('house/bhouse8', True),
			'bhouse9' : TileTemplate('house/bhouse9', True),
			'bhouse10' : TileTemplate('house/bhouse10', False),
			'bhouse11' : TileTemplate('house/bhouse11', False),
			'bhouse12' : TileTemplate('house/bhouse12', False),
			'bhouse13' : TileTemplate('house/bhouse13', False),
			'bhouse14' : TileTemplate('house/bhouse14', True),
			'bhouse15' : TileTemplate('house/bhouse15', False),
			'bhouse16' : TileTemplate('house/bhouse16', False),
			'bhouse17' : TileTemplate('house/bhouse17', False),
			'bhouse18' : TileTemplate('house/bhouse18', False),
			'bhouse19' : TileTemplate('house/bhouse19', False),
			'bhouse20' : TileTemplate('house/bhouse20', False),
			'bhouse21' : TileTemplate('house/bhouse21', False),
			'bhouse22' : TileTemplate('house/bhouse22', False),
			'bhouse23' : TileTemplate('house/bhouse23', False),
			'bhouse24' : TileTemplate('house/bhouse24', False),
			'bhouse25' : TileTemplate('house/bhouse25', False),
			'bhouse26' : TileTemplate('house/bhouse26', False),
			'bhouse27' : TileTemplate('house/bhouse27', False),
			'bhouse28' : TileTemplate('house/bhouse28', False),
			'bhouse29' : TileTemplate('house/bhouse29', False),
			'bhouse30' : TileTemplate('house/bhouse30', False),
			'bhouse31' : TileTemplate('house/bhouse31', False),
			'bhouse32' : TileTemplate('house/bhouse32', False),
			'bhouse33' : TileTemplate('house/bhouse33', False),
			'bhouse34' : TileTemplate('house/bhouse34', False),
			'phouse0' : TileTemplate('house/phouse0', True),
			'phouse1' : TileTemplate('house/phouse1', False),
			'phouse2' : TileTemplate('house/phouse2', True),
			'phouse3' : TileTemplate('house/phouse3', True),
			'phouse4' : TileTemplate('house/phouse4', True),
			'phouse5' : TileTemplate('house/phouse5', False),
			'phouse6' : TileTemplate('house/phouse6', False),
			'phouse7' : TileTemplate('house/phouse7', False),
			'phouse8' : TileTemplate('house/phouse8', True),
			'phouse9' : TileTemplate('house/phouse9', True),
			'phouse10' : TileTemplate('house/phouse10', False),
			'phouse11' : TileTemplate('house/phouse11', False),
			'phouse12' : TileTemplate('house/phouse12', False),
			'phouse13' : TileTemplate('house/phouse13', False),
			'phouse14' : TileTemplate('house/phouse14', True),
			'phouse15' : TileTemplate('house/phouse15', False),
			'phouse16' : TileTemplate('house/phouse16', False),
			'phouse17' : TileTemplate('house/phouse17', False),
			'phouse18' : TileTemplate('house/phouse18', False),
			'phouse19' : TileTemplate('house/phouse19', False),
			'phouse20' : TileTemplate('house/phouse20', False),
			'phouse21' : TileTemplate('house/phouse21', False),
			'phouse22' : TileTemplate('house/phouse22', False),
			'phouse23' : TileTemplate('house/phouse23', False),
			'phouse24' : TileTemplate('house/phouse24', False),
			'phouse25' : TileTemplate('house/phouse25', False),
			'phouse26' : TileTemplate('house/phouse26', False),
			'phouse27' : TileTemplate('house/phouse27', False),
			'phouse28' : TileTemplate('house/phouse28', False),
			'phouse29' : TileTemplate('house/phouse29', False),
			'phouse30' : TileTemplate('house/phouse30', False),
			'phouse31' : TileTemplate('house/phouse31', False),
			'phouse32' : TileTemplate('house/phouse32', False),
			'phouse33' : TileTemplate('house/phouse33', False),
			'phouse34' : TileTemplate('house/phouse34', False)
			}

_loadComplete = False

def _GetAllImages(folder):
	output = []
	for file in os.listdir('Images' + os.sep + folder):
		fullpath = folder + os.sep + file
		if os.path.isdir('Images' + os.sep + fullpath):
			output += _GetAllImages(fullpath)
		elif file.endswith('.png'):
			output.append(fullpath)
	return output

_totalLoadsIncSprites = _GetAllImages('Tiles') + _GetAllImages('Sprites')
_totalLoadsCount = len(_totalLoadsIncSprites)

def LoadNextThing():
	global _totalLoadsCount, _totalLoadsIncSprites
	
	progress = LoadNextTile()
	
	progressB = 100
	if len(_totalLoadsIncSprites) > 0:
		path = _totalLoadsIncSprites[0]
		_totalLoadsIncSprites = _totalLoadsIncSprites[1:]
		ImageLibrary.Get(path, 0)
		progressB = 100 - 100 * len(_totalLoadsIncSprites) // _totalLoadsCount
	
	done = progress == None and len(_totalLoadsIncSprites) == 0
	
	if done: return None
	
	if progress == None: progress = 100
	if progressB == None: progressB = 100
	
	return (progress + progressB) // 2 

def LoadNextTile():
	global _tileStore, _tilesToBeLoaded, _loadComplete
	
	if _loadComplete: return None
	
	if len(_tilesToBeLoaded) == 0 and not _loadComplete:
		for key in _tileStore.keys():
			_tilesToBeLoaded[key] = _tileStore[key]
	tiles_left = len(_tilesToBeLoaded)
	total_tiles = len(_tileStore)
	if len(_tilesToBeLoaded) > 0:
		
		for key in _tilesToBeLoaded.keys():
			_tileStore[key].GetImage(0)
			_tilesToBeLoaded.pop(key)
			if len(_tilesToBeLoaded) == 0:
				_loadComplete = True
			return 100 - 100 * tiles_left // total_tiles
		
	return None
	
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
		self.permacolor = -1 # if colorization is lower than this, use this value instead
		self.image = template.GetImage(0)
		self.get_image = self.template.GetImage
	
	def Update(self, counter):
		self.colorization -= 5
	
	def GetImage(self, counter):
		color = (self.colorization - counter) * 3 + 255
		if color < self.permacolor:
			color = self.permacolor
		return self.get_image(color)
	
	def SetMinColorIntensity(self, color):
		self.permacolor = color
	
	def SetColorization(self, value):
		if self.colorization < value:
			self.colorization = value