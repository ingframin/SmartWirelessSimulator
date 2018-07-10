from world import *
from .agent_node import *
#from wireless import *
from random import randint,shuffle
from time import gmtime, strftime
import sys
        
config_file = None
debug_mode = False

try:
    config_file = 'config1'
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


agents_table = wrld.grid.nodes


f = open(config_file+'-'+strftime("%d-%m-%Y %H_%M_%S", gmtime())+'.txt','w')

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

    for n in nodes:
        agents_table[n.address].run(current_queue,next_queue,wrld.visibility(n),timer)

    print('-----------------------Next queue---------------------------------------',file=f)
    print('\n'.join([str(m) for m in next_queue]),file=f)
    print('------------------------------------------------------------------------',file=f)

    print('-----------------------Next queue---------------------------------------')
    print('\n'.join([str(m) for m in next_queue]))
    print('------------------------------------------------------------------------')

    for n in nodes:
        print('n= %d'%n.address)
        print('ap? '+str(agents_table[n.address].is_ap))
        print("Battery level= %f %%"%agents_table[n.address].battery)
        if agents_table[n.address].is_sta:
            print("Connected?"+str(agents_table[n.address].connected()))
        if agents_table[n.address].is_ap:
            print('associated nodes = '+str(agents_table[n.address].a_nodes))
            print('pings list='+str(agents_table[n.address].pings))
        print('input = '+str(agents_table[n.address].message_in))
        print('output = '+str(agents_table[n.address].message_out))
        #######################################################
        print('n= %d'%n.address, file=f)
        print('ap? '+str(agents_table[n.address].is_ap), file=f)
        print("Battery level= %f %%"%agents_table[n.address].battery, file=f)
        if agents_table[n.address].is_sta:
            print("Connected?"+str(agents_table[n.address].connected()), file=f)
        if agents_table[n.address].is_ap:
            print('associated nodes = '+str(agents_table[n.address].a_nodes), file=f)
            print('pings list='+str(agents_table[n.address].pings), file=f)
        print('input = '+str(agents_table[n.address].message_in), file=f)
        print('output = '+str(agents_table[n.address].message_out), file=f)

    nds = list(nodes)
    for n in nds:
        if agents_table[n.address].battery <= 0:
            print(agents_table[n.address].battery)
            input()
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
