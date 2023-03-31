from pos2d import Pos2D
from grid import Grid

class Player:
    pos: Pos2D
    grid: Grid
    
    def __init__(self, initial: Pos2D, grid: Grid):
        self.pos = initial
        self.grid = grid
    
    def move(self, direction: str):
        pos: Pos2D = None
        
        if direction == 'z':
            #monter
            pos = Pos2D(self.pos.getX(), self.pos.getY()-1) 
                
        elif direction == 's':
            #descendre
            pos = Pos2D(self.pos.getX(), self.pos.getY()+1)
            
        elif direction == 'q':
            #gauche
            pos = Pos2D(self.pos.getX()-1, self.pos.getY())
            
        elif direction == 'd':
            #droite
            pos = Pos2D(self.pos.getX()+1, self.pos.getY())
            
        if pos:
            if self.grid.present(self.grid.accessible_neighbours(self.pos), pos):
                self.pos = pos
                return True
        return False