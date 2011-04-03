import GamePlay

class Level:
    
    def __init__(self, columns, rows):
        self.width = columns
        self.height = rows
        self.pixelWidth = columns * 32
        self.pixelHeight = rows * 32
        self.InitializeTiles(columns, rows)
        self.sprites = []
        
        for i in range(100):
            male = i % 2 == 1
            variety = (i // 25) + 1
            x = i // 10
            y = i % 10
            self.sprites.append(GamePlay.Citizen(30 + x * 45, 30 + y * 45, male, variety))
    
    def InitializeTiles(self, columns, rows):
        tiles = []
        
        grass = GamePlay.TileTemplate()
        x = 0
        while x < columns:
            y = 0
            column = []
            while y < rows:
                column.append(GamePlay.Tile(x, y, grass))
                y += 1
            tiles.append(column)
            x += 1
        
        self.tiles = tiles
    
    def GetSpritesInRange(self, left, top, right, bottom):
        sprites = []
        for sprite in self.sprites:
            if sprite.X >= left and sprite.X <= right and sprite.Y >= top and sprite.Y <= bottom:
                sprites.append(sprite)
        return sprites 
    
    # arguments are level coordinates already normalized with the camera viewport into consideration
    def GetSpriteHitTest(self, pixelX, pixelY):
        winnerDistance = 9999999
        winner = None
        for sprite in self.sprites:
            dx = sprite.X - pixelX
            dy = sprite.Y - pixelY
            d = dx * dx + dy * dy
            r = sprite.R + 5
            if d < winnerDistance and d < r * r:
                winner = sprite
                winnerDistance = d
        return winner
    
    def RenderSprites(self, screen, cameraX, cameraY, opacity):
        left = cameraX - 64
        right = cameraX + 640 + 64
        top = cameraY - 64
        bottom = cameraY + 480 + 64
        
        for sprite in self.sprites:
            if sprite.X < left or sprite.X > right or sprite.Y < top or sprite.Y > bottom:
                continue
            image = sprite.GetImage(opacity)
            
            screen.blit(image, sprite.RenderCoordinates(cameraX, cameraY))
    
    def RenderTiles(self, screen, cameraX, cameraY, opacity):
        startX = cameraX // 32
        startY = cameraY // 32
        endX = startX + (640 // 32) + 1
        endY = startY + (480 // 32) + 1
        
        if startX < 0: startX = 0
        if startY < 0: startY = 0
        if endX >= self.width: endX = self.width
        if endY >= self.height: endY = self.height
        
        tiles = self.tiles
        
        x = startX
        while x < endX:
            y = startY
            while y < endY:
                tile = tiles[x][y]
                drawX = tile.PixelX - cameraX
                drawY = tile.PixelY - cameraY
                screen.blit(tile.GetImage(opacity), (drawX, drawY))
                y += 1
            x += 1 