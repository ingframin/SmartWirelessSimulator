from math import sqrt,log10,pi
from random import gauss
#needs to be split in separate components
#and multiple classes

class Agent:
    def __init__(self,address):
        self.address = address
        self.ssid = ''
        self.ap = False
        self.sta = False
        self.current_ap = None

#This can be refined with breadth first search
def distance(coord1,coord2):
    return sqrt((coord1[0]-coord2[0])**2+(coord1[1]-coord2[1])**2)

#See chapter2 of "Wireless Communication" by Andrea Goldsmith
def rssi(d,gamma=2,psi=1,d0=10):
    return 20*log10(0.125/(4*pi*d0))-10*gamma*log10(d/d0)-gauss(0,3.65)

#message defined as tuple (sender,receiver,type,content)
#grid defined as dictionary {address,coordinates}
def scan(agent,messages,grid):
    visible_aps = []
    for m in messages:
        if 'beacon' in m:            
            d = distance(grid[agent.address],m[0])
            RSSI = rssi(d)
            if RSSI > -120:
                visible_aps.append(RSSI,m[3])
    return visible_aps

def best_rssi(visible_aps):
    return sorted(visible_aps,key=lambda t: t[0])

def highest_bid(visible_aps):
    return sorted(visible_aps,key=lambda t: t[1])
    

if __name__=='__main__':
    a1 = Agent(0)
    a2 = Agent(1)
    grid = {0:(3,4),1:(5,6)}
    d = distance(grid[0],grid[1])
    for d in range(10,200,10):
        pr = rssi(d)
        print("d= %f; RSSI= %f"%(d,pr))
        