import GamePlay

class Level:
    
    def __init__(self, columns, rows):
        self.width = columns
        self.height = rows
        self.pixelWidth = columns * 32
        self.pixelHeight = rows * 32
        self.InitializeTiles(columns, rows)
        self.sprites = []
        self.counter = 0
        
        for i in range(100):
            male = i % 2 == 1
            variety = (i // 25) + 1
            x = i // 10
            y = i % 10
            self.sprites.append(GamePlay.Citizen(30 + x * 45, 30 + y * 45, male, variety))
        
        self.sprites[23].color = 255
    
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
    
    def UpdateTileColors(self):
        counter = self.counter
        width = len(self.tiles)
        height = len(self.tiles[0])
        for sprite in self.sprites:
            if sprite.color == 255:
                x = sprite.X // 32
                y = sprite.Y // 32
                self.tiles[x][y].SetColorization(counter)
                if x > 0:
                    self.tiles[x - 1][y].SetColorization(counter)
                    if y > 0:
                        self.tiles[x - 1][y - 1].SetColorization(counter - 40)
                    if y < height - 1:
                        self.tiles[x - 1][y + 1].SetColorization(counter - 40)
                        
                if y > 0:
                    self.tiles[x][y - 1].SetColorization(counter)
                if x < width - 1:
                    self.tiles[x + 1][y].SetColorization(counter)
                    if y > 0:
                        self.tiles[x + 1][y - 1].SetColorization(counter - 40)
                    if y < height - 1:
                        self.tiles[x + 1][y + 1].SetColorization(counter - 40)
                if y < height - 1:
                    self.tiles[x][y + 1].SetColorization(counter)
                
                
        
        self.counter += 1
                
    
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
    
    def RenderSprites(self, screen, cameraX, cameraY):
        left = cameraX - 64
        right = cameraX + 640 + 64
        top = cameraY - 64
        bottom = cameraY + 480 + 64
        
        for sprite in self.sprites:
            if sprite.X < left or sprite.X > right or sprite.Y < top or sprite.Y > bottom:
                continue
            image = sprite.GetImage()
            
            screen.blit(image, sprite.RenderCoordinates(cameraX, cameraY))
    
    def RenderTiles(self, screen, cameraX, cameraY):
        
        self.UpdateTileColors()
        
        startX = cameraX // 32
        startY = cameraY // 32
        endX = startX + (640 // 32) + 1
        endY = startY + (480 // 32) + 1
        
        if startX < 0: startX = 0
        if startY < 0: startY = 0
        if endX >= self.width: endX = self.width
        if endY >= self.height: endY = self.height
        
        tiles = self.tiles
        
        counter = self.counter
        
        x = startX
        while x < endX:
            y = startY
            while y < endY:
                tile = tiles[x][y]
                drawX = tile.PixelX - cameraX
                drawY = tile.PixelY - cameraY
                screen.blit(tile.GetImage(counter), (drawX, drawY))
                y += 1
            x += 1 

class SpriteGraph:
    
    def __init__(self, map_columns, map_rows):
        self.cols = []
        self.buckets = []
        self.populatedBuckets = {}
        bucketRange = 3
        self.bucketRange = bucketRange
        x = 0
        while x < map_columns:
            y = 0
            col = []
            self.cols.append(col)
            while y < map_rows:
                if x % bucketRange == 0 and y % bucketRange == 0:
                    bucket = SpriteBucket(str(x) + '-' + str(y))
                    self.buckets.append(bucket)
                    col.append(bucket)
                else:
                    col.append(self.cols[(x // bucketRange) * bucketRange][(y // bucketRange) * bucketRange])
                y += 1
            x += 1
        self.width = len(self.cols)
        self.height = len(self.cols[0])
        self.EstablishNeighbors(bucketRange)
    
    def EstablishNeighbors(self, bucketRange):
        
        width = len(self.cols)
        height = len(self.cols[0])
        
        x = 0
        while x < width:
            y = 0
            while y < height:
                bucket = self.cols[x][y]
                
                for neighbor in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                    nx = x + neighbor[0] * bucketRange
                    ny = y + neighbor[1] * bucketRange
                    if nx >= 0 and nx < width and ny >= 0 and ny < height:
                        bucket.AddNeighbor(self.cols[nx][ny])
                
                y += bucketRange
            x += bucketRange
    
    def ClearAll(self):
        for bucket in self.populatedBuckets.values():
            bucket.ClearSprites()
    
    def AddSprite(self, sprite):
        x = sprite.X // 32
        y = sprite.Y // 32
        bucket = self.cols[x][y]
        bucket.AddSprite(sprite)
        self.populatedBuckets[bucket.key] = bucket
        
    def GetSpritesNear(self, x, y, radius, radiates):
        bucket = self.cols[x // 32][y // 32]
        
        if radiates and not bucket.radiates:
            sprites = []
        else:
            sprites = bucket.GetSpritesNear(x, y, radius, radiates)
        for neighbor in bucket.neighbors:
            if not radiates or neighbor.radiates:
                sprites += neighbor.GetSpritesNear(x, y, radius, radiates)
        return sprites 

class SpriteBucket:
    
    def __init__(self, key):
        self.sprites = []
        self.neighbors = []
        self.key = key
        self.radiates = False
        
    def AddSprite(self, sprite):
        if sprite.color == 255: self.radiates = True
        self.sprites.append(sprite)
    
    def ClearSprites(self):
        self.sprites = []
        self.radiates = False
    
    def GetSpritesNear(self, x, y, radius, radiates):
        output = []
        if radiates and not self.radiates: return output
        for sprite in self.sprites:
            dx = sprite.X - x
            dy = sprite.Y - y
            if dx * dx + dy * dy < radius * radius:
                output.append(sprite)
        return output
    
    def AddNeighbor(self, neighbor):
        self.neighbors.append(neighbor)