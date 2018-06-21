class Node:

    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    
    def __eq__(self, n):
        return self.x == n.x and self.y == n.y
    
    def __hash__(self):
        return hash(str("x:%d;y:%d"%(self.x,self.y)))
    

class EmptyNode(Node):
    def __init__(self,x=0,y=0):
        Node.__init__(self,x,y)
    
    def __repr__(self):
        return 'Empty Node: (x = %d ; y = %d)'%(self.x,self.y)
    
class WallNode(Node):
    def __init__(self,x=0,y=0):
        Node.__init__(self,x,y)
    def __repr__(self):
        return 'Wall Node: (x = %d ; y = %d)'%(self.x,self.y)

class AgentNode(Node):
    def __init__(self,x=0,y=0,id=0):
        Node.__init__(self,x,y)
        self.id = id

    def __repr__(self):
        return 'Agent Node id= %d: (x = %d ; y = %d)'%(self.id,self.x,self.y)
    
    