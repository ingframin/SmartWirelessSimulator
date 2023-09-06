from typing import Optional
from enum import Enum

class NodeType(Enum):
    Empty = '_' 
    Wall = 'W'
    


class Node:
    
    def __init__(self,x:int, y:int, node_type: NodeType) -> None:
        self.x = x
        self.y = y
        self.type = node_type
    
    def __eq__(self, n) -> bool:
        return self.x == n.x and self.y == n.y
    
    def is_neighbor(self, n)->bool:
        return abs(n.x-self.x) == 1 or abs(self.y-n.y)==1
    
    def __repr__(self) -> str:
        return f'{self.type} Node {self.id}: {self.x},{self.y}'
    
    
class Grid:
    def __init__(self) -> None:
        self.nodes = set()
        
    def add_node(self,node:Node)->None:
        self.nodes.add(node)

    def get_node(self, x:int, y:int)->Node:
        for n in self.nodes:
            if n.x == x and n.y == y:
                return n
            
        return Node(x,y)
    
    def path(self, start:Node, stop:Node)->list[Node]:
        pass
