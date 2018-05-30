from world import *
from agent_node import *
from random import randint

wrld = World()
wrld.load('config1.cfg')

print(wrld)
#print(wrld.grid.nodes)
n = wrld.get_node(3)
#print(repr(wrld.get_node(3)))
#print(wrld.list_nodes())
print(wrld.visibility(n))


