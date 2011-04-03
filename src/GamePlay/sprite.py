from Resources import ImageLibrary

class Sprite:
    
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.targetX = x
        self.targetY = y
        self.R = 16
        self.color = 0
        self.V = 4.2
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
    
    
    def GetImage(self, opacity):
        return ImageLibrary.Get('Sprites/Dude1/down0.png', opacity)
    
    def RenderCoordinates(self, camX, camY):
        return (self.X - self.R - camX, self.Y - self.R - camY)
    
    def SetTarget(self, x, y):
        self.targetX = x
        self.targetY = y
    
    def Update(self):
        if self.targetX != self.X or self.targetY != self.Y:
            dx = self.targetX - self.X
            dy = self.targetY - self.Y
            distance = (dx * dx + dy * dy) ** 0.5
            if distance < self.V:
                self.X = self.targetX
                self.Y = self.targetY
            else:
                self.X = self.X + int(dx / distance * self.V)
                self.Y = self.Y + int(dy / distance * self.V)
        