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