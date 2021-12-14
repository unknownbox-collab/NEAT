import numpy as np
FIRST = 0
LAST = -1

class Node:
    def __init__(self,topology,objId,connFrom,preConn = [], postConn = []) -> None:
        self.value = 0
        self.topology = topology
        if connFrom > LAST:
            self.layer = topology.nodes[connFrom].layer + 1
        else:
            self.layer = connFrom + 1
        self.innovNum = 0
        self.preConn = np.array(preConn)
        self.postConn = np.array(postConn)
        self.id = objId

class Edge:
    def __init__(self, start, end, weight) -> None:
        self.start = start  #id
        self.end = end    #id
        self.weight = weight
        self.disabled = False

class Topology:
    def __init__(self, inputNum, outputNum) -> None:
        self.nodes = np.array([])
        self.makeNewNodes(inputNum  , FIRST - 1)
        self.makeNewNodes(outputNum , LAST  - 1)
        self.conns = np.array([])
        self.nowId = 0
        self.innovN
        self.maxLayer = 0
        self.inputNum = inputNum
        self.outputNum = outputNum
        self.layerNum = []
    
    def load(self,nodes,conns,innovNum,maxLayer,layerNum):
        self.nodes += nodes
        self.conns += conns
        self.innovNum = innovNum
        self.maxLayer = maxLayer
        self.layerNum = layerNum
    
    def addConnMutation(self): #O(n^2)
        nodeLayer = np.array(map(lambda x : x.layer ,self.nodes))
        cand = np.array(list(map(lambda x : x if sum(self.layerNum[x.layer:]) != len(x.postConn) else False, self.nodes[nodeLayer>-1])))
        cand = cand[cand!=False]
        start = np.random.choice(cand)
        cand = np.array(list(map(lambda x : x if not x.id in list(map(lambda y : (y.start, y.end),x.postConn)) else False, self.nodes[nodeLayer==-1 | nodeLayer>start.layer])))
        end = np.random.choice(cand)

    
    def addEdgeMutation(self):
        #TODO : targetNode.layer != -1 and targetNode don't have every available Edge.
        self.conns.append(Edge())

    def addNodeMutation(self):
        self.nodes

    def makeNewNodes(self, num, connFrom):
        for i in range(num):
            self.nodes.append(Node(self,self.nowId,connFrom))
            self.nowId += 1