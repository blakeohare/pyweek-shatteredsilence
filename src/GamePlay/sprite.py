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
		self.V = 4.2
		self.direction = 'down'
		self.colorizeable = False
		self.IsRadiating = False
		self.demotivation = 0
		self.beingShoved = False
		self.shoveCounter = 0
	
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
		return (self.X - self.R - camX, self.Y - self.R - camY)
	
	def SetTarget(self, x, y):
		self.targetX = x
		self.targetY = y
	
	def Update(self):
		if self.targetX != self.X or self.targetY != self.Y:
			dx = self.targetX - self.X
			dy = self.targetY - self.Y
			distance = (dx * dx + dy * dy) ** 0.5
			if distance < self.V:
				self.DX = self.targetX - self.X
				self.DY = self.targetY - self.Y
			else:
				self.DX = int(dx / distance * self.V)
				self.DY = int(dy / distance * self.V)
		
		if self.shoveCounter > 0:
			self.shoveCounter -= 1 
	
class Citizen(Sprite):
	
	def __init__(self, x, y, male, variety):
		Sprite.__init__(self, x, y)
		self.colorizeable = True
		self.imagepath = ('Girl', 'Dude')[male] + str(variety)

	
	def GetImage(self):
		color = self.color - self.demotivation
		return ImageLibrary.Get('Sprites/' + self.imagepath + '/down0.png', color)

	def Decolorize(self):
		self.colorizeable = True
		self.color = 0
		self.demotivation = 0
		self.IsRadiating = False
		self.targetX = self.X
		self.targetY = self.Y
	
class Police(Sprite):
	
	def __init__(self, x, y, variety):
		Sprite.__init__(self, x, y)
		self.target = None
		self.mode = 'walking' # modes are 'walking', 'pursuit', and 'smackdown'
		self.counter = 0
		self.smackCounter = 0
	
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
		
		