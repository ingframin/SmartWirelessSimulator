import math
#test for determining the central node

class Node:

    def __init__(self, name, x,y):
        self.x = x
        self.y = y
        self.name = name

    
    def distance(self,node):
        return math.sqrt((self.x-node.x)**2 + (self.y-node.y)**2)
    
    def __repr__(self):
        return self.name+'\tx: '+str(self.x)+'\ty:'+str(self.y)
    
def central(distances):
    avg = []
    for n in distances:
        avgd = sum(distances[n])/len(distances[n])
        avg.append((n,avgd))
    dc = 10000000000
    nc = None
    for d in avg:
        if d[1] < dc:
            dc = d[1]
            nc = d[0]
    
    return nc



n1 = Node('1',1,2)
n2 = Node('2',3,5)
n3 = Node('3',0,0)
n4 = Node('4',6,1)
n5 = Node('5',5,3)

nodes = [n1,n2,n3,n4,n5]

distances = dict()

for n in nodes:
    for n2 in nodes:
        try:
            distances[n].append(n.distance(n2))
        except:
            distances[n] = []

print(distances)

print(central(distances))