from wireless import *

class Agent:
    def __init__(self,id,position,current_status):
        self.id = id
        self.position = position
        self.current_status = {}
        self.current_time = 0
        self.wireless = WirelessComponent(id)
    
    def _process_input(self,queue):
        self.wireless.receive(queue)
    
    def _process_output(self,queue):
        self.wireless.send(queue)

    def run(self,time_stamp,current_queue,next_queue,visibility):
        self._process_input(current_queue)
        #here goes my elaboration
        self._process_output(next_queue)
    