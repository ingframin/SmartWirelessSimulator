class StationComponent:
    
    def __init__(self):
        #available networks
        self.networks = []
        #this indicates if the node is associated to a network
        self.current_ap = None
        self.wait_response = False
        

    def scan(self, visible_aps):
        '''Adds the visible access points to the available network list.
        Each ap is represented as a dictionary with 3 fields:
        - ssid
        - address
        - distance
        it's up to the AgentNode to remove its address'''

        self.networks.clear()

        for v in visible_aps:

            self.networks.append((v['ssid'], v['address'], v['distance']))

    def connection_request(self):
        '''tries to connect to all avilable networks'''
        request = {'receiver':self.networks[-1],'type':'request','params':'connect'}
        self.wait_response = True
        return request
    
    def connection_response(self,response):
        
        if response['params']=='accept':
            self.current_ap = self.networks[-1]
            self.wait_response = False
            return
        else:
            self.wait_response = False
            self.networks.pop()

    
    def connected(self):
        return self.current_ap != None