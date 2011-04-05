import MapGen

class LevelSeed:
	def __init__(self, special=None, args=None):
		self.width = 64
		self.height = 64
		self.mode = 'individual'
		self.map = None
		self.specialName = None
		if special != None:
			if special == 'next':
				self.InitializeNextLevel(args)
			else:
				self.InitializeSpecialLevel(special, args)
		else:
			self.width = args['width']
			self.height = args['height']
			self.mode = args['mode']
			self.progress = args['progress']
			self.timedMode = args['minutes'] > -1
			self.minutes = args['minutes']
			
			if self.mode == 'individual':
				self.citizens = args['citizens']
				self.police = args['police']
			else:
				self.citizens = 0
				self.police = 0
			
			if self.mode == 'region':
				self.city_centers = args['city_centers']
			else:
				self.city_centers = 0
	
	def InitializeNextLevel(self, previousLevelSeed):
		specialName = previousLevelSeed.specialName
		if specialName == None:
			self.InitializeNextCustomLevel(previousLevelSeed)
		elif specialName == 'level1':
			self.InitializeSpecialLevel('level2', previousLevelSeed)
		elif specialName == 'level2':
			self.InitializeSpecialLevel('level3', previousLevelSeed)
		elif specialName == 'level3':
			self.InitializeSpecialLevel('level4', previousLevelSeed)
		elif specialName == 'level4':
			self.InitializeSpecialLevel('level5', previousLevelSeed)
		elif specialName == 'level5':
			self.InitializeSpecialLevel('level6', previousLevelSeed)
		elif specialName == 'level6':
			self.InitializeSpecialLevel('level7', previousLevelSeed)
		elif specialName == 'level7':
			self.InitializeSpecialLevel('level8', previousLevelSeed)
		elif specialName == 'level8':
			self.InitializeSpecialLevel('level9', previousLevelSeed)
		elif specialName == 'level9':
			# TODO: something else
			raise "You won!"
		elif specialName == 'testlevel':
			self.InitializeSpecialLevel('level1', previousLevelSeed)
			# meh
			
	def InitializeSpecialLevel(self, special, previousLevelSeed):
		self.progress = True
		self.timedMode = False
		self.citizens = 0
		self.police = 0
		self.specialName = special
		
		if special == 'testlevel':
			self.progress = False
			self.width = 32
			self.height = 24
		elif special == 'level1':
			self.width = 20
			self.height = 15
		elif special == 'level2':
			self.width = 32
			self.height = 24
		elif special == 'level3':
			self.width = 64
			self.height = 48
		elif special == 'level4':
			self.width = 180
			self.height = 100
		elif special == 'level5':
			self.mode = 'crowd'
			self.width = 40
			self.height = 32
		elif special == 'level6':
			self.mode = 'crowd'
			self.width = 96
			self.height = 64
		elif special == 'level7':
			self.mode = 'crowd'
			self.width = 180
			self.height = 100
		elif special == 'level8':
			self.mode = 'region'
			self.width = 40
			self.height = 32
		elif special == 'level9':
			self.mode = 'region'
			self.width = 96
			self.height = 64
		self.map = MapGen.BuildMap(special, self.width, self.height, previousLevelSeed)
	