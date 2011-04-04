from Resources import ImageLibrary

class Sprite:
    
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.DX = 0
        self.DY = 0
        self.targetX = x
        self.targetY = y
        self.R = 16
        self.color = 0
        self.V = 4.2
        self.direction = 'down'
        self.colorizeable = False
        self.IsRadiating = False
    
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
        raise "You were supposed to override Sprite.GetImage"
    
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
                self.DX = self.targetX - self.X
                self.DY = self.targetY - self.Y
            else:
                self.DX = int(dx / distance * self.V)
                self.DY = int(dy / distance * self.V)
    
class Citizen(Sprite):
    
    def __init__(self, x, y, male, variety):
        Sprite.__init__(self, x, y)
        self.colorizeable = True
        self.imagepath = ('Girl', 'Dude')[male] + str(variety)
    
    def GetImage(self):
        return ImageLibrary.Get('Sprites/' + self.imagepath + '/down0.png', self.color)

class Police(Sprite):
    
    def __init__(self, x, y, variety):
        Sprite.__init__(self, x, y)
        self.target = None
        self.mode = 'walking' # modes are 'walking', 'pursuit', and 'smackdown'
        self.counter = 0
    
    def GetImage(self):
        if self.mode == 'walking':
            image = 'temp_police0.png'
        elif self.mode == 'smackdown':
            if (self.counter / 15) % 2 == 0:
                image = 'temp_police1.png'
            else:
                image = 'temp_police2.png'
        else:
            image = 'temp_police2.png'
        return ImageLibrary.Get(image, 0)
    
    def Update(self):
        self.counter += 1
        if self.target != None:
            self.targetX = self.target.X
            self.targetY = self.target.Y
            dx = self.targetX - self.X
            dy = self.targetY - self.Y
            if dx * dx + dy * dy < (1.5 * 32) ** 2:
                self.mode = 'smackdown'
            else:
                self.mode = 'pursuit'
        else:
            self.mode = 'walking'
            pass #TODO: patrol mode (most likely walk till you hit a wall and turn left, repeat
        Sprite.Update(self)
        
    def TargetCitizen(self, citizen):
        self.target = citizen
        