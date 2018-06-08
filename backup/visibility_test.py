from itertools import product
from collections import namedtuple
import math

Point = namedtuple('Point', ['x', 'y'])

class AgentNode:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return 'A'
    
class WallNode:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'W'
class VisitedNode:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'V'


class Grid:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.nodes = {}

    def __getitem__(self,coord):
        if coord.x >= self.width or coord.x <0:
            raise ValueError
        if coord.y >= self.height or coord.y <0:
            raise ValueError
        
        if coord in self.nodes:
            return self.nodes[coord]
        else:
            return None

    def __setitem__(self,coord,node):
        if coord.x >= self.width or coord.x <0:
            raise ValueError
        if coord.y >= self.height or coord.y <0:
            raise ValueError
        self.nodes[coord] = node

    def __str__(self):
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                if Point(x,y) in self.nodes:
                    s+= str(self.nodes[Point(x,y)])
                else:
                    s+='_'
            s+='\n'
        return s
        

    
        
def distance(node1,node2):
        return math.sqrt((node2.x-node1.x)**2 + (node2.y-node1.y)**2)

def compute_neighbors(node,width,height):
    
    xc = [node.x,node.x-1,node.x+1]
    yc = [node.y,node.y-1,node.y+1]
    
    if node.x == width-1:
        xc.remove(node.x+1)
    if node.x == 0:
        xc.remove(node.x-1)
    if node.y == height-1:
        yc.remove(node.y+1)
    if node.y == 0:
        yc.remove(node.y-1)
    neighbors = [Point(*n) for n in product(xc,yc)]
    neighbors.remove(node)
    return neighbors

def breadth_first(grid,start):
    frontier = []
    frontier.append(start)
    agents = []
    paths = {}
    came_from = {}
    came_from[start]=None
    

    while len(frontier) > 0:
        current = frontier.pop()
        neighbors = compute_neighbors(current,grid.width,grid.height)
        for node in neighbors:
            
            if  node not in came_from and (type(grid[node])!= WallNode):
                frontier.append(node)
                if type(grid[node])==AgentNode:
                    agents.append(node)
                
                came_from[node]=current

    for a in agents:
        path = a
        paths[a] = []
        
        while path != None:
            path = came_from[path]
            paths[a].append(path)
               
                
    return came_from,paths
                
                
if __name__=='__main__':
    grid = Grid(16,16)
    grid[Point(5,5)]=AgentNode(5,5)
    grid[Point(7,5)]=AgentNode(7,5)
    grid[Point(10,8)]=AgentNode(10,8)
    grid[Point(2,2)]=AgentNode(2,2)
    grid[Point(5,9)]=AgentNode(5,9)

    grid[Point(3,6)]=WallNode(3,6)
    grid[Point(4,6)]=WallNode(4,6)
    grid[Point(5,6)]=WallNode(5,6)
    grid[Point(6,6)]=WallNode(6,6)
    grid[Point(7,6)]=WallNode(7,6)
    grid[Point(4,2)]=WallNode(4,2)
    grid[Point(5,11)]=WallNode(5,11)
    
    print(grid)
    cf,p = breadth_first(grid,Point(5,5))
    print(p)



    
    
