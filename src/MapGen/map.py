import MapGen
import os

def _trim(string):
	while len(string) > 0 and string[0] in ' \t\r\n':
		string = string[1:]
	while len(string) > 0 and string[-1] in ' \t\r\n':
		string = string[:-1]
	return string

def BuildMapFromCommands(commands, width, height, previousLevelSeed):
		
	items = []
	citizens = []
	police = []
	tileOverrides = []
	carryover = None
	for line in commands:
		parts = _trim(line).split(' ')
		if parts[0] == 'ROAD':
			item = MapGen.Road(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
			items.append(item)
		elif parts[0] == 'BUILDING':
			item = MapGen.Building(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]), int(parts[6]))
			items.append(item)
		elif parts[0] == 'CITIZEN':
			x = int(parts[1])
			y = int(parts[2])
			male = parts[3].upper() == 'M'
			variety = int(parts[4])
			citizens.append((x, y, male, variety))
		elif parts[0] == 'POLICE':
			x = int(parts[1])
			y = int(parts[2])
			variety = int(parts[3])
			police.append((x, y, variety))
		elif parts[0] == 'CARRYOVER':
			carryover = (int(parts[1]), int(parts[2]), previousLevelSeed)
		elif parts[0] == 'TILE':
			tileOverrides.append((parts[1], int(parts[2]), int(parts[3])))
	return Map(width, height, items, citizens, police, carryover, tileOverrides)

def BuildMap(level, width, height, previousLevelSeed):
	path = 'Levels' + os.sep + level + '.txt'
	c = open(path, 'rt')
	lines = c.read().split('\n')
	c.close()
	
	return BuildMapFromCommands(lines, width, height, previousLevelSeed)
	
class Map:
	
	def __init__(self, width, height, items, citizens, police, carryover, tileOverrides):
		self.InitializeGrid(width, height)
		self.roadSquares = []
		
		self.citizens = citizens
		self.police = police
		
		items = self.FillGridWithRoads(items)
		items = self.FillGridWithBuildings(items)
		
		self.FleshOutRoads(self.roadSquares)
		
		if carryover != None:
			self.FillInPreviousLevel(carryover[0], carryover[1], carryover[2].map.grid)
		
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
		
	def FleshOutRoads(self, roadSquares):
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

			col = 0
			while col < 7:
				row = 0
				while row < 7:
					grid[x + col - 3][y + row - 3] = impose[row][col]
					row += 1
				col += 1		  
			
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
			if item.IsBuilding:
				item.ApplySelfToGrid(self.grid)
			else:
				notbuildings.append(item)
		return notbuildings