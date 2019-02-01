# -*- coding: utf-8 -*-
from agent_node import AgentNode
from config_parser import *
from node import *
from grid import *

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
        if type(self.grid[node]) in (WallNode,AgentNode):
            raise Exception("Cell already occupied!")
        self.grid[node] = node

    def kill_node(self,node):
        print(repr(self.grid.nodes[node]))
        self.grid.nodes.pop(node)
            
    def get_node(self,addr):
        for n in self.grid.nodes:
            if self.grid[n].address == addr:
                return self.grid[n]
        raise Exception("Node not found")
    
    def list_nodes(self):
        return [self.grid.nodes[n] for n in self.grid.nodes if type(self.grid.nodes[n]) == AgentNode]
            
    def visibility(self,node):
        '''Given a node as input, it returns a list of all visible nodes.
        Visibility is blocked by walls.
        The distance is evaluated as the number of steps between
        2 nodes'''
        cm,pth = self.grid.breadth_first(node)
        visibility_list = []
        for p in pth:
            
            if len(pth[p]) <= self.visibility_threshold and self.grid[p] != node:
                visibility_list.append((self.grid[p],len(pth[p])-1))
        return visibility_list

