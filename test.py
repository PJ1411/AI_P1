import pygame
import math
import queue

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
found=False
WIDTH = 24
HEIGHT = 24
MARGIN = 1
START = [19,0]
END = [0,19]

#Layout for Game-Table
# 1 = Wall
layout = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]
    ]

# Classes 
opn = queue.PriorityQueue()
visited=[]
class Field:
    def __init__(self,X,Y):
        self.x = X
        self.y = Y
        self.parent=None
        self.reached=False
        self.neighbours=[]
        self.wall = False
        self.start = False
        self.end = False
        self.g= None
        self.prio=0;

    def __lt__(self,other):
        return self.prio < other.prio
    
    def getNeighbours(self,fields):
        X = self.x
        Y = self.y
        self.neighbours = [0,0,0,0]
        if(X>0):
            if(fields[X-1][Y].wall==False):
                self.neighbours[0] = fields[X-1][Y]
        if(X<19):
            if(fields[X+1][Y].wall==False):
                self.neighbours[2] = fields[X+1][Y]
        if(Y>0):
            if(fields[X][Y-1].wall==False):
                self.neighbours[3] = fields[X][Y-1]
        if(Y<19):
            if(fields[X][Y+1].wall==False):
                self.neighbours[1] = fields[X][Y+1]
        
             
class Grid:
    def __init__(self,lo,w,h,m,Start,End):
        self.layout=lo
        self.width = w
        self.height = h
        self.margin = m
        self.start = None
        self.end = None
        self.solved = False
        self.fields=[]
        for x in range(0,20):
            row = []
            for y in range(0,20):
                field = Field(x,y)
                if(self.layout[x][y]==1):
                    field.wall = True
                    visited.insert(len(visited),field)
                if([x,y] == Start):
                    field.start = True
                    self.start = field
                elif([x,y] == End):
                    field.end = True
                    self.end = field
                row.insert(y,field)
            self.fields.append(row)
                
                
    def setLayout(self,udate):
        self.layout=update

    def drawGrid(self):
        for x in range(0,20):
            for y in range(0,20):
                if(self.layout[x][y]==0):
                    if(self.fields[x][y].reached):
                        pygame.draw.rect(screen,GREEN,[(self.margin + self.width) * y + self.margin,(self.margin + self.height) * x + self.margin,self.width,self.height])
                    else:
                        pygame.draw.rect(screen,WHITE,[(self.margin + self.width) * y + self.margin,(self.margin + self.height) * x + self.margin,self.width,self.height])
                elif(self.layout[x][y]==1):
                    pygame.draw.rect(screen,BLACK,[(self.margin + self.width) * y + self.margin,(self.margin + self.height) * x + self.margin,self.width,self.height])
                if([x,y] == [self.start.x,self.start.y]):
                    pygame.draw.rect(screen,BLUE,[(self.margin + self.width) * y + self.margin,(self.margin + self.height) * x + self.margin,self.width,self.height])
                elif([x,y] == [self.end.x,self.end.y]):
                    pygame.draw.rect(screen,RED,[(self.margin + self.width) * y + self.margin,(self.margin + self.height) * x + self.margin,self.width,self.height])

grid = Grid(layout,WIDTH,HEIGHT,MARGIN,START,END)

#Prints PrioQueue
def getFrontier(frontier):
   temp = queue.PriorityQueue()
   print("Frontier:")
   size= frontier.qsize()
   for v in range(0,size):
      knoten = frontier.get()
      temp.put(knoten)
      print(knoten[0], " | " , knoten[1].x, ",", knoten[1].y)
   for v in range(0,size):
      knoten = temp.get()
      frontier.put(knoten)

def f(field):
    h = math.sqrt((grid.end.x-field.x)**2+(grid.end.y-field.y)**2)
    g = field.g
    return (h+g)

#Checks if node is in froniter-PrioQueue
def inPrio(node,frontier):
   size = frontier.qsize()
   temp = queue.PriorityQueue()
   seen = False
   
   for v in range(0,size):
      knoten = frontier.get()
      temp.put(knoten)
      if(node.x == knoten[1].x and node.y == knoten[1].y):
          seen = True
          
   for v in range(0,size):
      knoten = temp.get()
      frontier.put(knoten)
   return seen

#Removes node from frontier-PrioQueue
def remove(node,frontier):
    size = frontier.qsize()
    temp = queue.PriorityQueue()
    for v in range(0,size):
        knoten = frontier.get()
        not_found = True
        if(node.x == knoten[1].x and node.y==knoten[1].y):
            not_found = False
        if(not_found):
            temp.put(knoten)
    for v in range(0,size-1):
       knoten = temp.get()
       frontier.put(knoten)

def cost(a,b):
    return 1;
        
def getPath(node):
    while True:
        if(node.x == grid.start.x and node.y == grid.start.y):
            break
        else:
            pygame.draw.rect(screen,BLUE,[(MARGIN + WIDTH) * node.y + MARGIN,(MARGIN + HEIGHT) * node.x + MARGIN,WIDTH,HEIGHT])
        node = node.parent
        
    
def UpdateVertex(s, s_neu):
    if(s.g+cost(s,s_neu)<s_neu.g):
        s_neu.g = s.g + cost(s,s_neu)
        s_neu.parent = s
        if(inPrio(s_neu,opn)):
            remove(s_neu,opn)
        opn.put((f(s_neu),s_neu))

def Initialize():
    grid.start.g = 0
    grid.start.parent=grid.start
    opn.put((f(grid.start),grid.start))
    
def AStar():
    tupel = opn.get()
    s = tupel[1]
    last = s
    if(s.x==grid.end.x and s.y==grid.end.y ):
        print("Ziel erreicht")
        grid.solved = True
        grid.end.parent = s.parent
        return
    visited.insert(len(visited),s)
    s.reached = True
    s.getNeighbours(grid.fields)
    for i in range(0,4):
        if(s.neighbours[i]!=0):
            child = s.neighbours[i]
            not_visited = True
            for v in range(0,len(visited)):
                if(visited[v].x==child.x and visited[v].y==child.y):
                    not_visited =False
                    break
            if(not_visited):
                if(inPrio(child,opn)==False):
                    child.g = math.inf
                    child.parent = 0
            UpdateVertex(s,child)
                       
                           

pygame.init()

size = (500, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

done = False

not_found=False
clock = pygame.time.Clock()
Initialize()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

     
    if(grid.solved==False):
        AStar()
    screen.fill(BLACK)

           
    if(grid.solved==True):
        grid.drawGrid()
        getPath(grid.end)
    else:
        grid.drawGrid()
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
