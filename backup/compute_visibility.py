from math import sqrt

width = 16
height = 16

grid = [0 for x in range(width*height)]

def set_wall(x,y):
    global grid
    grid[x+width*y] = 1


set_wall(1,3)
set_wall(2,3)
set_wall(3,3)
set_wall(4,3)
set_wall(5,3)

def distance(x1,y1,x2,y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def visibility(grid,width,height,x1,y1,x2,y2,threshold = 100):

    if distance(x1,y1,x2,y2) > threshold:
        return False
    
    if x2<x1:
        x1,x2 = x2,x1
    #if y2<y1:
    #    y1,y2 = y2,y1

    dy = y2-y1
    dx = x2-x1
    m = dy/dx
   
    q = -x1+y1/m
    mul = 2
    
    steps = [x /(mul) for x in range(mul*x1, mul*x2)]
    print(steps)
    for i in steps:
        j = int(m*i+q)
        print("i=%d, j=%d"%(i,j))
        if grid[int(i)+width*j] == 1:
            print_grid(grid)
            return False
        grid[int(i)+width*j] = 5
    print_grid(grid)
    return True
    

def print_grid(grid):
    
    counter = 0
    for g in grid:
        print(g, end="", flush=True)
        counter+=1
        if counter == width:
            counter = 0
            print()
    

