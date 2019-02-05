import enum

class MessageType(enum.Enum):
    beacon = 0
    request = 1
    response = 2
    data = 3


class Message:
    
    def __init__(self,sender:int, receiver:int, mess_type:MessageType):
        self.sender = sender
        self.receiver = receiver
        self.type = mess_type
        self.content = []
        
    