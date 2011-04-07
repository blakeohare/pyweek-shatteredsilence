import Game
import GamePlay
import Resources
import Menus

class LoadingScreen(Game.GameSceneBase):
	
	def __init__(self):
		Game.GameSceneBase.__init__(self)
		self.counter = 0
		self.font = Resources.GetFont(255, 255, 255)
		self.x = None
		self.progress = 0
	
	def ProcessInput(self, events):
		pass
	
	def Update(self):
		progress = GamePlay.LoadNextTile()
		if progress == None or progress > 20:
			self.next = Menus.Title()
			self.progress = 100
		else:
			self.progress = progress
		self.counter += 1
	
	def Render(self, screen):
		text = 'Loading' + ('.' * ((self.counter) % 4))
		text2 = str(self.progress) + '%'
		image = self.font.Render(text)
		screen.fill((0, 0, 0))
		if self.x == None:
			self.x = (640 - image.get_width()) / 2
		y = (480 - image.get_height()) / 2 - 50
		screen.blit(image, (self.x, y))
		screen.blit(self.font.Render(text2), (self.x + 20, y + 20))
	