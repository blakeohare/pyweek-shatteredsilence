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
			#self.PlaySound('phase_complete.ogg')
			levelseed = GamePlay.LevelSeed('next', self.prevPlayScene.levelSeed, self.prevPlayScene.level)
			if levelseed.won:
				self.next = GamePlay.WinScene(self.prevPlayScene)
			else:
				self.nextPlayScene = GamePlay.PlayScene(levelseed)
		elif self.counter == 69:
			self.next = self.nextPlayScene
			camOff = self.next.level.initCameraOffset   
			if camOff != None:
				self.next.cameraX = self.prevPlayScene.cameraX + camOff[0] * 32
				self.next.cameraY = self.prevPlayScene.cameraY + camOff[1] * 32

				
			
	
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
		
		ninexWord = Resources.ImageLibrary.Get('9xImage.png')
		dx = (640 - ninexWord.get_width()) // 2
		dy = (480 - ninexWord.get_height()) // 2 - 80 - self.counter * 5
		
		screen.blit(ninexWord, (dx, dy))
		