from grid import Grid
from pos2d import Pos2D
from grid import Node

class GridRenderer:
    grill:list[list[str]]
    grid:Grid
    
    def __init__(self, grid: Grid):
        self.grill = []
        self.grid = grid
        self.fill()
        
        for x in range(0, grid.width):
            for y in range(0, grid.height):
                node = grid.grill[x][y]
                self.make(node, x, y)
    
        self.createBorder()
        
    def createBorder(self):
        for x in range(0, self.grid.width):
            if x == 0:
                self.grill[(self.grid.height-1)*2+2][x*4]='└'
            else:
                if not self.grid.grill[x][self.grid.height-1].left:
                    self.grill[(self.grid.height-1)*2+2][x*4]='┴'
                else:
                    self.grill[(self.grid.height-1)*2+2][x*4]='─'
            
            for n in range(1, 5):
                self.grill[(self.grid.height-1)*2+2][x*4+n] = '─'
            
            if x == self.grid.width-1:
                self.grill[(self.grid.height-1)*2+2][x*4+4]='┘'
        
        for y in range(0, self.grid.height):
            if y == 0:
                self.grill[y*2][(self.grid.width-1)*4+4]='┐'
            else:
                if not self.grid.grill[self.grid.width-1][y].up:
                    self.grill[y*2][(self.grid.width-1)*4+4]='┤'
                else:
                    self.grill[y*2][(self.grid.width-1)*4+4]='│'
            
            for n in range(1, 2):
                self.grill[y*2+n][x*4+4]='│'
    
    def make(self, node:Node, x:int, y:int):
        other = None
                
        if not node.left:
            self.grill[y*2+1][x*4]='│'
        
        if not node.up:
            for i in range(x*4+1, x*4+4):
                self.grill[y*2][i]='─'
                
        if not node.up and not node.left:
            if x-1 < 0 and y-1 < 0:
                self.grill[y*2][x*4]='┌'
                
            elif x-1 >= 0 and y-1 >=0:
                other = self.grid.grill[x-1][y-1]
                if not other.right and not other.down:
                    self.grill[y*2][x*4]='┼'
                elif not other.right:
                    self.grill[y*2][x*4]='├'
                elif not other.down:
                    self.grill[y*2][x*4]='┬'
                else:
                    self.grill[y*2][x*4]='┌'
            
            elif x-1 >= 0:
                other = self.grid.grill[x-1][y]
                if not other.up:
                    self.grill[y*2][x*4]='┬'
                else:
                    self.grill[y*2][x*4]='┌'
            
            elif y-1 >= 0:
                other = self.grid.grill[x][y-1]
                
                if not other.left:
                    self.grill[y*2][x*4]='├'
                else:
                    self.grill[y*2][x*4]='┌'
        
        elif node.up and node.left:
            if x-1 >= 0 and y-1 >=0:
                other = self.grid.grill[x-1][y-1]
                if not other.right and not other.down:
                    self.grill[y*2][x*4]='┘'
                elif not other.right:
                    self.grill[y*2][x*4]='│'
                elif not other.down:
                    self.grill[y*2][x*4]='─'
                    
            elif x-1 >= 0 and not self.grid.grill[x-1][y].up:
                self.grill[y*2][x*4]='─'
            
            elif y-1 >= 0 and not self.grid.grill[x][y-1].left:
                self.grill[y*2][x*4]='│'
        
        elif not node.up:
            if x-1 >= 0 and y-1 >=0 and not self.grid.grill[x-1][y-1].down and not self.grid.grill[x-1][y-1].right:
                self.grill[y*2][x*4]='┴'
            elif y-1 >=0 and not self.grid.grill[x][y-1].left:
                self.grill[y*2][x*4]='└'
            elif x-1 >= 0 and not self.grid.grill[x-1][y].up:
                self.grill[y*2][x*4]='─'
        
        elif not node.left:
            if x-1 >= 0 and y-1 >=0 and not self.grid.grill[x-1][y-1].down and not self.grid.grill[x-1][y-1].right:
                self.grill[y*2][x*4]='┤'
            elif y-1 >=0 and not self.grid.grill[x][y-1].left:
                self.grill[y*2][x*4]='│'
            elif x-1 >= 0 and not self.grid.grill[x-1][y].up:
                self.grill[y*2][x*4]='┐'
                
    def fill(self):
        for i in range(0, self.grid.height*2+1):
            self.grill.append([])
            for j in range(0, self.grid.width*4+1):
                self.grill[i].append(' ')
                
    
    def show(self):
        row = ""
        for line in self.grill:
            row = ""
            for data in line:
                row += data
            print(row)