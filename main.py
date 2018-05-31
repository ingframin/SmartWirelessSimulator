from world import *
from agent_node import *
from random import randint

running = True
timer = 0
message_queue = []

wrld = World()
wrld.load('config1.cfg')
f = open('log.txt','w')

while True:
    
        
    print(wrld)
    nodes = wrld.list_nodes()
    for n in nodes:
        n.run(message_queue,wrld.visibility(n),timer)
        
    if timer == 10:
        wrld.kill_node(nodes[4])
        
    f.write(str(message_queue))
    for n in nodes:
        print('n= %d'%n.address)
        print('ap? '+str(n.is_ap))
        if n.is_ap:
            print('associated nodes = '+str(n.a_nodes))
        print('input = '+str(n.message_in))
        print('output = '+str(n.message_out))
        
    message_queue = list(filter(lambda m: m['timestamp'] > timer, message_queue))
    timer += 1
    input()
