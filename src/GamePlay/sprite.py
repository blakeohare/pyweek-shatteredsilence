from Resources import ImageLibrary

class Sprite:
	
	def __init__(self, x, y):
		self.X = x
		self.Y = y
		self.DX = 0
		self.DY = 0
		self.targetX = x
		self.targetY = y
		self.R = 16
		self.color = 0
		self.gV = 1.8
		self.cV = 4.2
		self.direction = 'down'
		self.colorizeable = False
		self.IsRadiating = False
		self.demotivation = 0
		self.beingShoved = False
		self.shoveCounter = 0
		self.waypoints = []
		self.waypointDelay = 0
		self.direction = 'down'
		self.isMoving = False
		self.renderCounter = 0
		self.IsPolice = False
	
	def IsCollision(self, anotherSprite):
		dx = (self.X - anotherSprite.X)
		dy = (self.Y - anotherSprite.Y)
		r = self.R - anotherSprite.R
		return dx * dx + dy * dy < r * r
	
	def IsInCultureRange(self, anotherSprite):
		dx = (self.X - anotherSprite.X)
		dy = (self.Y - anotherSprite.Y)
		return dx * dx + dy * dy < 64 * 64
	
	
	def GetImage(self):
		raise "You were supposed to override Sprite.GetImage"
	
	def RenderCoordinates(self, camX, camY):
		return (self.X - self.R - camX, self.Y - self.R - camY - 10)
	
	def SetTarget(self, x, y):
		self.targetX = x
		self.targetY = y
	
	def SetWaypoint(self, x, y):
		self.waypoints = [(self.X, self.Y), (x + 16, y + 16)]
	
	def Update(self):
		self.renderCounter += 1
		
		if len(self.waypoints) > 0:
			if self.color == 255:
				self.waypoints = []
			else:
				if self.X != self.waypoints[0][0] or self.Y != self.waypoints[0][1]:
					self.targetX = self.waypoints[0][0]
					self.targetY = self.waypoints[0][1]
					self.waypointDelay = 0
				elif self.waypointDelay > 20:
					self.waypoints = self.waypoints[::-1]
		self.waypointDelay += 1
		
		v = self.gV
		if self.color == 255: v = self.cV
		elif self.color != 0: v = 0
		
		if self.targetX != self.X or self.targetY != self.Y:
			dx = self.targetX - self.X
			dy = self.targetY - self.Y
			distance = (dx * dx + dy * dy) ** 0.5
			if distance < v:
				self.DX = self.targetX - self.X
				self.DY = self.targetY - self.Y
			else:
				self.DX = int(dx / distance * v)
				self.DY = int(dy / distance * v)
		
		if self.shoveCounter > 0:
			self.shoveCounter -= 1 
		
		dx = self.DX
		dy = self.DY
		if dx != 0 or dy != 0:
			self.isMoving = True
			if dx * dx > dy * dy:
				if dx > 0:
					self.direction = 'right'
				else:
					self.direction = 'left'
			else:
				if dy > 0:
					self.direction = 'down'
				else:
					self.direction = 'up'
		else:
			self.isMoving = False
	
	
class Citizen(Sprite):
	
	def __init__(self, x, y, male, variety):
		Sprite.__init__(self, x, y)
		self.colorizeable = True
		self.imagepath = ('Girl', 'Dude')[male] + str(variety)

	def Clone(self):
		sprite = Citizen(self.X, self.Y, True, 1)
		sprite.colorizeable = self.colorizeable
		sprite.imagepath = self.imagepath
		sprite.targetX = self.targetX
		sprite.targetY = self.targetY
		sprite.color = self.color
		sprite.IsRadiating = self.IsRadiating
		sprite.isMoving = self.isMoving
		sprite.waypoints = self.waypoints
		sprite.direction = self.direction
		sprite.demotiviation = self.demotivation
		sprite.waypointDelay = self.waypointDelay
		return sprite
		
	def GetImage(self):
		color = self.color - self.demotivation
		num = '0'
		if self.isMoving:
			num = ('1', '0', '2', '0')[(self.renderCounter // 3) & 3] 
		return ImageLibrary.Get('Sprites/' + self.imagepath + '/' + self.direction + num + '.png', color)

	def Decolorize(self):
		self.colorizeable = True
		self.color = 0
		self.demotivation = 0
		self.IsRadiating = False
		self.targetX = self.X
		self.targetY = self.Y
	
	def Colorize(self):
		self.color = 255
		self.IsRadiating = True
		self.waypoints = []
		self.targetX = self.X
		self.targetY = self.Y
	
class Police(Sprite):
	
	def __init__(self, x, y, variety):
		Sprite.__init__(self, x, y)
		self.target = None
		self.mode = 'walking' # modes are 'walking', 'pursuit', and 'smackdown'
		self.counter = 0
		self.smackCounter = 0
		self.IsPolice = True
	
	def Clone(self):
		sprite = Police(self.X, self.Y, 1)
		sprite.colorizeable = self.colorizeable
		sprite.targetX = self.targetX
		sprite.targetY = self.targetY
		sprite.color = self.color
		sprite.IsRadiating = self.IsRadiating
		sprite.isMoving = self.isMoving
		sprite.waypoints = self.waypoints
		sprite.direction = self.direction
		sprite.demotiviation = self.demotivation
		sprite.waypointDelay = self.waypointDelay
		return sprite
	def GetImage(self):
		if self.mode == 'walking':
			image = 'Sprites/Police/down0.png'
		elif self.mode == 'smackdown':
			if (self.counter / 15) % 2 == 0:
				image = 'Sprites/Police/down0.png'
			else:
				image = 'Sprites/Police/down0.png'
		else:
			image = 'Sprites/Police/down0.png'
		return ImageLibrary.Get(image, 0)
	
	def Update(self):
		if self.target != None:
			self.targetX = self.target.X
			self.targetY = self.target.Y
			dx = self.targetX - self.X
			dy = self.targetY - self.Y
			if dx * dx + dy * dy < (1.5 * 32) ** 2:
				if self.mode != 'smackdown':
					self.mode = 'smackdown'
					self.smackCounter = 0
			else:
				self.mode = 'pursuit'
			if self.target.color == 0:
				self.target = None
				self.targetX = self.X
				self.targetY = self.Y
		else:
			self.mode = 'walking'
			#TODO: patrol mode (most likely walk till you hit a wall and turn left, repeat
		
		if self.mode == 'smackdown':
			self.smackCounter += 1
			
			if self.target == None:
				self.mode = 'walking'
				self.smackCounter = 0
			elif self.target.demotivation >= 255:
				self.target.Decolorize()
				self.target = None
				self.mode = 'walking'
				self.smackCounter = 0
			else:
				self.smackCounter += 1
				if self.smackCounter > 30:
					self.target.demotivation += 100
					self.smackCounter = 0
			
		
		Sprite.Update(self)
		
	def TargetCitizen(self, citizen):
		self.target = citizen
		
		