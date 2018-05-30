from collections import deque
from random import randint

class AgentNode:
    '''Base class for node agents'''
    def __init__(self,address=0, x=0, y=0, max_connections=5):
        self.address = address
        #node position
        self.x = x
        self.y = y
        #available networks
        self.networks = []
        #maximum nodes associated to this node
        self.max_connections = max_connections

        #Mode: is_ap = Access Point;is_sta = Station
        #they can be true at the same time        
        self.is_ap = False
        self.is_sta = False
        self.ssid = ''

        #associated nodes
        self.a_nodes = []

        #this indicates if the node is associated to a network
        self.current_ap = None
        
        #input message queue
        self.message_in = []
        #output message queue
        self.message_out = []

        #current timestamp
        self.timestamp = 0
        
        #candidate network for association
        self.candidate = None

    def scan(self,visibility_list):
        '''scan the visible nodes to discover available networks'''
        for v in visibility_list:
            if v[0].is_ap:
                self.networks.append((v[0].ssid,v[0].address,v[1]))

    def set_access_point(self,ssid):
        '''turn on access point mode'''
        self.is_ap = True
        self.ssid = ssid

    def set_station(self):
        '''turn on or reset station mode''' 
        self.is_sta = True
        self.current_ap = None
        self.networks.clear()
        self.candidate = None

    def connect(self,network):

        m = {'sender':self.address,'receiver':network[1],'type':'request','params':'connect'}
        self.message_out.append(m)

    def disconnect(self):
        m = {'sender':self.address,'receiver':self.current_ap[0],'type':'request','params':'disconnect'}
        self.current_ap = None
        self.message_out.append(m)

    def process_connections(self,request):
        response = {'sender':self.address,'receiver':request['sender'],
                    'type':'response'}

        if len(self.a_nodes)<self.max_connections:
            self.a_nodes.append(request['sender'])
            response['params']='accept'
        else:
            response['params']='refuse'

        self.message_out.append(response)

    def process_input(self):
        for m in self.message_in:
            
            if m['type'] == 'request':
                if m['params']=='connect':
                    self.process_connections(m)
                
            if m['type'] == 'response':
                if m['params']=='accept':
                    self.current_ap = self.candidate
   
    def send(self,message_queue):
        for m in self.message_out:
            m['timestamp'] = self.timestamp
            message_queue.append(m)

    def receive(self,message_queue):
        received_indexes = []
        for i in range(len(message_queue)):
            m = message_queue[i]
            if m['receiver'] == self.address:
                self.message_in.append(m)
        
                
    
    def deliberate(self,visibility_list):
        if self.is_sta:
            if self.current_ap is not None:
                return
            else:
                self.scan(visibility_list)
                min_dist = 100
                self.candidate = None
                for n in self.networks:
                    if n[2] < min_dist:
                        self.candidate = n
                if self.candidate is not None:
                    self.connect(n)
                else:
                    self.set_access_point('Node=%d'%randint(0,256))

    def run(self,message_queue,visibility_list,timer):
        '''function to be called in the main loop'''
        self.timestamp = timer
        self.receive(message_queue)
        self.process_input()
        self.deliberate(visibility_list)
        self.send(message_queue)

    def __eq__(self,n):
        return self.__hash__() == n.__hash__()

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return 'Agent: address=%d, x=%d, y=%d'%(self.address,self.x,self.y)

    def __str__(self):
        return 'A'


#############################################  Test  #########################################################
if __name__=='__main__':
    message_queue = []
    timer = 0
    ag1 = AgentNode()
    ag1.is_sta = True
    ag2 = AgentNode(1,1,1)
    ag3 = AgentNode(2,2,2)
    ag2.set_access_point('test')
    vlist = [(ag2,3),(ag3,2)]
    ag1.scan(vlist)
    print(ag1.networks)
    print('---------------------------------------------')
    ag1.run(message_queue,vlist,timer)
    ag2.run(message_queue,vlist,timer)
    
    timer+=1
    for m in message_queue:
        if m['timestamp'] < timer:
            del(m)
    print(message_queue)
    print('---------------------------------------------')
    ag1.run(message_queue,vlist,timer)
    ag2.run(message_queue,vlist,timer)
    timer+=1
    for m in message_queue:
        if m['timestamp'] < timer:
            message_queue.remove(m)
    print(message_queue)
    print('---------------------------------------------')
