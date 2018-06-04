from world import *
from agent_node import *
from random import randint,shuffle
from time import gmtime, strftime

running = True
timer = 0
message_queue = []

wrld = World()
wrld.load('config2.cfg')
f = open('log'+strftime("%d-%m-%Y %H:%M:%S", gmtime())+'.txt','w')
#nodes = wrld.list_nodes()
while running:
    print('timestamp = %d'%timer)
    print('timestamp = %d'%timer, file=f)
    print('------------------------------------------------------------------------')
    print(message_queue)
    print('------------------------------------------------------------------------')
    print(wrld)
    print('------------------------------------------------------------------------',file=f)
    print(message_queue,file=f)
    print('------------------------------------------------------------------------',file=f)
    print(wrld,file=f)
    nodes = wrld.list_nodes()
    if len(nodes)==0:
        break
    shuffle(nodes)
    for n in nodes:
        n.run(message_queue,wrld.visibility(n),timer)
        # print(n.candidates)

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

    message_queue = list(filter(lambda m: m['timestamp'] > timer, message_queue))
    timer += 1
    # cmd = str(input('>>'))
    # if 'quit' in cmd:
    #     running = False
    # if 'kill' in cmd:
    #     cs = cmd.split()
    #     n = wrld.get_node(int(cs[1]))
    #     wrld.kill_node(n)

f.close()
