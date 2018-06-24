from itertools import product
from .config_parser import read_config
from .node import *
#Nodes do not share any parental/inheritance relations,
#I am relying on duck-typing



class Grid:
    ''' 
        Container object for nodes.
        It represents a bidimensional grid
    ''' 
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.nodes = {}

    def __getitem__(self,xy):
        '''
        input: (x,y) tuple
        output: Node object at coordinates x,y or an EmptyNode if x,y is empty
        errors: IndexError if x and/or y are out of bounds
        '''
        if xy[0] >= self.width or xy[0] <0:
            #print("x= %d y=%d"%(xy[0],xy[1]))
            raise IndexError("x coordinate out of bounds")
        if xy[1] >= self.height or xy[1] <0:
            #print("x= %d y=%d"%(xy[0],xy[1]))
            raise IndexError("y coordinate out of bounds")

        if xy in self.nodes:
            return self.nodes[xy]
        else:
            return EmptyNode(xy[0],xy[1])

    def __setitem__(self,xy,node):
        if xy[0] >= self.width or xy[0] <0:
            #print("x= %d y=%d"%(xy[0],xy[1]))
            raise IndexError("x coordinate out of bounds")
        if xy[1] >= self.height or xy[1] <0:
            #print("x= %d y=%d"%(xy[0],xy[1]))
            raise IndexError("y coordinate out of bounds")
        self.nodes[xy] = node

    def __str__(self):
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                if Node(x,y) in self.nodes:
                    s+= str(self.nodes[(x,y)])
                else:
                    s+='_'
            s+='\n'
        return s

    def remove(self,xy):
        if xy[0] >= self.width or xy[0] <0:
            #print("x= %d y=%d"%(xy[0],xy[1]))
            raise IndexError("x coordinate out of bounds")
        if xy[1] >= self.height or xy[1] <0:
            #print("x= %d y=%d"%(xy[0],xy[1]))
            raise IndexError("y coordinate out of bounds")
        try:
            self.nodes.pop(xy)
        except KeyError:
            pass

    def _compute_neighbors(self, node):

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

    def search(self, start):
        '''Finds minimum path between start
        node and all other agent nodes'''

        frontier = []
        frontier.append(start)
        agents = []
        paths = {}
        came_from = {}
        came_from[start]=None

        while len(frontier) > 0:
            
            current = frontier.pop(0)
            neighbors = self._compute_neighbors(current)
            for node in neighbors:

                if  node not in came_from and (type(self[(node.x,node.y)])!= WallNode):
                    frontier.append(node)
                    if type(self[(node.x,node.y)])==AgentNode:
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
 
        return paths

class World:

    def __init__(self,width=10, height=10, v_threshold = 3):
        self.grid = Grid(width,height)
        self.width = width
        self.height = height
        self.visibility_threshold = v_threshold
        self.agents = {}

    def __str__(self):
        return str(self.grid)

    def config(self, config):
        '''
        Config is an iterable that contains 3 fields:
        - world dictionary
        - agents list
        - walls list
        '''

        world,agents,walls = config
        #load world parameters
        self.width = world['width']
        self.height = world['height']
        self.visibility_threshold = world['v_threshold']
        self.grid = Grid(width=self.width,height=self.height)

        #Load agent nodes
        for ag in agents:
            self.add_node(AgentNode(x=ag['x'], y=ag['y'],id=ag['mac']))
            
        #Load walls
        for wl in walls:
            self.add_node(WallNode(x=wl['x'], y=wl['y']))


    def add_node(self,node):
        if type(self.grid[(node.x,node.y)]) != EmptyNode:
            raise Exception("Cell already occupied")
        if type(node) == AgentNode:
            self.agents[node.id] = node

        self.grid[(node.x,node.y)] = node

    def kill_node(self,node):
        self.grid[(node.x,node.y)] = EmptyNode(node.x,node.y)
        if type(node) == AgentNode:
            self.agents.pop(node.id)
            
    def get_node(self,addr):
        if addr in self.agents:
            return self.agents[addr]
            
        raise Exception("Node not found")
    
    def list_nodes(self):
        return self.agents.values()
            
    def visibility(self,node):
        '''Given a node as input, it returns a list of all visible nodes.
        Visibility is blocked by wallsself.
        The distance is evaluated as the number of steps between
        2 nodes'''
        pth = self.grid.search(node)
        visibility_list = []
        for p in pth:
            
            if len(pth[p]) <= self.visibility_threshold and self.grid[(p.x,p.y)] != node:
                visibility_list.append((self.grid[(p.x,p.y)],len(pth[p])-1))
        return visibility_list

