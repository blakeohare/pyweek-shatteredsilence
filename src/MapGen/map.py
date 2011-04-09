import MapGen
import os

def _trim(string):
	while len(string) > 0 and string[0] in ' \t\r\n':
		string = string[1:]
	while len(string) > 0 and string[-1] in ' \t\r\n':
		string = string[:-1]
	return string

def BuildMapFromCommands(commands, mapwidth, mapheight, previousLevelSeed, previousLevel):
	items = []
	citizens = []
	police = []
	tileOverrides = []
	carryover = None
	isCrowdLevel = False
	for line in commands:
		parts = _trim(line).split(' ')
		if parts[0] == 'ROAD':
			item = MapGen.Road(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
			items.append(item)
		elif parts[0] == 'CROAD':
			isCrowdLevel = True
			item = MapGen.CRoad(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
			items.append(item)
		elif parts[0] == 'BUILDING':
			item = MapGen.Building(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]), int(parts[6]))
			items.append(item)
		elif parts[0] == 'CITIZEN':
			
			x = int(parts[1])
			y = int(parts[2])
			
			male = parts[3].upper() == 'M'
			variety = int(parts[4])
			if len(parts) > 5:
				tx = int(parts[5])
				ty = int(parts[6])
			else:
				tx = x
				ty = y
			citizens.append((x, y, male, variety, tx, ty))
			
		elif parts[0] == 'POLICE':
			x = int(parts[1])
			y = int(parts[2])
			variety = int(parts[3])
			police.append((x, y, variety))
		elif parts[0] == 'BUSH':
			x = int(parts[1])
			y = int(parts[2])
			widthIhatePython = int(parts[3])
			items.append(MapGen.Bush(x, y, widthIhatePython))
		elif parts[0] == 'TREE':
			x = int(parts[1])
			y = int(parts[2])
			type = parts[3].lower()
			items.append(MapGen.Tree(x, y, type))
		elif parts[0] == 'CARRYOVER':
			colorize_center = len(parts) >= 4 and parts[3] == 'COLOR'
			carryover = (int(parts[1]), int(parts[2]), previousLevelSeed, colorize_center)
		elif parts[0] == 'TILE':
			tileOverrides.append((parts[1], int(parts[2]), int(parts[3])))
		elif parts[0] == 'HOUSE':
			x = int(parts[1])
			y = int(parts[2])
			items.append(MapGen.House(x, y, int(parts[3])))
		elif parts[0] == 'RECT':
			type = parts[1]
			left = int(parts[2])
			top = int(parts[3])
			width = int(parts[4])
			height = int(parts[5])
			x = left
			endX = left + width - 1
			endY = top + height - 1
			
			while x <= endX:
				y = top
				while y <= endY:
					tileOverrides.append((parts[1], x, y))
					y += 1
				x += 1
				
	return Map(mapwidth, mapheight, items, citizens, police, carryover, tileOverrides, previousLevel, isCrowdLevel)

def BuildMap(level, width, height, previousLevelSeed, previousLevel):
	path = 'Levels' + os.sep + level + '.txt'
	c = open(path, 'rt')
	lines = c.read().split('\n')
	c.close()
	
	return BuildMapFromCommands(lines, width, height, previousLevelSeed, previousLevel)
	
