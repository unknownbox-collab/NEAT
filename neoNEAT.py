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
        for i in range(self.inNodeNum):
            self.nodes[i] = Node(i,[],[],0)
        for i in range(self.inNodeNum,self.outNodeNum + self.inNodeNum):
            self.nodes[i] = Node(i,[],[],-1)
        self.edges = list(edges)

        def modifyLayer(nextNode):
            for edge in nextNode.next:
                end = edge.end
                if self.nodes[end].layer != -1 and self.nodes[end].layer < nextNode.layer + 1:
                    self.nodes[end].layer = nextNode.layer + 1
                    if self.maxLayer < nextNode.layer + 1: self.maxLayer = nextNode.layer + 1
                    nextNode = self.nodes[end]
                    modifyLayer(nextNode)
                else:
                    break

        for edge in edges:
            if not edge.start in self.nodes.keys():
                self.nodes[edge.start] = Node(edge.start,[],[edge],1)
                if self.maxLayer < 1: self.maxLayer = 1
            else:
                self.nodes[edge.start].next.append(edge)
            if not edge.end in self.nodes.keys():
                frontLayer = self.nodes[edge.start].layer
                self.nodes[edge.end] = Node(edge.end,[edge],[],frontLayer + 1)
                if self.inNodeNum <= edge.end < self.inNodeNum + self.outNodeNum:
                    self.nodes[edge.end].layer = -1
                print(frontLayer)
                if self.maxLayer < frontLayer + 1:
                    self.maxLayer = frontLayer + 1
            else:
                self.nodes[edge.end].before.append(edge)
                frontLayer = self.nodes[edge.start].layer
                if self.nodes[edge.end].layer < frontLayer + 1 and self.nodes[edge.end].layer != -1:
                    self.nodes[edge.end].layer = frontLayer + 1
                    modifyLayer(self.nodes[edge.end])
    
    def forward(self,*inputValue):
        values = {}
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
            for edge in self.edges:
                if self.nodes[edge.end].layer == targetLayer and not self.nodes[edge.end].disAbled:
                    if self.nodes[edge.start].layer != 0:
                        values[edge.end] += ReLU(values[edge.start] * edge.weight)
                    else:
                        values[edge.end] += values[edge.start] * edge.weight
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
        print((start.nodeId,end.nodeId,weight,innovNum))
        self.edges.append(Edge(start.nodeId,end.nodeId,weight,innovNum))
        self.init(*self.edges)
        innovNum += 1
    
    def addNodeMutation(self):
        start = self.nodes[random.choice(list(self.nodes.keys()))]
        end = self.nodes[random.choice(list(self.nodes.keys()))]

t = Topology(3,2)
innovNum = 5
t.init()
t.addEdgeMutation()
t.addEdgeMutation()
t.addEdgeMutation()
t.addEdgeMutation()
t.addEdgeMutation()
t.addEdgeMutation()
result = t.forward(2,2,2)
print(result)