from world import *
from agent_node import *
from random import randint,shuffle
from time import gmtime, strftime
import sys

class Simulation:

    def __init__(self,config_file):
        self.current_time = 0
        self.running = True
        self.current_queue = []
        self.next_queue = []
        self.wrld = World()
        self.wrld.load(config_file+'.cfg')
        self.log = []
    
    def run(self):
        
        while self.running:
            nodes = wrld.list_nodes()
            if len(nodes)==0:
                break
    
            for n in nodes:
                node_vis[n.id]=wrld.visibility(n.position)
                n.run(self.current_time, self.current_queue,self.next_queue,node_vis[n.address])
        
                
                if n.battery <= 0:
                    wrld.kill_node(n)

                self.current_queue = self.next_queue.copy()
                self.next_queue.clear()
                self.current_time += 1
        

    def file_log(self,logfile):
        with open(logfile,'w') as f:
            for d in self.log:
                print(d, file=f)


        
config_file = None
debug_mode = False

try:
    config_file = sys.argv[1]
except:
    print('config file missing!')
    exit(0)

try:
    if sys.argv[2] == 'debug':
        debug_mode = True
    print('commads:')
    print('Hit Enter to advance one step')
    print('Type quit to exit')
    print('Type kill n to remove a node (e.g. kill 1 to kill node number 1)')
except:
    pass


running = True
timer = 0
current_queue = []
next_queue = []
wrld = World()
wrld.load(config_file+'.cfg')
f = open(config_file+'-'+strftime("%d-%m-%Y %H_%M_%S", gmtime())+'.txt','w')
#nodes = wrld.list_nodes()
node_vis={}
while running:
    print("World map:")
    print(wrld)
    print('------------------------------------------------------------------------')
    print('timestamp = %d'%timer)
    print('timestamp = %d'%timer, file=f)
    print('----------------------Current queue-------------------------------------')
    print('\n'.join([str(m) for m in current_queue]))
    print('------------------------------------------------------------------------')
    print('-----------------------Current queue------------------------------------',file=f)
    print('\n'.join([str(m) for m in current_queue]),file=f)
    print('------------------------------------------------------------------------',file=f)
    print("World map:",file=f)
    print(wrld,file=f)
    nodes = wrld.list_nodes()
    if len(nodes)==0:
        break
    #shuffle(nodes)
    for n in nodes:
        node_vis[n.address]=wrld.visibility(n)

    for n in nodes:
        n.run(current_queue,next_queue,node_vis[n.address],timer)
        # print(n.candidates)
    print('-----------------------Next queue---------------------------------------',file=f)
    print('\n'.join([str(m) for m in next_queue]),file=f)
    print('------------------------------------------------------------------------',file=f)

    print('-----------------------Next queue---------------------------------------')
    print('\n'.join([str(m) for m in next_queue]))
    print('------------------------------------------------------------------------')

    for n in nodes:
        print('n= %d'%n.address)
        print('ap? '+str(n.is_ap))
        print("Battery level= %f %%"%n.battery)
        if n.is_sta:
            print("Connected?"+str(n.connected()))
        if n.is_ap:
            print('associated nodes = '+str(n.a_nodes))
            print('pings list='+str(n.pings))
        print('input = '+str(n.message_in))
        print('output = '+str(n.message_out))
        #######################################################
        print('n= %d'%n.address, file=f)
        print('ap? '+str(n.is_ap), file=f)
        print("Battery level= %f %%"%n.battery, file=f)
        if n.is_sta:
            print("Connected?"+str(n.connected()), file=f)
        if n.is_ap:
            print('associated nodes = '+str(n.a_nodes), file=f)
            print('pings list='+str(n.pings), file=f)
        print('input = '+str(n.message_in), file=f)
        print('output = '+str(n.message_out), file=f)
        if n.battery <= 0:
           wrld.kill_node(n)

    current_queue = next_queue.copy()
    next_queue.clear()
    timer += 1

    if debug_mode:
        cmd = str(input('>>'))
        if 'quit' in cmd:
            running = False
        if 'kill' in cmd:
            cs = cmd.split()
            n = wrld.get_node(int(cs[1]))
            wrld.kill_node(n)

f.close()
