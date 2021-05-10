#from prettytable import PrettyTable
from utils import *
import queue

class Node:

   def __init__(self, name):
       self.parent = 0
       self.name = name
       self.edges = []
       self.value = 0

def getChildNodes_BFS(problem, parent, visited,frontier):
   for i in range(0,len(g.nodes)):
      if(g.nodes[i].name == parent.name):
         if(len(g.nodes[i].edges)>0):
            for e in range(0,len(g.nodes[i].edges)):
               child = Node(g.nodes[i].edges[e].end.name)
               child.parent = parent
               child.value = g.nodes[i].edges[e].value+parent.value
               if(check_visited(child,visited)==False and check_Frontier(child,frontier)==False):
                  if(child.name == problem.end):
                     problem.solved = True
                     problem.best_node = child
                     return
                  frontier.put(child)

def getChildNodes_UCS(problem, parent, visited,frontier):
   for i in range(0,len(g.nodes)):
      if(g.nodes[i].name == parent.name):
         if(len(g.nodes[i].edges)>0):
            for e in range(0,len(g.nodes[i].edges)):
               child = Node(g.nodes[i].edges[e].end.name)
               child.parent = parent
               child.value = g.nodes[i].edges[e].value+parent.value
               if(check_visited(child,visited)==False and check_FrontierPrio(child,frontier)==False):
                  frontier.put((child.value,child))
               elif(check_FrontierPrio(child,frontier)==True):
                  check_HigherCost(child,frontier)


def getChildNodes_DFS(problem, parent, visited,frontier):
   for i in range(0,len(g.nodes)):
      if(g.nodes[i].name == parent.name):
         if(len(g.nodes[i].edges)>0):
            for e in range(0,len(g.nodes[i].edges)):
               child = Node(g.nodes[i].edges[e].end.name)
               child.parent = parent
               child.value = g.nodes[i].edges[e].value+parent.value
               if(check_visited(child,visited)==False and check_FrontierLIFO(child,frontier)==False):
                  if(child.name == problem.end):
                     problem.solved = True
                     problem.best_node = child
                     return
                  frontier.put(child)

                  


               
   
def check_visited(node,visited):
   for v in range(0,len(visited)):
      if(node.name == visited[v].name):
         return True
   return False

def check_Frontier(node,frontier):
   size = frontier.qsize()
   temp = queue.Queue()
   seen = False
   for v in range(0,size):
      knoten = frontier.get()
      temp.put(knoten)
      if(node.name == knoten.name):
         seen = True
   for v in range(0,size):
      knoten = temp.get()
      frontier.put(knoten)
   return seen

def check_FrontierPrio(node,frontier):
   size = frontier.qsize()
   temp = queue.PriorityQueue()
   seen = False
   for v in range(0,size):
      knoten = frontier.get()
      temp.put(knoten)
      if(node.name == knoten[1].name):
         seen = True
   for v in range(0,size):
      knoten = temp.get()
      frontier.put(knoten)
   return seen

def check_FrontierLIFO(node,frontier):
   size = frontier.qsize()
   temp = queue.LifoQueue()
   seen = False
   for v in range(0,size):
      knoten = frontier.get()
      temp.put(knoten)
      if(node.name == knoten.name):
         seen = True
   for v in range(0,size):
      knoten = temp.get()
      frontier.put(knoten)
   return seen
      
def check_HigherCost(node,frontier):
   size = frontier.qsize()
   temp = queue.PriorityQueue()
   for v in range(0,size):
      knoten = frontier.get()
      if(node.name == knoten[1].name and node.value < knoten[1].value):
         temp.put((node.value,node))
      else:
         temp.put(knoten)
   for v in range(0,size):
      knoten = temp.get()
      frontier.put(knoten)


def getPath(node):
   path = []
   i=0
   while(True):
      if(node.parent == 0):
         return path
      path.insert(i,node)
      i += 1
      node = node.parent

   return path
                  

class Edge:

   def __init__(self, edge):
      self.start = edge[0]
      self.end = edge[1]
      self.value = edge[2]


class Graph:

   def __init__(self, node_list, edges):
      self.nodes = []
      for name in node_list:
         self.nodes.append(Node(name))

      for e in edges:
        e = (getNode(e[0],self.nodes), getNode(e[1], self.nodes), e[2])        

        self.nodes[next((i for i,v in enumerate(self.nodes) if v.name == e[0].name), -1)].edges.append(Edge(e))
        self.nodes[next((i for i,v in enumerate(self.nodes) if v.name == e[1].name), -1)].edges.append(Edge((e[1], e[0], e[2])))


   def print(self):
      node_list = self.nodes
      
      t = PrettyTable(['  '] +[i.name for i in node_list])
      for node in node_list:
         edge_values = ['X'] * len(node_list)
         for edge in node.edges:
            edge_values[ next((i for i,e in enumerate(node_list) if e.name == edge.end.name) , -1)] = edge.value           
         t.add_row([node.name] + edge_values)
      print(t)
            

