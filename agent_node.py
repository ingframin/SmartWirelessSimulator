from random import randint
from random import shuffle


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

        #associated nodes
        self.a_nodes = set()
        #max connections
        self.max_cons = 5

        #this indicates if the node is associated to a network
        self.current_ap = None

        #input message queue
        self.message_in = []

        #output message queue
        self.message_out = []

        #current timestamp
        self.timestamp = 0

        #candidate network for association
        self.candidates = []

        #ping message register
        self.pings = []

        #Message counter
        self.m_count = 0
        self.no_conns = 0
        self.bid = 0

    def scan(self,visibility_list):
        '''scan the visible nodes to discover available networks'''
        self.battery -= 0.25
        self.networks.clear()

        for v in visibility_list:

            if v[0].address in self.aps:
                self.networks.append((v[0].ssid,v[0].address,v[1]))

    def set_access_point(self,ssid):
        '''turn on access point mode'''
        self.battery -= 0.1
        self.is_ap = True
        self.ssid = ssid
        self.no_conns = 0
        self.a_nodes.clear()

    def set_station(self):
        '''turn on or reset station mode'''
        self.battery -= 0.1
        self.is_sta = True
        self.current_ap = None
        self.networks = []
        self.candidates = []

    def connect(self,network):
        '''when in station mode, connect to the network passed as parameter'''
        self.battery -= 0.1
        m = {'sender':self.address,'receiver':network[1],'type':'request','params':'connect'}
        self.message_out.append(m)

    def disconnect(self):
        '''disconnect from current network'''
        self.battery -= 0.1
        m = {'sender':self.address,'receiver':self.current_ap[0],'type':'request','params':'disconnect'}
        self.current_ap = None
        self.message_out.append(m)

    def process_connection(self,request):
        self.battery -= 0.1
        response = {'sender':self.address,'receiver':request['sender'],
                    'type':'response'}
        if len(self.a_nodes)<self.max_cons:
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
            self.battery -= 0.01
            if m['sender'] != self.address:
                pm['receiver'] = m['sender']
                pm['ping_ID'] = m['ID']
                self.message_out.append(pm)
        self.pings.clear()

    def react(self):
        '''Reactive part of the control loop'''
        self.aps.clear()
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
                    try:
                        self.candidates.pop()
                        print("candidates="+str(self.candidates))
                        self.connect(self.candidates[-1])
                    except:
                        print("candidates="+str(self.candidates))

            if m['type']=='beacon':
                self.aps.append(m['sender'])

            if m['type'] == 'solve_deadlock':
                if m['params'] > self.bid:
                    self.a_nodes.clear()
                    self.is_ap = False
                    self.no_conns = 0
                    self.set_station()

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
        bm = {'sender':self.address,'receiver':-1,'type':'beacon','SSID':self.ssid}
        self.message_out.append(bm)

    def execute(self,visibility_list):
        '''BDI part of the control loop'''
        if self.is_sta:
            #Intentions when in station mode

            if self.connected():

                if self.current_ap not in self.networks or self.current_ap[1] not in self.aps:
                    print("AP Disappeared!")
                    self.set_station()

            if not self.connected():
                #Here is where the selection criteria goes
                #Here there should be a function that selects the best criteria
                #depending on the configuration.
                #The same criterium is not always good. Sometimes it prolongs the life of the system, 
                #sometims it shortens it.
                #Apply strategy pattern. Find algorithm to select the strategy.
                
                if len(self.candidates)==0:
                    self.scan(visibility_list)
                    
                    for n in self.networks:
                        
                        if n[1] == self.address:
                            continue
                        self.candidates.append(n)
                        

                if len(self.candidates) > 0:
                    #shuffle(self.candidates)
                    #sorted(self.candidates, key=lambda x: x[2])
                    sorted(self.candidates)
                    self.connect(self.candidates[-1])

                else:
                    self.set_access_point('Node=%d'%self.address)

        if self.is_ap:
           
            self.send_beacon()
            #intentions when in AP mode
            if len(self.a_nodes) == 0:
                self.no_conns += 1

                if self.no_conns > 2:
                    self.a_nodes.clear()
                    self.is_ap = False
                    self.no_conns = 0
                    self.set_station()

        if self.is_ap and self.is_sta:
            if self.current_ap != None:
                pass

                #if len(self.a_nodes)==0 or (len(self.a_nodes)==1 and self.current_ap[1] in self.a_nodes) :
                if len(self.a_nodes)==0:
                #     # m = {'sender':self.address,'receiver':self.current_ap[-1]}
                #     # m['type'] = 'solve_deadlock'
                #     # self.bid = randint(0,255)
                #     # print(self.bid)
                #     # m['params']=self.bid
                #     #self.message_out.append(m)
                    self.a_nodes.clear()
                    self.is_ap = False
                    self.no_conns = 0
                    self.set_station()



    def run(self,message_queue,next_queue,visibility_list,timer):
        '''function to be called in the main loop'''
        self.timestamp = timer
        self.receive(message_queue)
        self.react()
        self.execute(visibility_list)
        self.send(next_queue)

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
