from pos2d import Pos2D

class Box:
    _point1: Pos2D
    _point2: Pos2D
    
    def setPoin1(self, point:Pos2D):
        self._point1 = point
    
    def setPoin2(self, point:Pos2D):
        self._point2 = point
    
    def getPoin1(self):
        return self._point1
    
    def getPoin2(self):
        return self._point2