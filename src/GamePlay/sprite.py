from Resources import ImageLibrary

class Sprite:
    
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.targetX = x
        self.targetY = y
        self.R = 16
        self.color = 0
        self.direction = 'down'
    
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
        return ImageLibrary.Get('temp_dude.png')
    
    def RenderCoordinates(self, camX, camY):
        return (self.X - self.R - camX, self.Y - self.R - camY)