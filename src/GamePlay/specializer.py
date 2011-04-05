def GetSpecializer(levelName):
	if levelName == 'level1': return Level1Specializer()
	if levelName == 'level2': return Level2Specializer()
	if levelName == 'level3': return Level3Specializer()
	if levelName == 'level4': return Level4Specializer()
	if levelName == 'level5': return Level5Specializer()
	if levelName == 'level6': return Level6Specializer()
	if levelName == 'level7': return Level7Specializer()
	if levelName == 'level8': return Level8Specializer()
	if levelName == 'level9': return Level9Specializer()
	return SpecializerBase()

class SpecializerBase:
	
	def __init__(self):
		pass
	
	def ShouldShowMessage(self, counter, conversionProgress):
		return None

class Level1Specializer(SpecializerBase):
	def __init__(self):
		pass
	
	def ShouldShowMessage(self, counter, conversionProgress):
		if counter == 2:
			return ['This is story mode. This should', 'probably say something interesting']
		
class Level2Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level3Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level4Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level5Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level6Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level7Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level8Specializer(SpecializerBase):
	def __init__(self):
		pass
	
class Level9Specializer(SpecializerBase):
	def __init__(self):
		pass
	