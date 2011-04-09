import GamePlay

class Level:
	
	def __init__(self, levelseed):
		self.width = levelseed.width
		self.height = levelseed.height
		
		self.pixelWidth = self.width * 32
		self.pixelHeight = self.height * 32
		self.InitializeTiles(self.width, self.height, levelseed.map)
		self.sprites = []
		self.police = []
		self.counter = 0
		self.randomDirections = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		self.citizens = []
		
		for citizen in levelseed.map.citizens:
			x = citizen[0]
			y = citizen[1]
			tx = citizen[4]
			ty = citizen[5]
			sprite = GamePlay.Citizen(32 * citizen[0] + 16, 32 * citizen[1] + 16, citizen[2], citizen[3])
			if levelseed.map.isCrowdLevel:
				sprite.Crowdify()
			if x != tx or y != ty:
				sprite.SetWaypoint(tx * 32, ty * 32)
			self.sprites.append(sprite)
			self.citizens.append(sprite)
		
		#self.citizens[0].color = 255
		
		for police in levelseed.map.police:
			sprite = GamePlay.Police(32 * police[0] + 16, 32 * police[1] + 16, police[2])
			self.sprites.append(sprite)
			self.police.append(sprite)
			if levelseed.map.isCrowdLevel:
				sprite.Crowdify()
		
		self.spriteGraph = SpriteGraph(self.width, self.height)
		
		self.PreColorize(levelseed.map.colorize_these)
		self.initCameraOffset = None
		if levelseed.map.carryoversprites != None:
			x = levelseed.map.carryoversprites[0]
			y = levelseed.map.carryoversprites[1]
			
			self.initCameraOffset = (x, y)
			self.CarryOverSprites(x, y, levelseed.map.previousLevel)
		levelseed.map.previousLevel = None
	
	def CarryOverSprites(self, xTileOffset, yTileOffset, previousLevel):
		if previousLevel == None: return
		for sprite in previousLevel.sprites:
			sprite = sprite.Clone()
			sprite.X += xTileOffset * 32
			sprite.Y += yTileOffset * 32
			sprite.targetX += xTileOffset * 32
			sprite.targetY += yTileOffset * 32
			waypoints = []
			for waypoint in sprite.waypoints:
				waypoints.append((waypoint[0] + xTileOffset * 32, waypoint[1] + yTileOffset * 32))
			sprite.waypoints = waypoints 
			if sprite.IsPolice:
				self.police.append(sprite)
			else:
				self.citizens.append(sprite)
			self.sprites.append(sprite)
	def PreColorize(self, rectangles):
		for rectangle in rectangles:
			xStart = rectangle[0]
			xEnd = xStart + rectangle[2] - 1
			yStart = rectangle[1]
			yEnd = yStart + rectangle[3] - 1
			y = yStart
			while y <= yEnd:
				x = xStart
				while x <= xEnd:
					self.tiles[x][y].SetMinColorIntensity(255)
					x += 1
				y += 1 
			# TODO: 50% intensity on the border?
		
	def InitializeTiles(self, columns, rows, map_data):
		tiles = []
		x = 0
		while x < columns:
			y = 0
			column = []
			while y < rows:
				column.append(GamePlay.MakeTile(map_data.grid[x][y], x, y))
				y += 1
			tiles.append(column)
			x += 1
		
		self.tiles = tiles
	
	def GetProgress(self):
		total = len(self.citizens)
		converted = 0
		for citizen in self.citizens:
			if citizen.color == 255:
				converted += 1
		
		if total == 0: total = 1
		return 100.0 * converted / total
	
	def UpdateTileColors(self):
		counter = self.counter
		width = len(self.tiles)
		height = len(self.tiles[0])
		for sprite in self.sprites:
			if sprite.color == 255:
				x = sprite.X // 32
				y = sprite.Y // 32
				self.tiles[x][y].SetColorization(counter)
				if x > 0:
					self.tiles[x - 1][y].SetColorization(counter)
					if y > 0:
						self.tiles[x - 1][y - 1].SetColorization(counter - 40)
					if y < height - 1:
						self.tiles[x - 1][y + 1].SetColorization(counter - 40)
						
				if y > 0:
					self.tiles[x][y - 1].SetColorization(counter)
				if x < width - 1:
					self.tiles[x + 1][y].SetColorization(counter)
					if y > 0:
						self.tiles[x + 1][y - 1].SetColorization(counter - 40)
					if y < height - 1:
						self.tiles[x + 1][y + 1].SetColorization(counter - 40)
				if y < height - 1:
					self.tiles[x][y + 1].SetColorization(counter)
				
				
		
		self.counter += 1
	
	def Update(self):
		self.UpdateSprites()
		self.UpdatePolice()
	
	def UpdatePolice(self):
		fugitives = self.radiatingSprites
		
		# TODO: AAAAAAAAAAH!!!! NESTED LOOP! KILL IT! KILLLLL ITTT!!!!
		officer_sight_range = 7 # (blocks)
		officer_sight_range = (officer_sight_range * 32) ** 2
		
		for officer in self.police:
			officer.counter += 1
			if officer.target == None:
				closest = None
				closestDistance = 9999999
				
				for evildoer in fugitives:
					dx = evildoer.X - officer.X
					dy = evildoer.Y - officer.Y
					distance = dx * dx + dy * dy
					if distance < closestDistance:
						closestDistance = distance
						closest = evildoer
				
				if closestDistance < officer_sight_range:
					officer.TargetCitizen(closest)
		
	def RandomDirection(self):
		self.randomDirections = [self.randomDirections[-1]] + self.randomDirections[:-1]
		return self.randomDirections[0]
	
	def UpdateSprites(self):
		
		graph = self.spriteGraph
		graph.ClearAll()
		
		for sprite in self.sprites:
			sprite.IsRadiating = False
			graph.AddSprite(sprite)
		
		for sprite in self.sprites:
			sprite.Update()
			
			x = sprite.X
			y = sprite.Y
			dx = sprite.DX
			dy = sprite.DY
			
			# do collision dispersion
			tooClose = graph.GetClosestNeighboringSprite(sprite)
			if tooClose != None and not sprite.isMoving:
				if sprite.X < tooClose.X:
					dx = -1
				else:
					dx = 1
				if sprite.Y < tooClose.Y:
					dy = -1
				else:
					dy = 1
				sprite.targetX = sprite.X + dx * (sprite.R + 1) * 1 // 3
				sprite.targetY = sprite.Y + dy * (sprite.R + 1) * 1 // 3
				tooClose.targetX = tooClose.X - dx * (sprite.R + 1) * 1 // 3
				tooClose.targetY = tooClose.Y - dy * (sprite.R + 1) * 1 // 3
			
			# do location updates
			
			if dx != 0 or dy != 0:
				newx = x + dx
				newy = y + dy
				
				if newx < 0: newx = 0
				if newx >= self.width * 32: newx = self.width * 32 - 1
				if newy < 0: newy = 0
				if newy >= self.height * 32: newy = self.height * 32 - 1 
				
				tile = self.tiles[newx // 32][newy // 32]
				
				
				if tile.IsPassable:
					x = newx
					y = newy
					sprite.X = x
					sprite.Y = y
				else:
					sprite.targetX = sprite.X
					sprite.targetY = sprite.Y
				sprite.DX = 0
				sprite.DY = 0
			
			# do color updates
			if sprite.color < 255: sprite.color -= 2
			if sprite.color < 0: sprite.color = 0
			
			wasColorized = sprite.color == 255
			
			if sprite.color != 255 and sprite.colorizeable:
				if graph.IsRadiantSpriteNear(x, y, 32 * 2):
					sprite.color += 4
			if sprite.color >= 255 and not wasColorized:
				sprite.Colorize()
			
		radiatingSprites = []
		for sprite in self.sprites:
			if sprite.IsRadiating:
				radiatingSprites.append(sprite)
		self.radiatingSprites = radiatingSprites
		
	
	def GetSpritesInRange(self, left, top, right, bottom):
		sprites = []
		for sprite in self.sprites:
			if sprite.X >= left and sprite.X <= right and sprite.Y >= top and sprite.Y <= bottom:
				sprites.append(sprite)
		return sprites 
	
	# arguments are level coordinates already normalized with the camera viewport into consideration
	def GetSpriteHitTest(self, pixelX, pixelY):
		winnerDistance = 9999999
		winner = None
		for sprite in self.sprites:
			dx = sprite.X - pixelX
			dy = sprite.Y - pixelY
			d = dx * dx + dy * dy
			r = sprite.R + 5
			if d < winnerDistance and d < r * r:
				winner = sprite
				winnerDistance = d
		return winner
	
	def RenderSprites(self, screen, cameraX, cameraY):
		left = cameraX - 64
		right = cameraX + 640 + 64
		top = cameraY - 64
		bottom = cameraY + 480 + 64
		
		for sprite in self.sprites:
			if sprite.X < left or sprite.X > right or sprite.Y < top or sprite.Y > bottom:
				continue
			image = sprite.GetImage()
			
			screen.blit(image, sprite.RenderCoordinates(cameraX, cameraY))
	
	def RenderTiles(self, screen, cameraX, cameraY):
		
		self.UpdateTileColors()
		
		startX = cameraX // 32
		startY = cameraY // 32
		endX = startX + (640 // 32) + 1
		endY = startY + (480 // 32) + 1
		
		if startX < 0: startX = 0
		if startY < 0: startY = 0
		if endX >= self.width: endX = self.width
		if endY >= self.height: endY = self.height
		
		tiles = self.tiles
		
		counter = self.counter
		
		x = startX
		while x < endX:
			y = startY
			while y < endY:
				tile = tiles[x][y]
				drawX = tile.PixelX - cameraX
				drawY = tile.PixelY - cameraY
				screen.blit(tile.GetImage(counter, tiles), (drawX, drawY))
				y += 1
			x += 1 

class SpriteGraph:
	
	def __init__(self, map_columns, map_rows):
		self.cols = []
		self.buckets = []
		self.populatedBuckets = {}
		bucketRange = 3
		self.bucketRange = bucketRange
		x = 0
		while x < map_columns:
			y = 0
			col = []
			self.cols.append(col)
			while y < map_rows:
				if x % bucketRange == 0 and y % bucketRange == 0:
					bucket = SpriteBucket(str(x) + '-' + str(y))
					self.buckets.append(bucket)
					col.append(bucket)
				else:
					col.append(self.cols[(x // bucketRange) * bucketRange][(y // bucketRange) * bucketRange])
				y += 1
			x += 1
		self.width = len(self.cols)
		self.height = len(self.cols[0])
		self.EstablishNeighbors(bucketRange)
	
	def EstablishNeighbors(self, bucketRange):
		
		width = len(self.cols)
		height = len(self.cols[0])
		
		x = 0
		while x < width:
			y = 0
			while y < height:
				bucket = self.cols[x][y]
				
				for neighbor in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
					nx = x + neighbor[0] * bucketRange
					ny = y + neighbor[1] * bucketRange
					if nx >= 0 and nx < width and ny >= 0 and ny < height:
						bucket.AddNeighbor(self.cols[nx][ny])
				
				y += bucketRange
			x += bucketRange
	
	def GetClosestNeighboringSprite(self, sprite):
		sprites = self.GetSpritesNear(sprite.X, sprite.Y, sprite.R * 2, False)
		winnerDistance = 9999
		winner = None
		for neighbor in sprites:
			if neighbor != sprite:
				dx = sprite.X - neighbor.X
				dy = sprite.Y - neighbor.Y
				r2 = dx * dx + dy * dy
				if r2 < winnerDistance:
					winner = neighbor
					winnerDistance = r2
		return winner
	
	def ClearAll(self):
		for bucket in self.populatedBuckets.values():
			bucket.ClearSprites()
	
	def AddSprite(self, sprite):
		x = sprite.X // 32
		y = sprite.Y // 32
		bucket = self.cols[x][y]
		bucket.AddSprite(sprite)
		self.populatedBuckets[bucket.key] = bucket
		
	def GetSpritesNear(self, x, y, radius, radiates):
		bucket = self.cols[x // 32][y // 32]
		
		if radiates and not bucket.radiates:
			sprites = []
		else:
			sprites = bucket.GetSpritesNear(x, y, radius, radiates)
		for neighbor in bucket.neighbors:
			if not radiates or neighbor.radiates:
				sprites += neighbor.GetSpritesNear(x, y, radius, radiates)
		return sprites
	
	def IsRadiantSpriteNear(self, x, y, radius):
		bucket = self.cols[x // 32][y // 32]
		if bucket.radiates:
			if bucket.IsRadiantSpriteNear(x, y, radius):
				return True
		
		for neighbor in bucket.neighbors:
			if neighbor.radiates and neighbor.IsRadiantSpriteNear(x, y, radius):
				return True
		
		return False

class SpriteBucket:
	
	def __init__(self, key):
		self.sprites = []
		self.neighbors = []
		self.key = key
		self.radiates = False
		
	def AddSprite(self, sprite):
		if sprite.color == 255: self.radiates = True
		self.sprites.append(sprite)
	
	def ClearSprites(self):
		self.sprites = []
		self.radiates = False
	
	def GetSpritesNear(self, x, y, radius, radiates):
		output = []
		if radiates and not self.radiates: return output
		for sprite in self.sprites:
			dx = sprite.X - x
			dy = sprite.Y - y
			if dx * dx + dy * dy < radius * radius:
				output.append(sprite)
		return output
	
	def IsRadiantSpriteNear(self, x, y, radius):
		if self.radiates:
			for sprite in self.sprites:
				if sprite.color == 255:
					dx = sprite.X - x
					dy = sprite.Y - y
					if dx * dx + dy * dy < radius * radius:
						sprite.IsRadiating = True
						return True
		return False
				
		
	
	def AddNeighbor(self, neighbor):
		self.neighbors.append(neighbor)
		

