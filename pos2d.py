class Pos2D:
    pass

class Pos2D:
    _x:int = 0
    _y:int = 0
    
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    def __eq__(self, other: Pos2D):
        return other.getX() == self.getX() and other.getY() == self.getY()
        
    def getX(self):
        return self._x

    def getY(self):
        return self._y
    
    def setX(self, x):
        self._x=x
    
    def setY(self, y):
        self._y = y