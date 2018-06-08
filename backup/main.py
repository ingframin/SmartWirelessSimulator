from node import *
from random import randint
import time
from threading import Thread

SIZE = 100

class SmartWireless:

    def __init__(self):
        self.node_set = set()
        self.index = 0
        
    def spawn_node(self):
        self.node_set.add(Node(self.index,randint(0,100),randint(0,100)))
        self.index += 1
        
    def kill_node(self,idn = -1):
        if idn < 0:
            return self.node_set.pop()
        else:
            try:
                self.node_set.remove(Node(idn))
            except:
                print("Node not present")

    def size(self):
        return len(self.node_set)

    def nodes(self):
        return self.node_set
    
simulation = SmartWireless()
now = time.clock()
for tr in simulation.node_set:
    tr.start()
    
while True:
    simulation.spawn_node()
    

    if simulation.size()>SIZE:
        try:
            node = simulation.kill_node()
            node.running = False
            print("removed node = %d"%node.ID)
        except:
             pass   

    
     
    dt = time.perf_counter() - now
    
    if dt < 0.1:
        time.sleep(0.1-dt)
    now = time.perf_counter() 
