class MapItem:
    
    def __init__(self):
        self.IsRoad = False
    

class Building(MapItem):
    
    def __init__(self, width, height, variety):
        MapItem.__init__(self)
    
    

class Road(MapItem):
    
    def __init__(self, startX, startY, endX, endY):
        MapItem.__init__(self)
        self.IsRoad = True
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
    
    def ApplySelfToGrid(self, grid):
        road_squares = []
        if self.startY == self.endY:
            left = self.startX
            right = self.endX
            if left > right:
                t = left
                left = right
                right = t
            x = left
            y = self.startY
            while x <= right:
                if grid[x][y] != 'intersection':
                    if grid[x][y] == 'yellow_line_vertical':
                        grid[x][y] = 'intersection'
                    else:
                        grid[x][y] = 'yellow_line_horizontal'
                    road_squares.append((x, y))
                x += 1
        else:
            top = self.startY
            bottom = self.endY
            if bottom < top:
                t = bottom
                bottom = top
                top = t
            x = self.startX
            y = top
            while y <= bottom:
                if grid[x][y] != 'intersection':
                    if grid[x][y] == 'yellow_line_horizontal':
                        grid[x][y] = 'intersection'
                    else:
                        grid[x][y] = 'yellow_line_vertical'
                    road_squares.append((x, y))
                y += 1
        return road_squares
            
            