#Still work in progress, just a tentative structure

class WirelessNode:

    def __init__(self,address):
        self.address = address
        #WiFi components
        #current SSID of this node
        self.ssid = ''
        #Visible access points
        self.aps = []
        #Packet input and output buffers
        self.message_in = []
        self.message_out = []


    def scan(self):
        '''scan the visible nodes to discover available networks
            if there are no available candidates'''
        for m in self.message_in:
            if m['type'] == 'beacon':
                ########################################################################
                RSSI = 0 
                #this must be computed from the world, 
                #I believe there should be a message class instead of using dictionaries
                ap = (m['ssid'],m['address'],RSSI)

    def send(self,message_queue):
        pass
    
    def receive(self,message_queue):
        pass

    def run(self,current_queue,next_queue,time_stamp):
        self.receive(current_queue)
        self.scan()
        self.send(next_queue)
    

        
