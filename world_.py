from math import *
from agent_node import *
from collections import namedtuple
from itertools import product
from config_parser import *

#Nodes do not share any parental/inheritance relations,
#I am relying on duck-typing

class WallNode:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return "Wall: x=%d y=%d"%(self.x,self.y)
    
    def __str__(self):
        return 'W'

Node = namedtuple('Node', ['x', 'y'])

def geom_distance(node1,node2):
        return sqrt((node2.x-node1.x)**2 + (node2.y-node1.y)**2)

class Grid:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.nodes = {}

    def __getitem__(self,coord):
        if coord.x >= self.width or coord.x <0:
            print("x= %d y=%d"%(coord.x,coord.y))
            raise IndexError("x coordinate out of bounds")
        if coord.y >= self.height or coord.y <0:
            print("x= %d y=%d"%(coord.x,coord.y))
            raise IndexError("y coordinate out of bounds")

        if coord in self.nodes:
            return self.nodes[coord]
        else:
            return None

    def __setitem__(self,coord,node):
        if coord.x >= self.width or coord.x <0:
            print("x= %d y=%d"%(coord.x,coord.y))
            raise IndexError("x coordinate out of bounds")
        if coord.y >= self.height or coord.y <0:
            print("x= %d y=%d"%(coord.x,coord.y))
            raise IndexError("y coordinate out of bounds")
        self.nodes[coord] = node

    def __str__(self):
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                if Node(x,y) in self.nodes:
                    s+= str(self.nodes[Node(x,y)])
                else:
                    s+='_'
            s+='\n'
        return s

    def compute_neighbors(self, node):

        xc = [node.x]
        yc = [node.y]

        if node.x < self.width-1:
            xc.append(node.x+1)
        if node.x > 0:
            xc.append(node.x-1)
        if node.y < self.height-1:
            yc.append(node.y+1)
        if node.y > 0:
            yc.append(node.y-1)

        neighbors = [Node(*n) for n in product(xc,yc)]
        neighbors.remove(Node(node.x,node.y))
        return neighbors

    def breadth_first(self, start):
        '''Finds minimum path between start
        node and all other nodes'''

        frontier = []
        frontier.append(start)
        agents = []
        paths = {}
        came_from = {}
        came_from[start]=None

        while len(frontier) > 0:
            
            current = frontier.pop(0)
            neighbors = self.compute_neighbors(current)
            for node in neighbors:

                if  node not in came_from and (type(self[node])!= WallNode):
                    frontier.append(node)
                    if type(self[node])==AgentNode:
                        agents.append(node)

                    came_from[node]=current

        for a in agents:
            step = a
            paths[a] = []
            steps = 0
            
            while step is not None:
                
                step = came_from[step]
                paths[a].append(step)
                steps+=1
 
        return came_from,paths

class World:

    def __init__(self,width=10,height=10, v_threshold = 3):
        self.grid = Grid(width,height)
        self.width = width
        self.height = height
        self.visibility_threshold = v_threshold

    def __str__(self):
        return str(self.grid)

    def load(self,filename):
        world,agents,walls = read_config(filename)
        #load world parameters
        self.width = world['width']
        self.height = world['height']
        self.visibility_threshold = world['v_threshold']
        self.grid = Grid(width=self.width,height=self.height)

        #Load agent nodes
        for ag in agents:
            a = AgentNode(address=ag['mac'], x=ag['x'], y=ag['y'])
            a.set_station()
            self.add_node(a)
        #Load walls
        for wl in walls:
            w = WallNode(x=wl['x'], y=wl['y'])
            self.add_node(w)


    def add_node(self,node):
        if type(self.grid[Node(node.x,node.y)]) in (WallNode,AgentNode):
            raise Exception("Cell already occupied!")
        self.grid[Node(node.x,node.y)] = node

    def kill_node(self,node):
        print(repr(self.grid.nodes[Node(node.x,node.y)]))
        self.grid.nodes.pop(Node(node.x,node.y))
            
    def get_node(self,addr):
        for n in self.grid.nodes:
            if self.grid[n].address == addr:
                return self.grid[n]
        raise Exception("Node not found")
    
    def list_nodes(self):
        return [self.grid.nodes[n] for n in self.grid.nodes if type(self.grid.nodes[n]) == AgentNode]
            
    def visibility(self,node):
        '''Given a node as input, it returns a list of all visible nodes.
        Visibility is blocked by wallsself.
        The distance is evaluated as the number of steps between
        2 nodes'''
        cm,pth = self.grid.breadth_first(node)
        visibility_list = []
        for p in pth:
            
            if len(pth[p]) <= self.visibility_threshold and self.grid[p] != node:
                visibility_list.append((self.grid[p],len(pth[p])-1))
        return visibility_list

