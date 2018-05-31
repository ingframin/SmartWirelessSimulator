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
        self.a_nodes = set()

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

        #ping message register
        self.pings = []
        #Message counter
        self.m_count = 0
        
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
            self.a_nodes.add(request['sender'])
            response['params']='accept'
        else:
            response['params']='refuse'

        self.message_out.append(response)

    def ping(self,addr):
        '''check if another node is reachable'''
        pm = {'sender':self.address,'receiver':addr,'type':'ping'}
        self.message_out.append(pm)

    def pong(self):
        '''answer to ping'''
        pm = {'sender':self.address, 'type':'pong'}
        for m in self.pings:
            if m['sender'] != self.address:
                pm['receiver'] = m['sender']
                pm['ping_ID'] = m['ID']  
                self.message_out.append(pm)
            
    def process_input(self):
        for m in self.message_in:
            
            if m['type'] == 'request':
                if m['params']=='connect':
                    self.process_connections(m)
                
            if m['type'] == 'response':
                if m['params']=='accept':
                    self.current_ap = self.candidate

            if m['type'] == 'ping':
                self.pings.append(m)
                self.pong()
                
                
            if m['type'] == 'pong':
                for p in self.pings:
                    if p['receiver'] == m['sender']:
                        self.pings.remove(p)
        #After input queue is processed, it can be cleared
        self.message_in.clear()
   
    def send(self,message_queue):
        for m in self.message_out:
            m['ID'] = 'N{}-M{}'.format(self.address,self.m_count)
            m['timestamp'] = self.timestamp+1
            message_queue.append(m)
            if m['type'] == 'ping':
                self.pings.append(m)
            self.m_count+=1
            
        #after sending, clear output buffer
        self.message_out.clear()

    def receive(self,message_queue):
        '''reads in all the messages in message_queue directed to this node and puts them into message_in''' 
        self.message_in.clear()
        
        for i in range(len(message_queue)):
            m = message_queue[i]
            if m['receiver'] == self.address and m['timestamp']==self.timestamp:
                self.message_in.append(m)
     
    def deliberate(self,visibility_list):
        if self.is_sta:

            if not self.connected():
                
                self.scan(visibility_list)
                min_dist = 100
                self.candidate = None
                for n in self.networks:
                    #connect to closest access point
                    if n[1] == self.address:
                        continue
                    if n[2] < min_dist:
                        self.candidate = n
                        
                if self.candidate is not None:
                    self.connect(n)

                else:
                    self.set_access_point('Node=%d'%randint(0,256))
                
        if self.is_ap:
            #ping nodes to see if they are there
            for n in self.a_nodes:
                self.ping(n)

            my_pings = [p['ID'] for p in filter(lambda m: m['sender']==self.address,self.pings)]
            for pm in self.pings:
                if pm['type'] == 'pong' and pm['ping_ID'] in my_pings:
                    self.a_nodes.add(pm['sender'])
                    my_pings.remove(pm['ping_ID'])

            self.pings = list(filter(lambda m: m['ID'] in my_pings or m['sender'] != self.address, self.pings))
            print("remaining pings ="+str(len(self.pings)))
                    

    def run(self,message_queue,visibility_list,timer):
        '''function to be called in the main loop'''
        self.timestamp = timer
        self.receive(message_queue)
        self.process_input()
        self.deliberate(visibility_list)
        self.send(message_queue)

    def connected(self):
        return self.current_ap != None
    
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
    ag1 = AgentNode(0,0,0)
    ag1.set_station()
    ag2 = AgentNode(1,1,1)
    ag2.set_station()
    ag3 = AgentNode(2,2,2)
    ag3.set_station()
    vlist = [(ag2,3),(ag3,2),(ag1,2)]
    while True:
        print('---------------------------------------------')
        ag1.run(message_queue,vlist,timer)
        print('agent 1:')
        print(ag1.message_in)
        print(ag1.message_out)
        
        print('connected= {}'.format(ag1.connected()))
        print('nodes: '+str(ag1.a_nodes))
        ag2.run(message_queue,vlist,timer)
        print('agent 2:')
        print(ag2.message_in)
        print(ag2.message_out)
        print('connected= {}'.format(ag2.connected()))
        print('nodes: '+str(ag2.a_nodes))
        ag3.run(message_queue,vlist,timer)
        print('agent 3:')
        print(ag3.message_in)
        print(ag3.message_out)
        print('connected= {}'.format(ag3.connected()))
        print('nodes: '+str(ag3.a_nodes))
        message_queue = list(filter(lambda m: m['timestamp'] > timer, message_queue))
        timer+=1
        input()
    
