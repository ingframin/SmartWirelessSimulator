from abc import ABC
from typing import Self
from math import sqrt
from enum import Enum,auto
from collections import deque

class WirelessState(Enum):
    IDLE = auto()
    TX = auto()
    RX = auto()


class Node(ABC):
    node_ids = 0

    def __init__(self, x=0, y=0):
        super().__init__()
        self._id = Node.node_ids
        Node.node_ids += 1
        self._x = x
        self._y = y
    
    def position(self)->tuple[int,int]:
        return (self._x,self._y)
    
    def id(self):
        return self._id
    
    def distance(self,n:Self)->float:
        npx,npy = n.position()
        return sqrt((self._x-npx)**2 + (self._y-npy)**2)
    
     

    
class WallNode(Node):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        #TODO: Maybe add texture for visualisation?
    
class WirelessNode(Node):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.battery = 100.0 #battery percentage
        self.current_state = WirelessState.IDLE    
        self.msgq = deque()

    def tx(self,queue:deque)->None:
        queue.append(self.id())

    def rx(self,queue)->None:
        for m in queue:
            self.msgq.append(m.copy())


if __name__ == "__main__":
    wn = WallNode()
    print(wn.position())
    
