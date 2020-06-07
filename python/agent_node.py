# -*- coding: utf-8 -*-
from random import randint,shuffle

class AgentNode:
    '''Base class for node agents'''
    def __init__(self,address=0, x=0, y=0):
        self.address = address
        #node position
        self.x = x
        self.y = y

        #available networks
        self.networks = []
        self.aps = []
        #Battery level
        self.battery = 100.0

        #Mode: is_ap = Access Point;is_sta = Station
        #they can be true at the same time
        self.is_ap = False
        self.is_sta = False
        self.ssid = ''
        self.wait = False
        self.timeout = 0

        #associated nodes
        self.a_nodes = set()
        #max connections
        self.max_cons = 7

        #this indicates if the node is associated to a network
        self.current_ap = None

        #input message queue
        self.message_in = []

        #output message queue
        self.message_out = []

        #current timestamp
        self.timestamp = 0
        self.rand_timer = randint(2,5)

        #candidate network for association
        self.candidates = []

        #ping message register
        self.pings = []

        #Message counter
        self.m_count = 0
        self.no_conns = 0
        #Strategies variables 
        self.bid = 0
        self.strategy = 0        

    def scan(self,visibility_list):
        '''scan the visible nodes to discover available networks
            if there are no available candidates'''
        if len(self.candidates)>0:
            return
        self.battery -= 0.25
        self.networks.clear()

        for v in visibility_list:

            if v[0].address in self.aps:
                self.networks.append((v[0].ssid,v[0].address,v[1]))
                
        for n in self.networks:
                        
            if n[1] == self.address:
                continue
            self.candidates.append(n)

    def set_access_point(self,ssid):
        '''turn on access point mode'''
        self.battery -= 0.1
        self.is_ap = True
        self.ssid = ssid
        self.no_conns = 0
        self.a_nodes.clear()
        self.wait = False
        self.timeout = 0
        

    def set_station(self):
        '''turn on or reset station mode'''
        self.battery -= 0.1
        self.is_sta = True
        self.current_ap = None
        self.networks = []
        self.candidates = []
        self.wait = False
        self.timeout = 0
        self.rand_timer = randint(2,5)
        
    def connect(self,network):
        '''when in station mode, connect to the network passed as parameter'''
        self.battery -= 0.1
        m = {'sender':self.address,'receiver':network[1],'type':'request','params':'connect'}
        self.message_out.append(m)
        self.wait = True
        self.timeout = self.timestamp

    def disconnect(self):
        '''disconnect from current network'''
        self.battery -= 0.1
        m = {'sender':self.address,'receiver':self.current_ap[0],'type':'request','params':'disconnect'}
        self.current_ap = None
        self.message_out.append(m)
        self.wait=False
        self.timeout = 0
        
    def process_connection(self,request):
        self.battery -= 0.1
        response = {'sender':self.address,'receiver':request['sender'],
                    'type':'response'}
        if len(self.a_nodes) == self.max_cons:
            response['params']='refuse'
        elif self.current_ap is not None and request['sender'] == self.current_ap[1]:
            response['params']='refuse'
            
        else:
            self.a_nodes.add(request['sender'])
            response['params']='accept'
            

        self.message_out.append(response)

    def ping(self,addr):
        '''check if another node is reachable'''
        pm = {'sender':self.address,'receiver':addr,'type':'ping'}
        self.message_out.append(pm)

    def pong(self):
        '''answer to ping'''
        pm = {'sender':self.address, 'type':'pong'}
        for m in self.pings:
            self.battery -= 0.01
            if m['sender'] != self.address:
                pm['receiver'] = m['sender']
                pm['ping_ID'] = m['ID']
                self.message_out.append(pm)
        self.pings.clear()

    def react(self):
        '''Reactive part of the control loop'''
                
        for m in self.message_in:
            self.battery -= 0.01
            if m['type'] == 'ping':
                self.pings.append(m)
                self.pong()

            if m['type'] == 'pong':
                for p in self.pings:
                    if p['receiver'] == m['sender']:
                        self.pings.remove(p)

            if m['type'] == 'request':
                if m['params']=='connect':
                    self.process_connection(m)
                    

            if m['type'] == 'response':
                if m['params']=='accept':
                    try:
                        self.current_ap = self.candidates[-1]
                    except:
                        print('---no candidates available for connection---')
                if m['params']=='refuse':
                    self.strategy = randint(0,3)
                    try:
                        self.candidates.pop()
                        print("candidates="+str(self.candidates))
                    except:
                        print("candidates="+str(self.candidates))
                self.wait = False
                self.timeout = 0
            if m['type']=='beacon':
                
                self.aps.append(m['sender'])

        self.message_in = []

    def send(self,message_queue):
        '''flush output queue'''
        for m in self.message_out:
            self.battery -= 0.2
            m['ID'] = 'N{}-M{}'.format(self.address,self.m_count)
            m['timestamp'] = self.timestamp+1
            message_queue.append(m)
            self.m_count+=1
        #Clean up output queue
        self.message_out = []


    def receive(self,message_queue):
        '''reads in all the messages in message_queue directed to this node and puts them into message_in
        -1 is the broadcast address!!!'''

        self.message_in = []

        for i in range(len(message_queue)):
            self.battery -= 0.2
            m = message_queue[i]
            if (m['receiver'] == self.address or m['receiver']== -1):
                self.message_in.append(m)

    def send_beacon(self):
        '''When in AP mode, broadcast the SSID'''
        bm = {'sender':self.address,'receiver':-1,'type':'beacon','SSID':self.ssid,'associated nodes':len(self.a_nodes),'free slots':self.max_cons-len(self.a_nodes)}
        self.message_out.append(bm)

    def execute(self,visibility_list):
        
        if self.wait:
            return
        for v in visibility_list:
            #this is a hackish fix to the connection bug.
            #for some reason, nodes do not detect when they are connected
            if self.address in v[0].a_nodes:
                self.current_ap = (v[0].ssid,v[0].address,v[1])
        
            
        if self.is_sta:
            #Intentions when in station mode
            self.scan(visibility_list)
            if self.connected():
                if self.current_ap[1] in self.a_nodes:
                    self.set_station()

                if self.current_ap not in self.networks or self.current_ap[1] not in self.aps:
                    print("AP Disappeared!")
                    self.set_station()
 
            else:
                #Access point selection                
                
                if len(self.candidates) > 0:
                    #Select strategy
                    if self.strategy == 0:
                        #The SSID with the highest number wins
                        self.bidding()
                        self.strategy = 1
                        
                    elif self.strategy == 1:
                        #The closest network wins
                        self.closest()
                        self.strategy = 2
                        
                    elif self.strategy == 2:
                        #A random network is selected
                        self.random()
                        self.strategy = 0

                    self.connect(self.candidates[-1])
                    
                elif self.rand_timer == 0:
                    #SSID random number - connect to the highest SSID
                    self.set_access_point('Node=%d'%randint(0,256))
                    self.rand_timer = randint(2,5)
                    
        if self.is_ap:
           
            self.send_beacon()
            
            if len(self.a_nodes) == 0:
                self.no_conns += 1
                #if no one connects, AP mode goes off
                if self.no_conns > 3:
                    self.a_nodes.clear()
                    self.is_ap = False
                    self.no_conns = 0          


    def run(self,message_queue,next_queue,visibility_list,timer):
        '''function to be called in the main loop'''
        self.timestamp = timer
        if self.timestamp-self.timeout > 3:
            self.timeout = 0
            self.wait = False
        self.rand_timer -= 1
        self.receive(message_queue)
        self.react()
        self.execute(visibility_list)
        self.send(next_queue)
        self.aps.clear()

    def connected(self):
        '''is the node connected?'''
        return self.current_ap != None

    def __eq__(self,n):
        return self.__hash__() == n.__hash__()

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return 'Agent: address=%d, x=%d, y=%d'%(self.address,self.x,self.y)

    def __str__(self):
        if self.is_ap and self.is_sta:
            return 'H'
        if self.is_sta and not self.is_ap:
            return 'S'
        return 'A'

    def closest(self):
        self.candidates.sort(key=lambda x: x[2])
        self.candidates.reverse()
        

    def random(self):
        shuffle(self.candidates)
        

    def bidding(self):
        max_ssid = 0
        index = 0
        final_index = 0
        for c in self.candidates:
            n = int(c[0].split('=')[1])
            if n > max_ssid:
                max_ssid = n
                final_index = index
            index += 1
        self.candidates.append(self.candidates[final_index])
        
        
