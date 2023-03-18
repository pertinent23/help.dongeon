from pos2d import Pos2D
from box import Box
from random import randint, shuffle
    
class Node:
    up: bool = True
    left: bool = True
    right: bool = True
    down: bool = True
    
    def clone(self):
        resultat = Node()
        resultat.up = self.up
        resultat.left = self.left
        resultat.right = self.right
        resultat.down = self.down
        
        return resultat

class Grid:
    width:int
    height:int
    grill:list[list[Node]]
    
    def accessible_neighbours(self, pos: Pos2D):
        pass
    
    def add_wall(self, pos1:Pos2D, pos2: Pos2D):
        pass
    
    def remove_wall(self, pos1:Pos2D, pos2: Pos2D):
        pass

class Grid:
    width:int
    height:int
    grill:list[list[Node]]
    
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.grill = []
        
        for x in range(0, self.width):
            self.grill.append([])
            for y in range(0, self.height):
                self.grill[x].append(Node())
                
                if x == 0:
                    self.grill[x][y].left = False
                
                if width - x == 1:
                    self.grill[x][y].right = False
                
                if y == 0:
                    self.grill[x][y].up = False
                
                if height - y == 1:
                    self.grill[x][y].down = False
    
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
        point_haut = box.getPoin1() 
        point_bas = box.getPoin2() 
        
        for y in range(point_haut.getY(), point_bas.getY()+1):
            self.add_wall(Pos2D(point_haut.getX()-1, y), Pos2D(point_haut.getX(), y))
            self.add_wall(Pos2D(point_bas.getX()+1, y), Pos2D(point_bas.getX(), y))
        
        for x in range(point_haut.getX(), point_bas.getX()+1):
            self.add_wall(Pos2D(x, point_haut.getY()-1), Pos2D(x, point_haut.getY()))
            self.add_wall(Pos2D(x, point_bas.getY()+1), Pos2D(x, point_bas.getY()))
    
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

    def _present(self, pile:list[Pos2D], pos:Pos2D):
        for item in pile:
            if item == pos:
                return True
        return False

    def _tree(self, grid: Grid, racine: Pos2D, pile: list[Pos2D], pairs: list[tuple[Pos2D]]):
        pile.append(racine)
        
        neighbours:list[Pos2D] = grid.accessible_neighbours(racine)
        shuffle(neighbours)
        
        for pos in neighbours:
            if not self._present(pile, pos):
                for j in range(0, len(pile)-1):
                    for item in grid.accessible_neighbours(pile[j]):
                        if item != pile[j+1] and (j == 0 or item != pile[j-1]):
                            if item != racine:
                                grid.add_wall(pile[j], item)
                self._tree(grid, pos, pile, pairs)
                pairs.append((pos, racine))

    def spanning_tree(self):
        resultat = Grid(self.width, self.height)
        resultat.grill = [[i.clone() for i in l] for l in self.grill]
        
        pile:list[Pos2D] = list()
        pairs:list[Pos2D] = list()
        self._tree(resultat, Pos2D(randint(0, self.width-1), 0), pile, pairs)
        
        #print([(o.getX(), o.getY()) for o in pile])
        
        if len(pile) <= 1:
            return resultat
        
        for item in pairs:
            resultat.remove_wall(item[0], item[1])
        
        return resultat
