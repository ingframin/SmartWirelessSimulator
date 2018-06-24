from access_point import *
from station import *

'''
Staus report is a dictionary with the following fields:
station : bool
    connected : bool
    current AP : string
    visible nets : [Network]
access point : bool
    ssid : string
    connections : [int]

pending requests : [Message]
pending responses : [Message]
'''


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

    def report_status(self):
        status = {}
        status['station'] = self.station != None
        status['access point'] = self.access_point != None
        
        if status['station']:
            status['connected'] = self.station.connected()
            status['current AP'] = str(self.station.current_ap)
            status['visible nets'] = self.station.networks

        if status['access point']:
            status['ssid'] = self.access_point.ssid
            status['connections'] = self.access_point.a_nodes.copy()    