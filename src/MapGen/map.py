import MapGen
import os

def _trim(string):
    while len(string) > 0 and string[0] in ' \t\r\n':
        string = string[1:]
    while len(string) > 0 and string[-1] in ' \t\r\n':
        string = string[:-1]
    return string
    
def BuildMap(level, width, height):
    path = ''
    if level == 'level1':
        path = 'Levels' + os.sep + 'level1.txt'
    else:
        print("level not found")
        return None
    
    c = open(path, 'rt')
    lines = c.read().split('\n')
    c.close()
    
    items = []
    for line in lines:
        parts = _trim(line).split(' ')
        if parts[0] == 'ROAD':
            item = MapGen.Road(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
            items.append(item)
        elif parts[0] == 'BUILDING':
            raise "not done yet"
    
    return Map(width, height, items)
    
    
    
class Map:
    
    def __init__(self, width, height, items):
        self.InitializeGrid(width, height)
        self.roadSquares = []
        
        items = self.FillGridWithRoads(items)
        items = self.FillGridWithBuildings(items)
        
        self.FleshOutRoads(self.roadSquares)
        
    def FleshOutRoads(self, roadSquares):
        intersections = []
        sidewalk = []
        grid = self.grid
        width = len(grid)
        height = len(grid[0])
        for road in roadSquares:
            x = road[0]
            y = road[1]
            type = grid[x][y]
            if type == 'intersection':
                intersections.append((x, y))
            elif type == 'yellow_line_horizontal':
                if y > 3:
                    grid[x][y - 1] = 'asphault'
                    grid[x][y - 2] = 'asphault'
                    sidewalk.append((x, y - 3))
                if y < height - 3:
                    grid[x][y + 1] = 'asphault'
                    grid[x][y + 2] = 'asphault'
                    sidewalk.append((x, y + 3))
            elif type == 'yellow_line_vertical':
                if x > 3:
                    grid[x - 1][y] = 'asphault'
                    grid[x - 2][y] = 'asphault'
                    sidewalk.append((x - 3, y))
                if x < width - 3:
                    grid[x + 1][y] = 'asphault'
                    grid[x + 2][y] = 'asphault'
                    sidewalk.append((x + 3, y))
        
        for sidewalkunit in sidewalk:
            x = sidewalkunit[0]
            y = sidewalkunit[1]
            grid[x][y] = 'sidewalk'
        
        for intersection in intersections:
            x = intersection[0]
            y = intersection[1]
            
            impose = [
              ['sidewalk_corner4', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'sidewalk_corner3'],
              ['vertical_crosswalk', 'asphault', 'asphault', 'asphault', 'asphault', 'asphault', 'vertical_crosswalk'],
              ['vertical_crosswalk', 'asphault', 'asphault', 'asphault', 'asphault', 'asphault', 'vertical_crosswalk'],
              ['vertical_crosswalk', 'asphault', 'asphault', 'asphault', 'asphault', 'asphault', 'vertical_crosswalk'],
              ['vertical_crosswalk', 'asphault', 'asphault', 'asphault', 'asphault', 'asphault', 'vertical_crosswalk'],
              ['vertical_crosswalk', 'asphault', 'asphault', 'asphault', 'asphault', 'asphault', 'vertical_crosswalk'],
              ['sidewalk_corner2', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'horizontal_crosswalk', 'sidewalk_corner1']]

            col = 0
            while col < 7:
                row = 0
                while row < 7:
                    grid[x + col - 3][y + row - 3] = impose[row][col]
                    row += 1
                col += 1          
            
    def InitializeGrid(self, width, height):
        self.grid = []
        x = 0
        while x < width:
            col = []
            y = 0
            while y < height:
                col.append(None)
                y += 1 
            x += 1
            self.grid.append(col)
    
    def FillGridWithRoads(self, items):
        notroads = []
        for item in items:
            if item.IsRoad:
                self.roadSquares += item.ApplySelfToGrid(self.grid)
            else:
                notroads.append(item)
        return notroads

    def FillGridWithBuildings(self, items):
        notbuildings = []
        for item in items:
            if item.IsBuilding:
                item.ApplySelfToGrid(self.grid)
            else:
                notbuildings.append(item)
        return notbuildings