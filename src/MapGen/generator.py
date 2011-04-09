import random

class Generator:
	
	def __init__(self, width, height, isUrban, isCrowd):
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
	
	def RandomBlocks(self, num):
		output = []
		width = self.logGridWidth
		height = self.logGridHeight
		while num > 0:
			x = random.randint(0, width - 1)
			y = random.randint(0, height - 1)
			output.append((x, y))
			num -= 1
		return output 
	
	def CompoundLogicalGrid(self):
		grid = self.logicalGrid
		
		width = self.logGridWidth
		height = self.logGridHeight
		
		compounds = self.RandomBlocks(width * height // 2)
		
		for compound in compounds:
			
			x = compound[0]
			y = compound[1]
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
		
		self.tasks.append(self.PopulateBlocks)
		
	
	def PopulateBlocks(self):
		commands = []
		grid = self.logicalGrid
		longWidth = self.cellWidth + 7
		logGridWidth = self.logGridWidth
		logGridHeight = self.logGridHeight
		for block in self.RandomBlocks(self.logGridHeight * self.logGridWidth // 2):
			x = block[0]
			y = block[1]
			cell = grid[x][y]
			if not cell[4]:
				left = (x - 1) * longWidth + 12
				top = (y - 1) * longWidth + 12
				width = longWidth - 7
				height = longWidth - 7
				roofHeight = 3
				cell[4] = True
				if not (cell[0] or cell[1] or cell[2] or cell[3]):
					pass
				else:
					if cell[0] and x > 0 and not grid[x - 1][y][4]:
						left -= longWidth
						width += longWidth
						grid[x - 1][y][4] = True
					elif cell[1] and y > 0 and not grid[x][y - 1][4]:
						top -= longWidth
						height += longWidth
						grid[x][y - 1][4] = True
						roofHeight += longWidth
					elif cell[2] and x < logGridWidth - 1 and not grid[x + 1][y][4]:
						width += longWidth
						grid[x + 1][y][4] = True
					elif cell[3] and y < logGridHeight - 1 and not grid[x][y + 1][4]:
						height += longWidth
						grid[x][y + 1][4] = True
						roofHeight += longWidth
					if random.random() < .5:
						roofHeight += 2
				commands.append('BUILDING %d %d %d %d %d 1' % (left, top, width, height, roofHeight))
				
		self.commands += commands
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