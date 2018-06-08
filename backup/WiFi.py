#Tests still missing :-/

from math import pi


class WiFi:
    '''Wi-Fi interface model.
    This is a simplified representation of all the states and operations
    associated with a WI-Fi adapter'''

    def __init__(self,mac):
        #unique ID for each node
        self.mac = mac
        #Network identifier when in AP mode
        self.ssid =""
        #Which modes are on?
        self.is_ap = False
        self.is_sta = False
        #Are we connected to something?
        self.connected = False
        #Access point to which the node is associated
        self.associated_ap = None
        #Associated nodes when access point is on
        self.associated_nodes = {}
        #Power managment stats
        self.battery_level = 100
        self.ap_op_power = 0.2
        self.sta_op_power = 0.1
        #Visible networks
        self.networks = {}
        #Packets buffer
        self.buffer = []
        #Errors buffer
        self.errors = []


    def __str__(self):
        s = ''
        s+='mac= '+str(self.mac)+'\n'
        s+='battery='+str(self.battery_level)+'\n'
        if self.is_ap:
            s+='ssid='+self.ssid+'\n'
            s+='associated nodes='+'\t'.join([str(n) for n in self.associated_nodes])
            s+='\n'
        else:
            s+='connected?'+str(self.connected)+'\n'
            print('----------------------------------')
            s+='associated to={\n'+str(self.associated_ap)+'\n}'
        return s

    def connect(self,ssid):
        '''Connects the node to the networke indicated by the SSID passed as parameter.
        Fails if the SSID is not in the list of visible networks or if the node station mode is off'''
        self.battery_level -= self.sta_op_power
        if self.is_sta:
            if ssid in self.networks:
                #self.networks[ssid][0] = pointer to the AP node
                #self.networks[ssid][1] = RSSI
                self.associated_ap = self.networks[ssid][0]
                self.associated_ap.associated_nodes[self.mac] = self
                print(self.associated_ap)
                self.connected = True
            else:
                self.errors.append("Network "+ssid+" not visible")
        else:
            self.errors.append("Node must be a station to connect to a network")

    def disconnect(self):
        '''Disconnects the node from the current network. It has no effect if the node is not connected to any network'''
        self.battery_level -= self.sta_op_power
        if self.is_sta:
            self.connected = False
            self.associated_ap = None
        else:
            self.errors.append("Node must be a station to disconnect from a network")

    def setAP(self,ssid):
        '''Start AP mode'''
        self.battery_level -= self.ap_op_power
        self.is_ap = True
        self.ssid = ssid

    def setSTA(self):
        '''Start station mode'''
        self.battery_level -= self.sta_op_power
        self.is_sta = True

    def turn_off_STA(self):
        '''Turns off station mode'''
        self.disconnect()
        self.battery_level -= self.sta_op_power
        self.is_sta = False

    def turn_off_AP(self):
        '''Start AP mode'''
        self.battery_level -= self.ap_op_power
        self.is_ap = False


    def scan(self,visible_nodes):
        '''visible_nodes= [(node,distance)]'''
        for n,d in visible_nodes:
            self.battery_level -= self.sta_op_power
            if n.is_ap:
                #Friis formula for normalized lambda
                rssi = 1E3/(4*pi*d)**2
                self.networks[n.ssid] = (n,rssi)

    def send(self,dest_mac,data):
        '''Send a packet to another node'''
        if self.is_sta:
            self.battery_level -= self.sta_op_power
            self.associated_ap.receive({'sender':self.mac,'dest':dest_mac,'data':data})
        if self.is_ap:

            if dest_mac in self.associated_nodes:
                self.battery_level -= self.ap_op_power
                self.associated_nodes[dest_mac].receive({'sender':self.mac,'dest':dest_mac,'data':data})
            else:
                '''Kind of MESH routing...'''
                self.battery_level -= self.ap_op_power
                aps = list(filter(lambda n: n.is_ap,self.associated_nodes))
                if len(aps) == 0:
                    self.errors.append("Impossible to deliver packet:"+str(data))
                for n in aps:
                    self.battery_level -= self.ap_op_power
                    if n.is_ap:
                        n.receive({'sender':self.mac,'dest':dest_mac,'data':data})



    def receive(self,packet):
        '''Receive a packet from another node'''
        self.buffer.append(packet)

if __name__ == '__main__':
    wifi0 = WiFi(0)
    wifi1 = WiFi(1)
    wifi2 = WiFi(2)
    wifi3 = WiFi(3)
    wifi4 = WiFi(4)
    wifi5 = WiFi(5)
    visible_list = []
    visible_list.append((wifi1,3))
    visible_list.append((wifi2,5))
    visible_list.append((wifi3,2))
    visible_list.append((wifi4,5))
    visible_list.append((wifi5,3))
    for node in visible_list:
        print(str(node[0]))
    print('----------------------------------')
    wifi5.setAP('test')
    wifi0.scan(visible_list)
    print(wifi0.networks)
    print('----------------------------------')
    wifi0.setSTA()
    wifi0.connect('test')
    print(wifi0)
    print('----------------------------------')
    
