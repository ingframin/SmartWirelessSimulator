from world import *
from agent_node import *
from random import randint,shuffle

running = True
timer = 0
message_queue = []

wrld = World()
wrld.load('config1.cfg')
f = open('log.txt','w')
nodes = wrld.list_nodes()
while running:

    print('------------------------------------------------------------------------')
    print(message_queue)
    print('------------------------------------------------------------------------')
    print(wrld)
    nodes = wrld.list_nodes()
    shuffle(nodes)
    for n in nodes:
        n.run(message_queue,wrld.visibility(n),timer)

    f.write(str(message_queue))

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
        if n.battery <= 0:
            wrld.kill_node(n)

    message_queue = list(filter(lambda m: m['timestamp'] > timer, message_queue))
    timer += 1
    cmd = str(input('>>'))
    if 'quit' in cmd:
        running = False
    if 'kill' in cmd:
        cs = cmd.split()
        n = wrld.get_node(int(cs[1]))
        wrld.kill_node(n)
f.close()