g = Graph( ['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa',
 'Va', 'Ri', 'Ti', 'Lu', 'Pi', 'Ur', 'Hi',
 'Me', 'Bu', 'Dr', 'Ef', 'Cr', 'Gi'],
[
   ('Or', 'Ze', 71), ('Or', 'Si', 151),
   ('Ne', 'Ia', 87), ('Ze', 'Ar', 75),
   ('Ia', 'Va', 92), ('Ar', 'Si', 140),
   ('Ar', 'Ti', 118), ('Si', 'Fa', 99),
   ('Si', 'Ri', 80), ('Fa', 'Bu', 211),
   ('Va', 'Ur', 142), ('Ri', 'Pi', 97),
   ('Ri', 'Cr', 146), ('Ti', 'Lu', 111),
   ('Lu', 'Me', 70), ('Me', 'Dr', 75),
   ('Dr', 'Cr', 120), ('Cr', 'Pi', 138),
   ('Pi', 'Bu', 101), ('Bu', 'Gi', 90),
   ('Bu', 'Ur', 85), ('Ur', 'Hi', 98),
   ('Hi', 'Ef', 86)
] )

def getFrontier(frontier):
   temp = queue.Queue()
   print("Frontier:")
   size= frontier.qsize()
   for v in range(0,size):
      knoten = frontier.get()
      temp.put(knoten)
      print(knoten)
   for v in range(0,size):
      knoten = temp.get()
      frontier.put(knoten)


      
class problem:
   def __init__(self,start,end):
      self.start = start
      self.end = end
      self.path_cost = 0
      self.solved = False
      self.best_node = None
      
def bfs(problem):
   node = Node(problem.start)
   if(problem.solved): return "Schon gelöst!"
   frontier = queue.Queue()
   frontier.put(node)
   visited=[]

   while problem.solved==False:
      if frontier.empty():
         return "Fehler"
      knoten = frontier.get()
      visited.insert(len(visited),knoten)
      getChildNodes_BFS(problem,knoten,visited,frontier)
      if(problem.solved == True):
         path = getPath(problem.best_node)
         kosten = problem.best_node.value
         print("Gelöst mit BFS!")
         print("Kosten:")
         print(kosten)
         print("Pfad:")
         pathString = ""
         for p in range(0,len(path)):
            pathString = "->" + path[p].name + pathString
         pathString = problem.start + pathString
            
         print(pathString)
         

def ucs(problem):
   node = Node(problem.start)
   if(problem.solved): return "Schon gelöst!"
   frontier = queue.PriorityQueue()
   frontier.put((0,node))
   visited=[]

   while problem.solved==False:
      if(frontier.empty()):
         return "FEHLER"
      knoten = frontier.get()[1]
      if(problem.end == knoten.name):
         path = getPath(knoten)
         kosten = knoten.value
         print("Gelöst mit UCS!")
         print("Kosten:")
         print(kosten)
         print("Pfad:")
         pathString = ""
         for p in range(0,len(path)):
            pathString = "->" + path[p].name + pathString
         pathString = problem.start + pathString
         print(pathString)
         problem.solved=True
      visited.insert(len(visited),knoten)
      getChildNodes_UCS(problem,knoten,visited,frontier)
      
                  
def dfs(problem):
   node = Node(problem.start)
   if(problem.solved): return "Schon gelöst!"
   frontier = queue.LifoQueue()
   frontier.put(node)
   visited = []

   while problem.solved==False:
      if frontier.empty():
         return "Fehler"
      knoten = frontier.get()
      visited.insert(len(visited),knoten)
      getChildNodes_DFS(problem,knoten,visited,frontier)
      if(problem.solved == True):
         path = getPath(problem.best_node)
         kosten = problem.best_node.value
         print("Gelöst mit DFS!")
         print("Kosten:")
         print(kosten)
         print("Pfad:")
         pathString = ""
         for p in range(0,len(path)):
            pathString = "->" + path[p].name + pathString
         pathString = problem.start + pathString
            
         print(pathString)
         problem.solved = True
   
   


p1 = problem('Bu','Ti')
p2 = problem('Bu','Ti')
p3 = problem('Bu','Ti')
bfs(p1)
print("----------")
ucs(p2)
print("----------")
dfs(p3)
print("----------")
      
      

   
   
   
   
   
   

   

                   
            
