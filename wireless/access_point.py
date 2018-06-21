class AccessPointComponent:

    def __init__(self,ssid,max_cons = 5):
        self.ssid = ssid
        self.max_cons = max_cons
        self.a_nodes = set()

    def send_beacon(self, address):
        '''Broadcast the SSID'''
        message = {'sender':address,'receiver':-1,'type':'beacon','SSID':self.ssid}
        return message

    def process_connection_request(self,address,request):
        '''Process connection requests and decide to accept or refuse'''
        response = {'sender':address,'receiver':request['sender'],
                    'type':'response'}
        
        if len(self.a_nodes) < self.max_cons:
            self.a_nodes.add(request['sender'])
            response['params']='accept'
        else:
            response['params']='refuse'
        
        return response

    def reset(self):
        self.ssid = ''
        self.a_nodes.clear()

    def set_ssid(self,ssid):
        self.ssid = ssid