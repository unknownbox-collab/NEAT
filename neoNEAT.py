from math import e
import random,time

innovNum = 0

class Edge:
    def __init__(self,start,end,weight,innov,disAbled = False) -> None:
        self.start = start
        self.end = end
        self.weight = weight
        self.innov = innov
        self.disAbled = disAbled

class Node:
    def __init__(self,nodeId,before,next,layer) -> None:
        self.nodeId = nodeId
        self.before = before
        self.next = next
        self.layer = layer

class Topology:
    def __init__(self, inNodeNum, outNodeNum) -> None:
        self.inNodeNum = inNodeNum
        self.outNodeNum = outNodeNum
        self.maxLayer = 0
        self.nodes = {}
        self.edges = []
    
    def init(self,*edges):
        self.maxLayer = 0
        self.nodes = {}
        self.edges = list(edges)

        def modifyLayer(nextNode):
            for edge in nextNode.next:
                end = edge.end
                if self.nodes[end].layer != -1 and self.nodes[end].layer <= nextNode.layer + 1:
                    self.nodes[end].layer = nextNode.layer + 1
                    nextNode = self.nodes[end]
                    modifyLayer(nextNode)
                else:
                    break
        #print(f'=== edges : {list(map(lambda x: f"{x.start} -> {x.end}",self.edges))}')
        for edge in edges:
            if not edge.start in self.nodes.keys():
                self.nodes[edge.start] = Node(edge.start,[],[edge],0)
            else:
                self.nodes[edge.start].next.append(edge)

            if not edge.end in self.nodes.keys():
                frontLayer = self.nodes[edge.start].layer
                self.nodes[edge.end] = Node(edge.end,[edge],[],frontLayer + 1)
                if self.inNodeNum <= edge.end < self.inNodeNum + self.outNodeNum:
                    self.nodes[edge.end].layer = -1
            else:
                self.nodes[edge.end].before.append(edge)
                frontLayer = self.nodes[edge.start].layer
                if (self.nodes[edge.end].layer < frontLayer + 1 and self.nodes[edge.end].layer != -1):
                    self.nodes[edge.end].layer = frontLayer + 1
                    modifyLayer(self.nodes[edge.end])
        #print(f'=== nodes : {list(map(lambda x: f"{x} : {self.nodes[x].layer}",self.nodes.keys()))}')
        
        for i in range(self.inNodeNum):
            if not i in self.nodes.keys():
                self.nodes[i] = Node(i,[],[],0)
        for i in range(self.inNodeNum,self.outNodeNum + self.inNodeNum):
            if not i in self.nodes.keys():
                self.nodes[i] = Node(i,[],[],-1)
    
    def forward(self,*inputValue):
        values = {}
        print("====FORWARD====")
        self.maxLayer = max(map(lambda x: self.nodes[x].layer,self.nodes.keys()))
        for nodeId in self.nodes.keys():
            values[nodeId] = 0
            if nodeId < self.inNodeNum :
                values[nodeId] = inputValue[nodeId]
        
        def ReLU(x):
            return max(x,0)
        
        for nowLayer in range(self.maxLayer + 1):
            targetLayer = nowLayer + 1
            if nowLayer == self.maxLayer:
                targetLayer = -1
            print("- taget :",targetLayer)
            for edge in self.edges:
                if self.nodes[edge.end].layer == targetLayer and not edge.disAbled:
                    if self.nodes[edge.start].layer != 0:
                        values[edge.end] += ReLU(values[edge.start] * edge.weight)
                    else:
                        values[edge.end] += values[edge.start] * edge.weight
                    print(f"-- forward : {edge.start} -> {edge.end}[{values[edge.end]}]")
        return [values[i] for i in range(self.inNodeNum , self.inNodeNum + self.outNodeNum)]

    def addEdgeMutation(self):
        global innovNum

        availNodeNum = self.outNodeNum
        start = self.nodes[random.choice(list(self.nodes.keys()))]
        connectedZone = list(map(lambda x: x.end ,self.nodes[start.nodeId].next))
        if start.layer != -1 :
            for node in self.nodes.keys():
                if self.nodes[node].layer > start.layer:
                    availNodeNum += 1
        availNodeNum -= len(connectedZone)
        while start.layer == -1 or availNodeNum == 0:
            start = self.nodes[random.choice(list(self.nodes.keys()))]
            availNodeNum = self.outNodeNum
            for node in self.nodes.keys():
                if self.nodes[node].layer > start.layer:
                    availNodeNum += 1
            connectedZone = list(map(lambda x: x.end ,self.nodes[start.nodeId].next))
            availNodeNum -= len(connectedZone)
        
        end = self.nodes[random.choice(list(self.nodes.keys()))]
        while (end.layer <= start.layer and end.layer != -1) or (end.nodeId in connectedZone):
            connectedZone = list(map(lambda x: x.end ,self.nodes[start.nodeId].next))
            end = self.nodes[random.choice(list(self.nodes.keys()))]
        weight = random.random()
        print(f'newEdge({innovNum}) : {start.nodeId} -> {end.nodeId}[{weight}]')
        self.edges.append(Edge(start.nodeId,end.nodeId,weight,innovNum))
        self.init(*self.edges)
        innovNum += 1
    
    def addNodeMutation(self):
        global innovNum

        edgeNum = random.randint(0,len(self.edges)-1)
        edge = self.edges[edgeNum]
        while self.edges[edgeNum].disAbled:
            edgeNum = random.randint(0,len(self.edges)-1)
            edge = self.edges[edgeNum]
        self.edges[edgeNum].disAbled = True

        newId = max(self.nodes.keys()) + 1
        frontEdge = Edge(edge.start, newId, 1.0, innovNum)
        endEdge = Edge(newId, edge.end, edge.weight, innovNum)

        self.nodes[edge.start].next.append(frontEdge)
        innovNum += 1

        self.nodes[edge.end].before.append(endEdge)
        innovNum += 1

        self.edges.append(frontEdge)
        self.edges.append(endEdge)
        self.init(*self.edges)
        print(f'>> newNode : {edge.start} -> ({newId}) -> {edge.end}')

t = Topology(3,2)
innovNum = 5
t.init()
t.addEdgeMutation()
t.addNodeMutation()
t.addEdgeMutation()
t.addNodeMutation()
t.addEdgeMutation()
t.addEdgeMutation()
t.addEdgeMutation()
t.addEdgeMutation()
result = t.forward(1,1,1)
print(result)