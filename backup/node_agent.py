from threading import *
from node import *
from random import randint
from time import sleep

class NodeAgent(Thread):

    def __init__(self,id=0,x=0,y=0):
        Thread.__init__(self)
        self.stop_event = Event()
        self.ID = id
        self.node = Node(id,x,y)
        self.strategies = {}
        self.goals = []
        self.env = {}

    
    def sense(self):
 #       self.node.scan_networks(self.env['nodes'])
         print(self.env)
        

    def deliberate(self):
        '''select the appropriate strategy towards the desired goal'''
        pass

    def act(self):
        '''execute selected strategy,
            if it doesn't work, chose another one'''
        pass
        
    
    def run(self):
        while not self.stop_event.is_set():
            print("Node ID= "+str(self.ID))
            self.sense()
            self.deliberate()
            self.act()
            sleep(0.5)


    def stop(self):
        self.stop_event.set()

    def set_env(self,env):
        self.env = env

    
if __name__=='__main__':
    n = NodeAgent()
    n.start()
    sleep(5)
    n.set_env({'prova':123})
    sleep(5)
    n.stop()
    
    n.join()
    
    
    