class Map:
	
	def __init__(self, width, height, items, citizens, police, carryover, tileOverrides, previousLevel, isCrowdLevel):
		self.InitializeGrid(width, height)
		self.roadSquares = []
		self.isCrowdLevel = isCrowdLevel
		self.colorize_these = []
		
		self.citizens = citizens
		self.police = police
		
		items = self.FillGridWithRoads(items)
		items = self.FillGridWithBuildings(items)
		self.previousLevel = previousLevel
		self.FleshOutRoads(self.roadSquares)
		self.carryoversprites = None
		
		if carryover != None:
			x = carryover[0]
			y = carryover[1]
			self.carryoversprites = (x, y)
			prev_grid = carryover[2].map.grid
			self.FillInPreviousLevel(x, y, prev_grid)
			if carryover[3]:
				self.colorize_these.append((x, y, len(prev_grid), len(prev_grid[0])))
		
		self.ApplyTileOverrides(tileOverrides)
	
	def ApplyTileOverrides(self, overrides):
		
		for override in overrides:
			
			self.grid[override[1]][override[2]] = override[0]
		
	def FillInPreviousLevel(self, left, top, grid):
		
		width = len(grid)
		height = len(grid[0])
		
		x = left
		right = left + width - 1
		bottom = top + height - 1
		while x <= right:
			y = top
			while y <= bottom:
				self.grid[x][y] = grid[x - left][y - top]
				y += 1
			x += 1 
		
		
	def FleshOutBigRoads(self, roadSquares):
		intersections = []
		sidewalk = []
		grid = self.grid
		width = len(grid)
		height = len(grid[0])
		for road in roadSquares:
			x = road[0]
			y = road[1]
			type = grid[x][y]
			if type == 'intersection':
				intersections.append((x, y))
			elif type == 'yellow_line_horizontal':
				if y > 3:
					grid[x][y - 1] = 'asphault'
					grid[x][y - 2] = 'asphault'
					sidewalk.append((x, y - 3))
				if y < height - 3:
					grid[x][y + 1] = 'asphault'
					grid[x][y + 2] = 'asphault'
					sidewalk.append((x, y + 3))
			elif type == 'yellow_line_vertical':
				if x > 3:
					grid[x - 1][y] = 'asphault'
					grid[x - 2][y] = 'asphault'
					sidewalk.append((x - 3, y))
				if x < width - 3:
					grid[x + 1][y] = 'asphault'
					grid[x + 2][y] = 'asphault'
					sidewalk.append((x + 3, y))
		
		for sidewalkunit in sidewalk:
			x = sidewalkunit[0]
			y = sidewalkunit[1]
			grid[x][y] = 'sidewalk'
		
		for intersection in intersections:
			x = intersection[0]
			y = intersection[1]
			
			impose = [
			  ['sidewalk_corner4', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'sidewalk_corner3'],
			  ['vertical_crosswalk', 'asphault', 'asphault', 'asphault', 'asphault', 'asphault', 'vertical_crosswalk'],
			  ['vertical_crosswalk', 'asphault', 'asphault', 'asphault', 'asphault', 'asphault', 'vertical_crosswalk'],
			  ['vertical_crosswalk', 'asphault', 'asphault', 'asphault', 'asphault', 'asphault', 'vertical_crosswalk'],
			  ['vertical_crosswalk', 'asphault', 'asphault', 'asphault', 'asphault', 'asphault', 'vertical_crosswalk'],
			  ['vertical_crosswalk', 'asphault', 'asphault', 'asphault', 'asphault', 'asphault', 'vertical_crosswalk'],
			  ['sidewalk_corner2', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'sidewalk_corner1']]
			
			if grid[x - 4][y] != 'yellow_line_horizontal':
				i = 0
				while i <= 6:
					impose[i][0] = 'sidewalk'
					i += 1
			if grid[x + 4][y] != 'yellow_line_horizontal':
				i = 0
				while i <= 6:
					impose[i][6] = 'sidewalk'
					i += 1
			if grid[x][y - 4] != 'yellow_line_vertical':
				i = 0
				while i <= 6:
					impose[0][i] = 'sidewalk'
					i += 1
			if grid[x][y + 4] != 'yellow_line_vertical':
				i = 0
				while i <= 6:
					impose[6][i] = 'sidewalk'
					i += 1
			
			col = 0
			while col < 7:
				row = 0
				while row < 7:
					grid[x + col - 3][y + row - 3] = impose[row][col]
					row += 1
				col += 1		  
		
	def FleshOutRoads(self, roadSquares):
		if self.isCrowdLevel:
			self.FleshOutSmallRoads(roadSquares)
		else:
			self.FleshOutBigRoads(roadSquares)
	
	
	
	def FleshOutSmallRoads(self, roadSquares):
		width = len(self.grid)
		height = len(self.grid[0])
		
		lookup = {
				'0000' : '4',
				'0001' : 'v',
				'0010' : 'h',
				'0011' : 'br',
				'0100' : 'v',
				'0101' : 'v',
				'0110' : 'tr',
				'0111' : 't4',
				'1000' : 'h',
				'1001' : 'bl',
				'1010' : 'h',
				'1011' : 't1',
				'1100' : 'tl',
				'1101' : 't2',
				'1110' : 't3',
				'1111' : '4'
				}
		
		for road in roadSquares:
			x = road[0]
			y = road[1]
			left = False
			right = False
			top = False
			bottom = False
			
			if x > 0:
				t = self.grid[x - 1][y]
				if t != None:
					left = t[:5] == 'croad'
			if x < width - 1:
				t = self.grid[x + 1][y]
				if t != None:
					right = t[:5] == 'croad'
			if y > 0:
				t = self.grid[x][y - 1]
				if t != None:
					top = t[:5] == 'croad'
			if y < height - 1:
				t = self.grid[x][y + 1]
				if t != None:
					bottom = t[:5] == 'croad'
			
			key = ('0','1')[left] + ('0','1')[top] + ('0','1')[right] + ('0','1')[bottom]
			self.grid[x][y] = 'croad_street-' + lookup[key]
	
	def InitializeGrid(self, width, height):
		self.grid = []
		x = 0
		while x < width:
			col = []
			y = 0
			while y < height:
				col.append(None)
				y += 1 
			x += 1
			self.grid.append(col)
	
	def FillGridWithRoads(self, items):
		notroads = []
		for item in items:
			if item.IsRoad:
				self.roadSquares += item.ApplySelfToGrid(self.grid)
			else:
				notroads.append(item)
		return notroads

	def FillGridWithBuildings(self, items):
		notbuildings = []
		for item in items:
			if item.Applyable:
				item.ApplySelfToGrid(self.grid)
			else:
				notbuildings.append(item)
				
		return notbuildings