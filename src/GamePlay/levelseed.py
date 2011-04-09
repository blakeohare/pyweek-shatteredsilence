import MapGen

class LevelSeed:
	def __init__(self, special=None, args=None, previousLevel=None):
		self.width = 64
		self.height = 64
		self.mode = 'individual'
		self.map = None
		if args != None:
			try:
				self.map = args.get('map')
			except:
				pass # >:( 3 hours of PyWeek to go. 
		self.specialName = None
		self.won = False
		
		if special != None:
			if special == 'next':
				self.InitializeNextLevel(args, previousLevel)
			else:
				self.InitializeSpecialLevel(special, args, None)
		else:
			self.width = args['width']
			self.height = args['height']
			self.mode = args['mode']
			self.progress = args['progress']
			self.timedMode = args['minutes'] > -1
			self.minutes = args['minutes']
			
			self.citizens = 0
			self.police = 0
		
			self.map = args['map']
	
	def GenerateCustomMap(self, width, height, isUrban, isCrowd):
		generator = MapGen.Generator(width, height, isUrban, isCrowd)
		while not generator.IsDone():
			generator.DoNextTask()
		commands = generator.commands
		return MapGen.BuildMapFromCommands(commands, width, height, None, None)
	
	def InitializeNextCustomLevel(self, previousLevelSeed):
		next = MapGen.PopNextSeed()
		if next == None:
			self.won = True
		else:
			self.width = next.width
			self.height = next.height
			self.mode = next.mode
			self.progress = next.progress
			self.timedMode = next.timedMode
			self.minutes = next.minutes
			self.map = next.map
		self.citizens = 0
		self.police = 0
	
	
	def InitializeNextLevel(self, previousLevelSeed, previousLevel):
		specialName = previousLevelSeed.specialName
		if specialName == None:
			self.InitializeNextCustomLevel(previousLevelSeed)
		elif specialName == 'level1':
			self.InitializeSpecialLevel('level2', previousLevelSeed, previousLevel)
		elif specialName == 'level2':
			self.InitializeSpecialLevel('level3', previousLevelSeed, previousLevel)
		elif specialName == 'level3':
			self.InitializeSpecialLevel('level4', previousLevelSeed, previousLevel)
		elif specialName == 'level4':
			self.InitializeSpecialLevel('level5', previousLevelSeed, previousLevel)
		elif specialName == 'level5':
			self.InitializeSpecialLevel('level6', previousLevelSeed, previousLevel)
		elif specialName == 'level6':
			self.InitializeSpecialLevel('level7', previousLevelSeed, previousLevel)
		elif specialName == 'level7':
			self.InitializeSpecialLevel('level8', previousLevelSeed, previousLevel)
		elif specialName == 'level8':
			self.InitializeSpecialLevel('level9', previousLevelSeed, previousLevel)
		elif specialName == 'level9':
			# TODO: something else
			self.won = True
		elif specialName == 'testlevel':
			self.InitializeSpecialLevel('level1', previousLevelSeed, previousLevel)
			# meh
			
	def InitializeSpecialLevel(self, special, previousLevelSeed, previousLevel):
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
			self.width = 29
			self.height = 33
		elif special == 'level3':
			self.width = 64
			self.height = 64
		elif special == 'level4':
			self.width = 180
			self.height = 100
		elif special == 'level5':
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
			self.mode = 'crowd'
			self.width = 40
			self.height = 32
		elif special == 'level9':
			self.mode = 'crowd'
			self.width = 96
			self.height = 64
		self.map = MapGen.BuildMap(special, self.width, self.height, previousLevelSeed, previousLevel, None)