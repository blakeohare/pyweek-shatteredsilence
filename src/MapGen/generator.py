import random

class Generator:
	
	# want to be able to do this in steps so that it 
	# can be done on a loading screen
	def __init__(self, width, height, isUrban):
		self.width = width
		self.height = height
		self.cellWidth = 8
		self.logGridWidth = self.width // (self.cellWidth + 7)
		self.logGridHeight = self.height // (self.cellWidth + 7)
		
		self.commands = []
		self.isUrban = isUrban
		self.tasks = [
					self.InitializeLogicalGrid,
					self.CompoundLogicalGrid,
					]
		self.commands.append('CITIZEN 5 5 M 1')
		self.commands.append('CITIZEN 15 15 M 1')
	
	
	def IsDone(self):
		return len(self.tasks) == 0
	
	def DoNextTask(self):
		if len(self.tasks) > 0:
			self.tasks[0]()
			self.tasks = self.tasks[1:]
	
	def CompoundLogicalGrid(self):
		grid = self.logicalGrid
		
		width = self.logGridWidth
		height = self.logGridHeight
		
		compounds = width * height // 2
		
		i = 0
		while i < compounds:
			
			x = random.randint(0, width - 1)
			y = random.randint(0, height - 1)
			direction = random.randint(0, 3)
			
			if not grid[x][y][direction]:
				grid[x][y][direction] = True
				if direction == 0 and x > 0:
					grid[x - 1][y][2] = True
				elif direction == 1 and y > 0:
					grid[x][y - 1][3] = True
				elif direction == 2 and x < width - 1:
					grid[x + 1][y][0] = True
				elif direction == 3 and y < height - 1:
					grid[x][y + 1][1] = True
		
			
			i += 1
		
		self.tasks.append(self.GenerateBlockList)
	
	def GenerateBlockList(self):
		# TODO: this
		self.tasks.append(self.PopulateBlocks)
	
	def PopulateBlocks(self):
		# TODO: this
		self.tasks.append(self.SerializeStreets)
	
	def SerializeStreets(self):
		cellWidth = self.cellWidth
		longWidth = cellWidth + 7
		logGridWidth = self.logGridWidth
		logGridHeight = self.logGridHeight
		logicalGrid = self.logicalGrid
		
		commands = []
		
		y = 1
		while y < logGridHeight:
			
			x = 1
			
			while x < logGridWidth:
				tile = logicalGrid[x][y]
				
				col = (x - 1) * longWidth + 8
				row = (y - 1) * longWidth + 8
				
				#vertical road needed (not connected to tile to left)
				if not tile[0]:
					commands.append('ROAD %d %d %d %d' % (col, row, col, row + longWidth))
					
				#horizontal road needed (not connected to tile above)
				if not tile[1]:
					commands.append('ROAD %d %d %d %d' % (col, row, col + longWidth, row))
				
				x += 1
			y += 1
		self.commands += commands
	
	def SerializeBlocks(self):
		# TODO: this
		pass
	
	def InitializeLogicalGrid(self):
		logGridWidth = self.logGridWidth
		logGridHeight = self.logGridHeight
		
		cols = []
		x = 0
		while x < logGridWidth:
			col = []
			y = 0
			while y < logGridHeight:
				
				# Connections...
				# 0 Left
				# 1 Top
				# 2 Right
				# 3 Bottom
				
				# 4 IsOccupied
				col.append([False, False, False, False, False])
				
				y += 1
			cols.append(col)
			x += 1
		
		self.logicalGrid = cols