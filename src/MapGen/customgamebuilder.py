import GamePlay

class CustomGameBuilder:
	
	def __init__(self, args):
		self.args = args
		
	def GetPlayScene(self):
		levelseed = GamePlay.LevelSeed(None, self.args)
		return GamePlay.PlayScene(levelseed)
