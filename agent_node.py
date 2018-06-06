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
        self.aps = []
        #maximum nodes associated to this node
        self.max_connections = max_connections

        self.battery = 100.0

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
        self.candidates = []

        #ping message register
        self.pings = []
        #Message counter
        self.m_count = 0
        self.no_conns = 0

    def scan(self,visibility_list):
        '''scan the visible nodes to discover available networks'''
        self.battery -= 0.25
        self.networks.clear()

        for v in visibility_list:

            if v[0].address in self.aps:
                self.networks.append((v[0].ssid,v[0].address,v[1]))
        #print("Visible Networks = "+repr(self.networks))

    def set_access_point(self,ssid):
        '''turn on access point mode'''
        self.battery -= 0.1
        self.is_ap = True
        self.ssid = ssid
        self.no_conns = 0

    def set_station(self):
        '''turn on or reset station mode'''
        self.battery -= 0.1
        self.is_sta = True
        self.current_ap = None
        self.networks = []
        self.candidates = []

    def connect(self,network):
        m = {'sender':self.address,'receiver':network[1],'type':'request','params':'connect'}
        self.message_out.append(m)

    def disconnect(self):
        m = {'sender':self.address,'receiver':self.current_ap[0],'type':'request','params':'disconnect'}
        self.current_ap = None
        self.message_out.append(m)

    def process_connection(self,request):
        self.battery -= 0.1
        response = {'sender':self.address,'receiver':request['sender'],
                    'type':'response'}

        if len(self.a_nodes)<self.max_connections:
            self.a_nodes.add(request['sender'])
            response['params']='accept'
        else:
            response['params']='refuse'
        if self.current_ap != None:
            if self.current_ap[1] in self.a_nodes:
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

    def process_input(self):
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
                        print("Current AP="+str(self.current_ap))
                if m['params']=='refuse':
                    self.current_ap = None

            if m['type']=='beacon':
                self.aps.append(m['sender'])

        #After input queue is processed, it can be = []ed
        self.message_in = []

    def send(self,message_queue):
        for m in self.message_out:
            self.battery -= 0.2
            m['ID'] = 'N{}-M{}'.format(self.address,self.m_count)
            m['timestamp'] = self.timestamp+1
            message_queue.append(m)
            # if m['type'] == 'ping':
            #     self.pings.append(m)
            self.m_count+=1
        #after sending, = [] output buffer
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
        bm = {'sender':self.address,'receiver':-1,'type':'beacon','SSID':self.ssid}
        self.message_out.append(bm)

    def execute(self,visibility_list):
        if self.is_sta:
            self.scan(visibility_list)
            if self.connected():
                #print("Connected to "+repr(self.current_ap))
                if self.current_ap not in self.networks:
                    print("AP Disappeared!")
                    self.set_station()

            if not self.connected():

                if len(self.candidates)==0:

                    min_dist = 100
                    for n in self.networks:
                        #connect to closest access point
                        if n[1] == self.address:
                            continue
                        if n[2] < min_dist:
                            self.candidates.append(n)



                if len(self.candidates) > 0:
                    self.connect(self.candidates[-1])

                else:
                    self.set_access_point('Node=%d'%self.address)


        if self.is_ap:
            self.send_beacon()
            if len(self.a_nodes) == 0:
                self.no_conns += 1


            if self.no_conns > 3:
                self.is_ap = False
                self.no_conns = 0
                self.set_station()

            if self.current_ap != None:
                if self.current_ap[1] in self.a_nodes:
                    try:
                        self.a_nodes.remove(self.current_ap)
                    except:
                        pass

            #ping nodes to see if they are there
            # for n in self.a_nodes:
            #     self.ping(n)
            #
            # my_pings = [p['ID'] for p in filter(lambda m: m['sender']==self.address,self.pings)]
            # for pm in self.pings:
            #     if pm['type'] == 'pong' and pm['ping_ID'] in my_pings:
            #         self.a_nodes.add(pm['sender'])
            #         my_pings.remove(pm['ping_ID'])
            #
            # self.pings = list(filter(lambda m: m['ID'] in my_pings or m['sender'] != self.address, self.pings))
            # #print("remaining pings ="+str(len(self.pings)))


    def run(self,message_queue,next_queue,visibility_list,timer):
        '''function to be called in the main loop'''
        self.timestamp = timer
        self.receive(message_queue)
        self.process_input()
        self.execute(visibility_list)
        self.send(next_queue)

    def connected(self):
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


#############################################  Test  #########################################################
if __name__=='__main__':
    message_queue = []
    next_queue = []
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
        print(message_queue)
        print('---------------------------------------------')
        ag1.run(message_queue,next_queue,vlist,timer)
        print('agent 1:')
        print(ag1.message_in)
        print(ag1.message_out)

        print('connected= {}'.format(ag1.connected()))
        print('nodes: '+str(ag1.a_nodes))
        ag2.run(message_queue,next_queue,vlist,timer)
        print('agent 2:')
        print(ag2.message_in)
        print(ag2.message_out)
        print('connected= {}'.format(ag2.connected()))
        print('nodes: '+str(ag2.a_nodes))
        ag3.run(message_queue,next_queue,vlist,timer)
        print('agent 3:')
        print(ag3.message_in)
        print(ag3.message_out)
        print('connected= {}'.format(ag3.connected()))
        print('nodes: '+str(ag3.a_nodes))
        timer+=1
        message_queue = next_queue.copy()
        next_queue.clear()

        input()
