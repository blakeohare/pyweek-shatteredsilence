import MapGen
import GamePlay
import random


_registeredSeeds = None

def PopNextSeed():
	global _registeredSeeds
	
	
	if len(_registeredSeeds) == 0: return None
	first = _registeredSeeds[0]
	_registeredSeeds = _registeredSeeds[1:]
	
	return first

class CustomGameBuilder:
	
	def __init__(self, args):
		self.args = args
		self.doProgress = args['progress'] # bool
		self.startZoom = args['zoom_level'] # 0-8
		self.mapSize = args['map_size'] # 1, 2, 3
		self.minutes = args['minutes'] # -1 for infinite
		
		args['isCrowd'] = self.startZoom >= 5
		args['mode'] = 'individual'
		if args['isCrowd']:
			args['mode'] = 'crowd'
		
	def GetPlayScene(self):
		global _registeredSeeds
		_registeredSeeds = None
		
		levels = []
		
		width = 28
		height = 24
		if self.mapSize == 2:
			width = 42
			height = 36
		elif self.mapSize == 3:
			width = 64
			height = 48
		
		swidth = width
		sheight = height
		
		for i in range(9):
			if i == 5:
				width = swidth
				height = sheight
			levels.append((width, height))
			width = int(width * 1.6)
			height = int(height * 1.6)
		
		if self.startZoom < 5:
			levels = levels[:5]
		else:
			levels = levels[5:]
		
		isCrowd = self.args['isCrowd']
		
		lastWidth = levels[-1][0]
		lastHeight = levels[-1][1]
		
		lastLevel = MapGen.Generator(lastWidth, lastHeight, True, isCrowd)
		
		while not lastLevel.IsDone():
			lastLevel.DoNextTask()
		commands = lastLevel.commands
		lastLevel = MapGen.BuildMapFromCommands(commands, width, height, None, None, None)
		
		
		# Generate tiles for big map
		
		# generate empty maps for smaller maps
		maps = []
		for level in levels:
			#print level
			mp = MapGen.BuildMapFromCommands([], level[0], level[1], None, None, None)
			#print 'map instance:', len(mp.grid), len(mp.grid[0])
			maps.append(mp)
		
		maps[-1] = lastLevel
		
		# determine top left coordinate of smaller map where it is in big map 
		offsets = []
		for level in levels:
			x = (lastWidth - level[0]) // 2
			y = (lastHeight - level[1]) // 2
			offsets.append((x, y))
		
		# blit big map onto smaller maps
		
		for i in range(len(levels) - 1):
			offset = offsets[i]
			xOffset = offset[0]
			yOffset = offset[1]
			level = maps[i]
			size = levels[i]
			width = size[0]
			height = size[1]
			#print i, width,height
			y = 0
			while y < height:
				x = 0
				while x < width:
					level.grid[x][y] = lastLevel.grid[x + xOffset][y + yOffset]
					x += 1
				y += 1
			
		
		addTheseSprites = []
		# blast out a bunch of sprites. PlayScene will automatically move sprites if they aren't standing in a valid place (like on a roof)
		for i in range(100):
			rx = int(random.random() * lastWidth - 4) + 2
			ry = int(random.random() * lastHeight - 4) + 2
			addTheseSprites.append((rx, ry))
		
		# sprites in previous level zone move to previous level
		
		for i in range(len(levels)):
			size = levels[i]
			offset = offsets[i]
			level = maps[i]
			
			newSpriteList = []
			for sprite in addTheseSprites:
				if sprite[0] < offset[0] or sprite[0] >= offset[0] + size[0] or sprite[1] < offset[1] or sprite[1] >= offset[1] + size[1]:
					newSpriteList.append(sprite)
				else:
					x = sprite[0] - offset[0]
					y = sprite[1] - offset[1]
					level.citizens.append((x, y, random.random() < .5, random.choice([1, 2, 3, 4]), x, y))
			addTheseSprites = newSpriteList
		
		# add a sprite to each border region of each level
		for level in maps:
			level.citizens.append((1, 1, True, 1, 1, 1))
		
		levels = levels[self.startZoom:]
		maps = maps[self.startZoom:]
		offsets = offsets[self.startZoom:]
		
		seeds = []
		for i in range(len(levels)):
			
			#print 'level',i,levels[i][0], levels[i][1], len(maps[i].grid), len(maps[i].grid[0])
			seeds.append(GamePlay.LevelSeed(None, {
												'map' : maps[i],
												'width' : levels[i][0],
												'height' : levels[i][1],
												'isCrowd' : isCrowd,
												'mode' : ('individual', 'crowd')[isCrowd],
												'progress' : True,
												'minutes' : -1
												}))
		
		_registeredSeeds = seeds
		first = _registeredSeeds[0]
		_registeredSeeds = _registeredSeeds[1:]
		
		return GamePlay.PlayScene(first)
