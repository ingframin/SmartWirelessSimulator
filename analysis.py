def battery(filename):
    with open(filename) as f:
        raw = f.readlines()
        buffer = {}
        current = 0
        for line in raw:
            if "n=" in line:
                n = int(line.split('=')[1])
                if n not in buffer:
                    buffer[n] = []
                current = n
                    
            if 'Battery' in line:
                b = float(line.split("=")[1].replace('%',''))
                buffer[current].append(b)

    with open('battery_'+filename,'w') as ref:
        
        for n in buffer:
            ref.write('n='+str(n)+'\n')
            for b in buffer[n]:
                ref.write(str(b)+'\n')
                
    return buffer

def a_nodes(filename):
    with open(filename) as f:
        raw = f.readlines()
        buffer = {}
        current = 0
 
        for line in raw:
                
            if "n=" in line:
                n = int(line.split('=')[1])
                if n not in buffer:
                    buffer[n] = []
                current = n
                    
            if 'associated nodes' in line and not ("set" in line):
                b = line.split("=")[1]
                buffer[current].append(b)

    with open('a_nodes_'+filename,'w') as ref:
        
        for n in buffer:
            ref.write('n='+str(n)+'\n')
            for b in buffer[n]:
                ref.write(str(b)+'\n')
                
    return buffer
                

def isAP(filename):
    with open(filename) as f:
        raw = f.readlines()
        buffer = {}
        current = 0
 
        for line in raw:
                
            if "n=" in line:
                n = int(line.split('=')[1])
                if n not in buffer:
                    buffer[n] = []
                current = n
                    
            if 'ap?' in line:
                b = bool(line.split("?")[1])
                buffer[current].append(b)

    with open('isAP_'+filename,'w') as ref:
        
        for n in buffer:
            ref.write('n='+str(n)+'\n')
            for b in buffer[n]:
                ref.write(str(b)+'\n')
                
    return buffer
                
                
