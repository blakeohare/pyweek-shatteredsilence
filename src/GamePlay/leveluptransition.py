import Game
import Resources
import GamePlay

class LevelUpTransition(Game.GameSceneBase):
	
	def __init__(self, prevPlayScene):
		Game.GameSceneBase.__init__(self)
		self.prevPlayScene = prevPlayScene
		self.nextPlayScene = None
		self.counter = 0
	
	def ProcessInput(self, events):
		pass
	
	def Update(self):
		self.counter += 1
		if self.counter == 3:
			self.PlaySound('phase_complete.ogg')
			self.nextPlayScene = GamePlay.PlayScene(GamePlay.LevelSeed('next', self.prevPlayScene.levelSeed))
		elif self.counter == 69:
			self.next = self.nextPlayScene  
			
	
	def Render(self, screen):
		self.prevPlayScene.Render(screen)
		ninex = Resources.ImageLibrary.Get('levelup.png')
		x = (640 - ninex.get_width()) / 2
		y = (480 - ninex.get_height()) / 2
		
		if self.counter < 45:
			screen.blit(ninex, (x, y))
		else:
			offset = self.counter - 45
			x -= offset * 24
			screen.blit(ninex, (x, y))