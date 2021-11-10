import pygame,sys,math,time,copy,datetime,json,random,asyncio,urllib
import numpy as np
from pygame.key import start_text_input

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

WHITE   =  (255, 255, 255)
ORANGE  =  (255, 127, 0  )
YELLOW  =  (255, 255, 0  )
BLACK   =  (0  , 0  , 0  )
BLUE    =  (0  , 0  , 255)
RED     =  (255, 0  , 0  )
SKYBLUE =  (135, 206, 235)
SLIVER  =  (192, 192, 192)

INPUT = 5
OUTPUT = 2
OUTMAX = INPUT + OUTPUT

def ReLU(x):
    return max(x,0)

#https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
def sortObjectBy(__Iter1,__attr,reverse = False):
    return np.array(sorted(__Iter1, key=lambda x: x.__getattribute__(__attr), reverse=reverse))

class Node:
    def __init__(self) -> None:
        self.value = 0
        self.activated = False
        self.forwardAble = False
        self.preConn = []
        self.postConn = []
    
    def addValue(self, value):
        self.value += value
    
    def reset(self):
        self.value = 0
        self.activated = False
        self.forwardAble = False
    
    def updateForwardAble(self,connections,num):
        result = []
        connEnds = map(lambda x : not x.activated if x.end == num else None, connections)
        for i in range(len(connEnds)):
            if connEnds[i] is not None :
                result.append(i)
        if all([connEnds[conn] for conn in result]):
            self.forwardAble = True
        else:
            self.forwardAble = False

    def updatePreConn(self,connections,num):
        self.preConn = []
        connEnds = [connections.end for i in connections]
        for i in range(len(connEnds)):
            if connEnds[i] == num :
                self.preConn.append(i)
    
    def updatePostConn(self,connections,num):
        self.postConn = []
        connStarts = [connections.start for i in connections]
        for i in range(len(connStarts)):
            if connStarts[i] == num :
                self.postConn.append(i)

class Connection:
    def __init__(self, start, end, innovationNum, weight = None, disabled = False) -> None:
        self.start = start
        self.end = end
        self.innovationNum = innovationNum
        self.weight = weight
        if self.weight is None:
            self.weight = random.choice(np.arange(0.0,1.0,0.01))
        self.disabled = disabled

    def reset(self):
        self.activated = False
    
    def mutation(self):
        if random.random < 0.8:
            self.weight += max(0,random.choice(np.arange(self.weight-0.3,self.weight+0.3,0.01)))
        else:
            self.weight = random.choice(np.arange(0.0,1.0,0.01))

class Topology:
    def __init__(self) -> None:
        self.innovationNum = 0
        self.nodes = [*([Node() for i in range(INPUT)]),*([Node() for i in range(OUTPUT)])]
        self.connections = []
    
    def addConnectionMutation(self):
        start = random.randint(0,INPUT-1)
        end = random(INPUT,OUTMAX-1)
        self.innovationNum += 1
        self.connections.append(Connection(start,end,self.innovationNum))
    
    def addNodeMutaion(self):
        if self.connections != []:
            choice = random.choice(range(len(self.connections)))
            target = self.connections[choice]
            self.nodes.append(Node())
            self.connections[choice].disable = True
            self.innovationNum += 1
            self.connections.append(Connection(target.start,len(self.nodes)-1,self.innovationNum,target.weight))
            self.innovationNum += 1
            self.connections.append(Connection(len(self.nodes)-1,target.end,self.innovationNum,1.0))
        else:
            self.addConnectionMutation()
    
    def forward(self):
        #TODO : 신경망 굴리도록 해야함.
        sortedConn = sortObjectBy(self.connections,'start')
        
        for i in range(len(self.nodes)) :
            self.nodes[i].updatePreConn(self.connections,i)
            self.nodes[i].updatePostConn(self.connections,i)

        forwardAble = self.countForwardAble()
        while all(map(lambda x : x.activated,self.nodes)):
            forwardAble = self.countForwardAble()
            for i in range(len(forwardAble)):
                nowNode = self.nodes[i]
                for conn in nowNode.postConn:
                    connection = self.connections[conn]
                    self.nodes[connection.end].addValue(self.nodes[connection.start] * connection.weight)

                nowNode.value = ReLU(nowNode.value)
                nowNode.activated = True
                
        result = list(map(lambda x : x.value , self.nodes[INPUT:OUTMAX]))
        for conn in self.connections : conn.reset()
        for node in self.nodes : node.reset()

        return result
    
    def countForwardAble(self) -> list:
        result = []
        for i in range(len(self.nodes)) : self.nodes[i].updateForwardAble(self.connections,i)
        for i in range(len(self.nodes)) : result.append(i) if self.nodes[i].forwardAble and not self.nodes[i].activated else None
        return result # return forwarAble and not activated Node idx list

class Player:
    def __init__(self,x,y,topology,connection) -> None:
        self.x = x
        self.y = y
        self.degree = 0
        self.speed = 0
        self.topology = topology
        self.connection = connection
    
    def move(self):
        self.x += math.cos(math.radians(self.degree)) * self.speed
        self.y += math.sin(math.radians(self.degree)) * self.speed
    
    def turn(self,degree):
        self.degree = degree
    
    def draw(self,screen):
        pygame.draw.circle(screen,YELLOW,(self.x,self.y),5)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("NEAT SIMULATION")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(20,SCREEN_HEIGHT/2)

    clock = pygame.time.Clock()
    while True:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(BLACK)
        player.draw(screen)
        pygame.display.update()