# -*- coding: utf-8 -*-
from node import Node,WallNode
from agent_node import AgentNode
from itertools import product

class Grid:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.nodes = {}

    def __getitem__(self,coord):
        if coord.x >= self.width or coord.x <0:
            print("x= %d y=%d"%(coord.x,coord.y))
            raise IndexError("x coordinate out of bounds: x= %d"%coord.x)
        if coord.y >= self.height or coord.y <0:
            print("x= %d y=%d"%(coord.x,coord.y))
            raise IndexError("y coordinate out of bounds: y= %d"%coord.y)

        if coord in self.nodes:
            return self.nodes[coord]
        else:
            return None

    def __setitem__(self,coord,node):
        if coord.x >= self.width or coord.x <0:
            print("x= %d y=%d"%(coord.x,coord.y))
            raise IndexError("x coordinate out of bounds: x= %d"%coord.x)
        if coord.y >= self.height or coord.y <0:
            print("x= %d y=%d"%(coord.x,coord.y))
            raise IndexError("y coordinate out of bounds: y= %d"%coord.y)
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
        neighbors.remove(node)
        return neighbors

    def breadth_first(self, start):
        '''Finds minimum path between start
        node and all other nodes'''

        frontier = []
        frontier.append(start)
        agents = []
        paths = {}
        came_from = {}
        came_from[start] = None

        while len(frontier) > 0:
            
            current = frontier.pop(0)
            neighbors = self.compute_neighbors(current)
            for node in neighbors:

                if  node not in came_from and (type(self[node])!= WallNode):
                    frontier.append(node)
                    if type(self[node])==AgentNode:
                        agents.append(node)

                    came_from[node]=current
        #Should this be computed here or should only came_from be returned?
        for a in agents:
            step = a
            paths[a] = []
            steps = 0
            
            while step is not None:
                
                step = came_from[step]
                paths[a].append(step)
                steps+=1
 
        return paths