from world import *
from agent_node import *
#from wireless import *
from random import randint,shuffle
from time import gmtime, strftime
import sys
        
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
config = read_config(config_file+'.cfg')
wrld.config(config)

wrl,agents,walls = config
agents_table = {}
for ag in agents:
    #temporary
    agents_table[ag['mac']] = Agent(ag['mac'],ag['x'],ag['y'])
    agents_table[ag['mac']].set_station()

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
        agents_table[n.id].run(current_queue,next_queue,wrld.visibility(n),timer)

    print('-----------------------Next queue---------------------------------------',file=f)
    print('\n'.join([str(m) for m in next_queue]),file=f)
    print('------------------------------------------------------------------------',file=f)

    print('-----------------------Next queue---------------------------------------')
    print('\n'.join([str(m) for m in next_queue]))
    print('------------------------------------------------------------------------')

    for n in nodes:
        print('n= %d'%n.id)
        print('ap? '+str(agents_table[n.id].is_ap))
        print("Battery level= %f %%"%agents_table[n.id].battery)
        if agents_table[n.id].is_sta:
            print("Connected?"+str(agents_table[n.id].connected()))
        if agents_table[n.id].is_ap:
            print('associated nodes = '+str(agents_table[n.id].a_nodes))
            print('pings list='+str(agents_table[n.id].pings))
        print('input = '+str(agents_table[n.id].message_in))
        print('output = '+str(agents_table[n.id].message_out))
        #######################################################
        print('n= %d'%n.id, file=f)
        print('ap? '+str(agents_table[n.id].is_ap), file=f)
        print("Battery level= %f %%"%agents_table[n.id].battery, file=f)
        if agents_table[n.id].is_sta:
            print("Connected?"+str(agents_table[n.id].connected()), file=f)
        if agents_table[n.id].is_ap:
            print('associated nodes = '+str(agents_table[n.id].a_nodes), file=f)
            print('pings list='+str(agents_table[n.id].pings), file=f)
        print('input = '+str(agents_table[n.id].message_in), file=f)
        print('output = '+str(agents_table[n.id].message_out), file=f)

    nds = list(nodes)
    for n in nds:
        if agents_table[n.id].battery <= 0:
            print(agents_table[n.id].battery)
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
