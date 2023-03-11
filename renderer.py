from grid import Grid
from pos2d import Pos2D

class GridRenderer:
    grill:list[list[str]]
    
    def __init__(self, grid: Grid):
        for x in range(0, grid.width):
            self.grill.append([])
            for y in range(0, grid.height):
                pos = Pos2D(x, y)
                neighbours = grid.accessible_neighbours(pos)
                
                if len(neighbours) == 1:
                    if abs(neighbours[0].getX() - pos.getX()) == 1:
                        self.grill[x][y].append('─')
                    
                    if abs(neighbours[0].getY() - pos.getY()) == 1:
                        self.grill[x][y].append('│')
    
    def show(self):
        pass