class MapItem:
	
	def __init__(self):
		self.IsRoad = False
		self.IsBuilding = False
		self.IsHouse = False
		self.Applyable = False
		
class House(MapItem):
	def __init__(self, x, y, variety):
		MapItem.__init__(self)
		self.IsHouse = True
		self.Applyable = True
		self.x = x
		self.y = y
		self.prefix = ''
		if variety == 2: self.prefix = 'b'
		elif variety == 3: self.prefix = 'p'
	
	def ApplySelfToGrid(self, grid):
		left = self.x
		top = self.y
		width = 5
		height = 7
		y = 0
		i = 0
		while y < height:
			x = 0
			while x < width:
				#print x + left, y + top, len(grid), len(grid[0])
				grid[x + left][y + top] = self.prefix + 'house' + str(i)
				i += 1
				x += 1
			y += 1

class Bush(MapItem):
	def __init__(self, x, y, width):
		MapItem.__init__(self)
		self.x = x
		self.y = y
		self.width = width
		self.Applyable = True
	
	def ApplySelfToGrid(self, grid):
		x = self.x
		y = self.y
		grid[x][y] = 'bush_left'
		grid[x + self.width - 1][y] = 'bush_right'
		xEnd = x + self.width - 1
		x += 1
		while x < xEnd:
			grid[x][y] = 'bush_center'
			x += 1

class Building(MapItem):
	
	def __init__(self, left, top, width, height, roofheight, variety):
		MapItem.__init__(self)
		self.IsBuilding = True
		self.Applyable = True
		self.top = top
		self.left = left
		self.width = width
		self.height = height
		self.roofHeight = roofheight
		self.folder = ''
		if variety == 1:
			self.folder = 'building/'
	
	def ApplySelfToGrid(self, grid):
		left = self.left
		top = self.top
		right = self.left + self.width - 1
		bottom = self.top + self.height - 1
		
		grid[left][top] = self.folder + 'roof1'
		grid[right][top] = self.folder + 'roof3'
		x = left + 1
		while x < right:
			grid[x][top] = self.folder + 'roof2'
			x += 1
		y = top + 1
		while y < top + self.roofHeight - 1:
			grid[left][y] = self.folder + 'roof4'
			grid[right][y] = self.folder + 'roof6'
			x = left + 1
			while x < right:
				# TODO: roof doodad?
				grid[x][y] = self.folder + 'roof5'
				x += 1
			y += 1
		grid[left][y] = self.folder + 'roof7'
		grid[right][y] = self.folder + 'roof9'
		x = left + 1
		while x < right:
			grid[x][y] = self.folder + 'roof8'
			x += 1
			
		y += 1
		while y < bottom:
			grid[left][y] = self.folder + 'building1'
			grid[right][y] = self.folder + 'building3'
			x = left + 1
			while x < right:
				grid[x][y] = self.folder + 'building2'
				x += 1
			y += 1
		grid[left][y] = self.folder + 'building4'
		grid[right][y] = self.folder + 'building6'
		x = left + 1
		while x < right:
			grid[x][y] = self.folder + 'building5'
			x += 1
	

class Road(MapItem):
	
	def __init__(self, startX, startY, endX, endY):
		MapItem.__init__(self)
		self.IsRoad = True
		self.startX = startX
		self.startY = startY
		self.endX = endX
		self.endY = endY
	
	def ApplySelfToGrid(self, grid):
		road_squares = []
		if self.startY == self.endY:
			left = self.startX
			right = self.endX
			if left > right:
				t = left
				left = right
				right = t
			x = left
			y = self.startY
			while x <= right:
				if grid[x][y] != 'intersection':
					if grid[x][y] == 'yellow_line_vertical':
						grid[x][y] = 'intersection'
					else:
						grid[x][y] = 'yellow_line_horizontal'
					road_squares.append((x, y))
				x += 1
		else:
			top = self.startY
			bottom = self.endY
			if bottom < top:
				t = bottom
				bottom = top
				top = t
			x = self.startX
			y = top
			while y <= bottom:
				if grid[x][y] != 'intersection':
					if grid[x][y] == 'yellow_line_horizontal':
						grid[x][y] = 'intersection'
					else:
						grid[x][y] = 'yellow_line_vertical'
					road_squares.append((x, y))
				y += 1
		return road_squares
