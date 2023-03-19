from grid import Grid
from argparse import Namespace
from box import Box
from math import floor
from random import randint
from pos2d import Pos2D

class DungeonGenerator:
    grid: Grid
    pieces: list[Box]
    openinsList: list[tuple[Pos2D]]
    
    width: int
    height: int
    rooms: int
    seed: int
    
    minwidth: int
    maxwidth: int
    minheight: int
    maxheight: int
    
    openings: int
    hard: bool
    
    def __init__(self, params: Namespace):
        self.openinsList = []
        self.width = params.width
        self.height = params.height
        self.rooms = params.rooms
        self.seed = params.seed
        self.minwidth = params.minwidth
        self.maxwidth = params.maxwidth
        self.minheight = params.minheight
        self.maxheight = params.maxheight
        self.openings = params.openings
        self.hard = params.hard
        self._create_grid()
        self._generer_pieces()
        self._load_box()
        self._generer_portes()
    
    def _create_grid(self):
        self.grid = Grid(self.width, self.height)
    
    def _present(self, pile:list[tuple[Pos2D]], pos:Pos2D):
        for item in pile:
            if item[0] == pos:
                return True
        return False
    
    def _add_portes(self, box: Box):
        haut = box.getPoin1()
        bas = box.getPoin2()
        n = 0
        p = 8
        
        while n < self.openings:
            for y in range(haut.getY(), bas.getY()+1):
                
                pos = Pos2D(haut.getX(), y)
                if n < self.openings and randint(0, 10) > p and not self._present(self.openinsList, pos):
                    self.openinsList.append((pos, Pos2D(pos.getX()-1, pos.getY())))
                    n+=1
                
                pos = Pos2D(bas.getX(), y)
                if n < self.openings and randint(0, 10) > p and not self._present(self.openinsList, pos):
                    self.openinsList.append((pos, Pos2D(pos.getX()+1, pos.getY())))
                    n+=1
            
            for x in range(haut.getX(), bas.getX()+1):
                
                pos = Pos2D(x, haut.getY())
                if n < self.openings and randint(0, 10) > p and not self._present(self.openinsList, pos):
                    self.openinsList.append((pos, Pos2D(pos.getX(), pos.getY()-1)))
                    n+=1
                
                pos = Pos2D(x, bas.getY())
                if n < self.openings and randint(0, 10) > p and not self._present(self.openinsList, pos):
                    self.openinsList.append((pos, Pos2D(pos.getX(), pos.getY()+1)))
                    n+=1
                        
    
    def _generer_portes(self):
        for piece in self.pieces:
            self._add_portes(piece)
    
    def _generer_pieces(self):
        self.pieces = []
        
        nombre_piece_possible_x = floor((self.width)/(self.minwidth+2))
        nombre_piece_possible_y = floor((self.height)/(self.minheight+2))
        nombre_piece_possible = nombre_piece_possible_x * nombre_piece_possible_y
        interval_x = 0
        interval_y = 0
        max_width = self.minwidth
        max_height = self.minheight
        
        if self.rooms < 1 or not nombre_piece_possible_x or not nombre_piece_possible_y:
            return;
        
        final_x = self.rooms // nombre_piece_possible_y
        
        if nombre_piece_possible < self.rooms:
            print(">> Pas assez d'espace pour générer le nombre de cases requises")
        else:
            interval_x = floor((self.width-final_x*(self.minwidth+2))/final_x)
            interval_y = floor((self.height-nombre_piece_possible_y*(self.minheight+2))/nombre_piece_possible_y)
            
            if max_width + interval_x > self.maxwidth:
                max_width = self.maxwidth
            else:
                max_width += interval_x
            
            if max_height + interval_y > self.maxheight:
                max_height = self.maxheight
            else:
                max_height += interval_y
        
        x = 1
        y = 1
        n = 0
        xal = 0
        yal = 0
        
        if n == self.rooms:
            return n;
        
        while x < self.width and x+max_width-1 < self.width and y+max_height-1 < self.height:
            xal = randint(0, max_width - self.minwidth)
            yal = randint(0, max_height - self.minheight)
            x += xal
            y += yal
            width = self.minwidth if self.minwidth == max_width else randint(self.minwidth, max_width - xal)
            height = self.minheight if self.minheight == max_height else randint(self.minheight, max_height - yal)
            
            piece = Box()
            piece.setPoin1(Pos2D(x, y))
            piece.setPoin2(Pos2D(x+width-1, y+height-1))
            self.pieces.append(piece)
            n += 1
            
            if n == self.rooms:
                return n;
            
            y += height + 2
            while y < self.height and y+max_height-1 < self.height and x+max_width-1 < self.width:
                xal = randint(0, max_width - self.minwidth)
                yal = randint(0, max_height - self.minheight)
                x += xal
                y += yal
                width = self.minwidth if self.minwidth == max_width else randint(self.minwidth, max_width-xal)
                height = self.minheight if self.minheight == max_height else randint(self.minheight, max_height-yal)
                
                piece = Box()
                piece.setPoin1(Pos2D(x, y))
                piece.setPoin2(Pos2D(x+width-1, y+height-1))
                self.pieces.append(piece)
                
                y += height + 2
                n += 1
                
                if n == self.rooms:
                    return n;
            
            x += width + 2
        
        return n
    
    def _load_box(self):
        for box in self.pieces:
            self.grid.isolate_box(box)
    
    def generate(self):
        resultat = Grid(self.width, self.height)
        resultat.grill = [[i.clone() for i in l] for l in self.grid.grill]
        
        if self.hard:
            resultat = resultat.spanning_tree()
        else:
            sp1 = resultat.spanning_tree()
            sp2 = resultat.spanning_tree()
            
            for x in range(0, self.width):
                for y in range(0, self.height):
                    resultat.grill[x][y].up = sp1.grill[x][y].up or sp2.grill[x][y].up
                    resultat.grill[x][y].down = sp1.grill[x][y].down or sp2.grill[x][y].down
                    resultat.grill[x][y].left = sp1.grill[x][y].left or sp2.grill[x][y].left
                    resultat.grill[x][y].right = sp1.grill[x][y].right or sp2.grill[x][y].right
        
        for item in self.openinsList:
            pos1, pos2 = item
            resultat.remove_wall(pos1, pos2)
    
        return {
            "grid": resultat
        }