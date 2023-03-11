from pos2d import Pos2D
from box import Box

class Node:
    up: bool = True
    left: bool = True
    right: bool = True
    down: bool = True


class Grid:
    width:int
    height:int
    grill:list[list[Node]]
    
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.grill = []
        
        for i in range(0, self.width):
            self.grill.append([])
            for j in range(0, self.height):
                self.grill[i].append(Node())
    
    def _wall_manager(self, pos1:Pos2D, pos2:Pos2D, val:bool):
        dx = pos1.getX() - pos2.getX()
        dy = pos1.getY() - pos2.getY()
        
        if (abs(dx) == 1) ^ (abs(dy) == 1):
            if dx > 0:
                self.grill[pos1.getX()][pos1.getY()].left = val
                self.grill[pos2.getX()][pos2.getY()].right = val
            elif dx < 0:
                self.grill[pos1.getX()][pos1.getY()].right = val
                self.grill[pos2.getX()][pos2.getY()].left = val
            
            
            if dy > 0:
                self.grill[pos1.getX()][pos1.getY()].up = val
                self.grill[pos2.getX()][pos2.getY()].down = val
            elif dy < 0:
                self.grill[pos1.getX()][pos1.getY()].down = val
                self.grill[pos2.getX()][pos2.getY()].up = val
    
    def add_wall(self, pos1:Pos2D, pos2: Pos2D):
        self._wall_manager(pos1, pos2, False)
    
    def remove_wall(self, pos1:Pos2D, pos2: Pos2D):
        self._wall_manager(pos1, pos2, True)

    
    def isolate_box(self, box: Box):
        point_haut = box.getPoin1() if box.getPoin1().getY() < box.getPoin2().getY() else box.getPoin2()
        point_bas = box.getPoin2() if box.getPoin1() == point_haut else box.getPoin1()
        
        for y in range(point_haut.getY(), point_bas.getY()+1):
            self.add_wall(Pos2D(point_haut.getX(), y), Pos2D(point_haut.getX()+1, y))
            self.add_wall(Pos2D(point_bas.getX(), y), Pos2D(point_bas.getX()-1, y))
        
        for x in range(point_haut.getX(), point_bas.getX()+1):
            self.add_wall(Pos2D(x, point_haut.getY()), Pos2D(x, point_haut.getY()+1))
            self.add_wall(Pos2D(x, point_bas.getY()), Pos2D(x, point_bas.getY()-1))
    
    def accessible_neighbours(self, pos: Pos2D):
        result: list[Pos2D] = []
        node = self.grill[pos.getX()][pos.getY()]
        
        if node.up and pos.getY()-1 >= 0:
            result.append(Pos2D(pos.getX(), pos.getY()-1))
        
        if node.down and pos.getY()+1 < self.height:
            result.append(Pos2D(pos.getX(), pos.getY()+1))
            
        if node.left and pos.getX()-1 >= 0:
            result.append(Pos2D(pos.getX()-1, pos.getY()))
        
        if node.right and pos.getX()+1 < self.width:
            result.append(Pos2D(pos.getX()+1, pos.getY()))

        return result
