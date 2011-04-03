import GamePlay

class Level:
    
    def __init__(self, columns, rows):
        self.width = columns
        self.height = rows
        self.pixelWidth = columns * 32
        self.pixelHeight = rows * 32
        self.InitializeTiles(columns, rows)
        self.sprites = []
        self.sprites.append(GamePlay.Sprite(64, 64))
    
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
    
    def RenderTiles(self, screen, cameraX, cameraY):
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
                screen.blit(tile.GetImage(), (drawX, drawY))
                y += 1
            x += 1 