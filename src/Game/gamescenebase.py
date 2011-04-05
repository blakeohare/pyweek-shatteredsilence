class GameSceneBase:
	
	def __init__(self):
		self.next = self
		
	def ProcessInput(self, events):
		raise "This method must be overridden"
	
	def Update(self):
		raise "This method must be overridden"
	
	def Render(self, screen):
		raise "This method must be overridden"