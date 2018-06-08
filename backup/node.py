from math import sqrt
from threading import *
import time

modes = ('STA', 'AP', 'AP_STA')

def distance(node1,node2):
    return sqrt((node1.x-node2.x)**2 + (node1.y-node2.y)**2)

class Node:
    '''This class represents the hardware node'''
    def __init__(self,ID, x=0, y=0):
        
        self.ID = ID
        self.mode = 'STA'
        self.visible_nets = {}
        self.rssi_threshold = 10
        self.gain = 1
        self.x = x
        self.y = y
        self.ssid = ''
        self.associated_nodes = set()
        self.associated_net = ''
        self.running = True
        
        
    def set_mode(self, mode,ssid=''):
        '''mode must be within the available modes:
            "STA" for a WiFi station
            "AP" for a WiFi access point
            "AP_STA" for both
        '''
        if mode in ('AP','AP_STA'):
            self.ssid = ssid

        if mode == 'STA':
            self.ssid = ''
        self.mode = mode
        

    def scan_networks(self,nodes):
        for n in filter(lambda n: n.mode in ('AP','AP_STA'), nodes):
            
            rssi = self.rssi(n)
            if rssi > self.rssi_threshold:
                self.visible_nets[n.ssid] = (n,rssi)

    def rssi(self,node):
        return 100*node.gain*self.gain/(distance(self,node))

    def set_ssid(self,ssid):
        if self.mode in ('AP','AP_STA'):
            self.ssid = ssid
        else:
            print("A node must have access point capabilities to have an SSID")

    
    def associate(self,node):
        self.associated_nodes.add(node)

    def deassociate(self,node):
        self.associated_nodes.remove(node)

    def connect(self, ssid):
        if ssid in self.visible_nets:
            self.associated_net = ssid
            self.visible_nets[ssid][0].associate(self)
        else:
            print("Impossible to associate to the required net")

    def disconnect(self):
        if self.associated_net != '':
            self.visible_nets[ssid][0].deassociate(self)
            self.associated_net = ''
    
   
    def __eq__(self,node):
        if self.ID == node.ID:
            return True
        return False
    
    def __hash__(self):
        return self.ID

    def __str__(self):
        s = ''
        s+= str(self.ID)+"\n"
        s+='mode='+self.mode+'\t'
        s+='x= %d, y= %d'%(self.x,self.y)+'\n'
        if self.mode=='AP' or self.mode=='AP_STA':
            s+='SSID='+self.ssid+'\n'
            s+=';'.join((str(s) for s in self.associated_nodes))+'\n'
        if self.mode == 'STA' or self.mode=='AP_STA':
            s+='Associated to ='+ self.associated_net+'\n'
        return s

