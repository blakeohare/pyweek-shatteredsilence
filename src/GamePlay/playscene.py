import pygame
from Game import GameSceneBase
import GamePlay
import Resources

class PlayScene(GameSceneBase):
	
	def __init__(self, levelSeed):
		GameSceneBase.__init__(self)
		self.tileWidth = levelSeed.width
		self.tileHeight = levelSeed.height
		self.level = GamePlay.Level(levelSeed)
		self.levelSeed = levelSeed
		self.cameraX = 0
		self.cameraY = 0
		self.dragStart = None
		self.selection = []
		self.cursorLogicalPosition = (0, 0)
		self.cursorScreenPosition = (0, 0)
		self.suppressDragDraw = True
		self.counter = 0
		self.progress = 0.0
		self.specializer = GamePlay.GetSpecializer(self.levelSeed.specialName)
		
		self.font_white = Resources.GetFont(255, 255, 255)
		self.font_red = Resources.GetFont(255, 0, 0)
		self.font_orange = Resources.GetFont(255, 128, 0)
		self.font_yellow = Resources.GetFont(255, 255, 0)
		self.font_green = Resources.GetFont(0, 255, 0)
		self.font_blue = Resources.GetFont(0, 170, 255)
		
		
		
	def ProcessInput(self, events):
		
		for event in events:
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				x = event.pos[0] + self.cameraX
				y = event.pos[1] + self.cameraY
				
				self.SetSelection(self.dragStart, (x, y))
				self.dragStart = None
				
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				x = event.pos[0] + self.cameraX
				y = event.pos[1] + self.cameraY
				self.dragStart = (x, y)
				self.suppressDragDraw = False
			
			elif event.type == pygame.MOUSEMOTION:
				self.cursorScreenPosition = event.pos
				x = event.pos[0] + self.cameraX
				y = event.pos[1] + self.cameraY
				self.cursorLogicalPosition = (x, y)
			
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
				self.MoveSelectionToTarget(event.pos[0] + self.cameraX, event.pos[1] + self.cameraY)
	
	def MoveSelectionToTarget(self, targetX, targetY):
		for sprite in self.selection:
			sprite.SetTarget(targetX, targetY)
	
	def SetSelection(self, startDrag, endDrag):
		
		# not sure how this occurred
		if startDrag == None or endDrag == None: return
		
		left = startDrag[0]
		top = startDrag[1]
		right = endDrag[0]
		bottom = endDrag[1]
		
		if left > right:
			t = left
			left = right
			right = t
		if top > bottom:
			t = top
			top = bottom
			bottom = t
		
		selection = []
		if right - left < 16 and bottom - top < 16:
			sprite = self.level.GetSpriteHitTest((right + left) // 2, (bottom + top) // 2)
			if sprite != None:
				selection =  [sprite]
			else:
				selection = [] 
		else:
			selection = self.level.GetSpritesInRange(left, top, right, bottom)
		
		self.selection = []
		for sprite in selection:
			if sprite.color == 255:
				self.selection.append(sprite)
			
	def Update(self):
		self.counter += 1
		
		self.level.Update()
		
		self.UpdateCamera()
		self.EnsureSelectionValid()
		self.progress = self.level.GetProgress()
		if self.progress >= 80:
			self.next = GamePlay.LevelUpTransition(self)
		
		messages = self.specializer.ShouldShowMessage(self.counter, self.progress)
		if messages != None:
			self.next = ShowMessageOverlay(messages, self)
		
	def EnsureSelectionValid(self):
		for sprite in self.selection:
			if sprite.color != 255:
				newselection = []
				for spriteB in self.selection:
					if spriteB.color == 255:
						newselection.append(spriteB)
				self.selection = newselection
				return
	
	def UpdateCamera(self):
		mouse_position = pygame.mouse.get_pos()
		x = mouse_position[0]
		y = mouse_position[1]
		
		dx = 0
		dy = 0
		
		if x < 64:
			dx = (3 - x // 16) * -1
		elif x > 640 - 63:
			dx = 3 - (640 - x) // 16
		if y < 64:
			dy = (3 - y // 16) * -1
		elif y > 480 - 63:
			dy = 3 - (480 - y) // 16
		
		self.cameraX += dx * 4
		self.cameraY += dy * 4
		
		if self.cameraX < 0: self.cameraX = 0
		if self.cameraY < 0: self.cameraY = 0
		if self.cameraX >= self.tileWidth * 32 - 640: self.cameraX = self.tileWidth * 32 - 640 - 1
		if self.cameraY >= self.tileHeight * 32 - 480: self.cameraY = self.tileHeight * 32 - 480 - 1
		
	def Render(self, screen):
		self.level.RenderTiles(screen, self.cameraX, self.cameraY)
		self.RenderSelection(screen)
		self.level.RenderSprites(screen, self.cameraX, self.cameraY)
		self.RenderDrag(screen)
		self.RenderChrome(screen, self.progress)
		
		mousepos = pygame.mouse.get_pos()
		x = (mousepos[0] + self.cameraX) // 32
		y = (mousepos[1] + self.cameraY) // 32
		mousepos = self.font_white.Render('(' + str(x) + ', ' + str(y) + ')')
		screen.blit(mousepos, (640 - mousepos.get_width(), 480 - mousepos.get_height()))
		
	def RenderChrome(self, screen, progress):
		conversions_text = self.font_white.Render('Conversion: ')
		screen.blit(conversions_text, (0, 0))
		
		if progress < 20: font = self.font_red
		elif progress < 40: font = self.font_orange
		elif progress < 60: font = self.font_yellow
		elif progress < 80: font = self.font_green
		else: font = self.font_blue
		screen.blit(font.Render(str(int(progress)) + '%'), (conversions_text.get_width(), 0))
	
	def RenderSelection(self, screen):
		for sprite in self.selection:
			coords = sprite.RenderCoordinates(self.cameraX, self.cameraY)
			left = coords[0] - 4
			top = coords[1] + sprite.R - 3
			width = sprite.R * 2 + 8
			height = sprite.R + 6
			
			pygame.draw.ellipse(screen, (255, 255, 0), pygame.Rect(left, top, width, height), 2)
	
	def RenderDrag(self, screen):
		
		if self.suppressDragDraw: return
		if self.dragStart == None: return
		
		left = self.dragStart[0] - self.cameraX
		right = self.cursorScreenPosition[0]
		top = self.dragStart[1] - self.cameraY
		bottom = self.cursorScreenPosition[1]
		
		if left > right:
			t = left
			left = right
			right = t
		if bottom < top:
			t = bottom
			bottom = top
			top = t
		
		pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(left, top, right - left, bottom - top), 1)

class ShowMessageOverlay(GameSceneBase):
	
	def __init__(self, messages, playScene):
		GameSceneBase.__init__(self)
		self.playScene = playScene
		self.font = Resources.GetFont(255, 255, 255)
		self.messages = messages
		self.border = Resources.CreateBorder(400, len(messages) * 20 + 60) 
	
	def ProcessInput(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				self.next = self.playScene
				self.playScene.next = self.playScene
	
	def Update(self):
		pass
	
	def Render(self, screen):
		self.playScene.Render(screen)
		x = 30
		y = 10
		screen.blit(self.border, (x, y))
		y -= 5
		for message in (self.messages + ["        ...press enter"]):
			
			y += 20
			image = self.font.Render(message)
			screen.blit(image, (x + 24, y))