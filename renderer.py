from grid import Grid
from pos2d import Pos2D
from grid import Node
from argparse import Namespace
from generation import DungeonGenerator
from player import Player
from os import system, name
from math import sqrt

class GridRenderer:
    grill:list[list[str]]
    view:list[list[str]]
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
        self.copy()
        
    def copy(self):
        self.view = [[i for i in o] for o in self.grill]
        
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
    
    def _dist(self, p1: Pos2D, p2: Pos2D):
        return sqrt((p2.getX()-p1.getX())**2 + (p2.getY()-p1.getY())**2)
    
    def setToch(self, toch: Pos2D, raduis: int, end: Pos2D):
        self.copy()
        for y in range(0, self.grid.height):
            for x in range(0, self.grid.width):
                if not (self._dist(Pos2D(x, y), toch) <= raduis):
                    self.view[y*2][x*4] = ' '
                    self.view[y*2][x*4 + 1] = ' '
                    self.view[y*2][x*4 + 2] = ' '
                    self.view[y*2][x*4 + 3] = ' '
                    self.view[y*2][x*4 + 4] = ' '
                    self.view[y*2 + 1][x*4] = ' '
                    self.view[y*2 + 2][x*4] = ' '
                    self.view[y*2 + 1][x*4 + 4] = ' '
                    self.view[y*2 + 1][x*4 + 3] = ' '
                    self.view[y*2 + 1][x*4 + 1] = ' '
                    self.view[y*2 + 2][x*4 + 1] = ' '
                    self.view[y*2 + 2][x*4 + 2] = ' '
                    self.view[y*2 + 2][x*4 + 3] = ' '
                    self.view[y*2 + 2][x*4 + 4] = ' '
                    
                    #pour éviter d'effacer le #
                    if Pos2D(x, y) != end:
                        self.view[y*2 + 1][x*4 + 2] = ' '
        
    def show(self):
        row = ""
        for line in self.view:
            row = ""
            for data in line:
                row += data
            print(row)
    
    def _affectContent(self, case: Pos2D, content: str):
        self.grill[case.getY()*2 + 1][case.getX()*4 + 2] = content
        
    def addContent(self, case: Pos2D, content: str):
        self._affectContent(case, content)
    
    def removeContent(self, case:Pos2D):
        self._affectContent(case, ' ')


class Renderer:
    generator: DungeonGenerator
    renderer: GridRenderer
    grid: Grid
    bonuses: list[Pos2D]
    start_position: Pos2D
    exit_position: Pos2D
    end: bool
    light: int
    level: int
    player: Player
    
    def __init__(self, metadata: Namespace):
        self.generator = DungeonGenerator(metadata)
        self.end = False
        self.light = self.generator.view_radius
        self.level = self.generator.torch_delay
        
        data = self.generator.generate()
        
        self.grid = data.get('grid') 
        self.bonuses = data.get('bonuses')
        self.start_position = data.get('start_position') 
        self.exit_position = data.get('exit_position')
        
        self.renderer = GridRenderer(self.grid)
        self.renderer.addContent(self.start_position, 'X')
        
        for pos in self.bonuses:
            self.renderer.addContent(pos, '@')
        self.renderer.addContent(self.exit_position, '#')

        self.player = Player(self.start_position, self.grid)
        
    def mainloop(self):
        self.renderer.setToch(self.start_position, self.light, self.exit_position)
        self.renderer.show()
        
        while not self.end:
            direction = str(input('>> Direction: ')).strip()
            
            if name in ['posix', 'nt', 'java']:
                system('clear')
            else:
                system('cls')
                
            if self.player.move(direction):
                self.level -= 1
            
            if self.level == 0:
                self.light -= 1
                self.level = self.generator.torch_delay
            
            if self.light <= 0:
                self.end = True
                
            self.renderer.removeContent(self.start_position)
            self.start_position = self.player.pos
            self.renderer.addContent(self.start_position, 'X')
            
            if self.grid.present(self.bonuses, self.start_position):
                self.light += self.generator.bonus_radius
                
                if self.light > self.generator.view_radius:
                    self.light = self.generator.view_radius
            
            elif self.start_position == self.exit_position:
                self.end = True
            
            
            self.renderer.setToch(self.start_position, self.light, self.exit_position)
            self.renderer.show()