# -*- coding: utf-8 -*-
from math import sqrt

class Node():
    def __init__(self, x,y):
        self.x = x
        self.y = y
    
    def distance(self,node2):
        return sqrt((node2.x-self.x)**2 + (node2.y-self.y)**2)
    
    def __eq__(self, n):
        if n.x == self.x and n.y == self.y:
            return True
        return False

    def __hash__(self):
        return hash(str(self.x)+str(self.y))

    def __repr__(self):
        return "Empty: x=%d y=%d"%(self.x,self.y)
    
    def __str__(self):
        return '_'


class WallNode(Node):
    def __init__(self,x,y):
        Node.__init__(self,x,y)

    def __repr__(self):
        return "Wall: x=%d y=%d"%(self.x,self.y)
    
    def __str__(self):
        return 'W'

if __name__=='__main__':
    wn = WallNode(*(2,3))
    print(wn)
    print(repr(wn))
    print()