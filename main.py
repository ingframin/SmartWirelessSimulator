# -*- coding: utf-8 -*-
from world import *
from agent_node import *
from random import randint,shuffle
from time import gmtime, strftime
import sys

#Map representation must be made graphical with Pyglet or Pygame or something else

strategies = ['closest','random','bidding','sorted']

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

f = open(config_file+'-result.txt','w')
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
        print("Strategy: "+strategies[n.strategy])
        print("Current AP: "+str(n.current_ap))
        if n.is_ap:
            print('associated nodes = '+str(n.a_nodes))
            print('pings list='+str(n.pings))
        print('input = '+str(n.message_in))
        print('output = '+str(n.message_out))
        #######################################################
        print('n= %d'%n.address, file=f)
        print('ap? '+str(n.is_ap), file=f)
        print("Battery level= %f %%"%n.battery, file=f)
        print("Strategy: "+strategies[n.strategy],file=f)
        print("Current AP: "+str(n.current_ap),file = f)
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
