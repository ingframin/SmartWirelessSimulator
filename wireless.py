from access_point import *
from station import *

class WirelessComponent:

    def __init__(self,MAC, max_connections = 5):
        self.mac = MAC
        self.station = StationComponent()
        self.access_point = AccessPointComponent('',max_connections)
        self.input_queue = []
        self.output_queue = []

    def send(self, queue):
        for m in self.output_queue:
            queue.append(m)
        
        self.output_queue.clear()
    
    def receive(self,queue):
        self.input_queue.clear()
        for m in queue:
            if m['receiver'] == self.mac:
                self.input_queue.append(m)
