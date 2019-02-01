import re
AGENT = re.compile('\{agent:\s*mac\s*=\s*[0-9]*,\s*x\s*=\s*[0-9]*,\s*y\s*=\s*[0-9]*\s*\}')
WORLD = re.compile('\{world:\s*width=\s*[0-9]*,\s*height=\s*[0-9]*,\s*v_threshold=\s*[0-9]*\s*\}')
WALL = re.compile('\{wall:\s*x=\s*[0-9]*,\s*y=\s*[0-9]*\s*\}')

def read_config(filename):
    lines = None
    agents = []
    ags = []
    world = {}
    ws = None
    walls = []
    wls = []

    with open(filename) as f:
        lines = f.readlines()
        
    for l in lines:

        if AGENT.match(l):

            ags.append(l.replace('{','').replace('}',''))

            continue

        if WALL.match(l):

            wls.append(l.replace('{','').replace('}',''))

            continue

        if WORLD.match(l):

            ws = l.replace('{','').replace('}','')

            continue

    w_params = ws.split(':')[1].split(',')

    for p in w_params:
        
        if 'width' in p:
            world['width']=int(p.replace('width=',''))
        if 'height' in p:
            world['height']=int(p.replace('height=',''))
        if 'v_threshold' in p:
            world['v_threshold']=int(p.replace('v_threshold=',''))

    for a in ags:
        ags_p = a.split(':')[1].split(',')
        ag = {}
        for p in ags_p:

            if 'mac' in p:
                ag['mac'] = int(p.replace('mac=',''))
            if 'x' in p:
                ag['x'] = int(p.replace('x=',''))
            if 'y' in p:
                ag['y'] = int(p.replace('y=',''))
        agents.append(ag)

    for w in wls:
        wls_p = w.split(':')[1].split(',')
        wl = {}
        for p in wls_p:

            if 'x' in p:
                wl['x'] = int(p.replace('x=',''))
            if 'y' in p:
                wl['y'] = int(p.replace('y=',''))
        walls.append(wl)

    return world,agents,walls


if __name__=='__main__':
    read_config("config1.cfg")
