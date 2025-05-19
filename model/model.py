import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._bestObjFun = []
        self._bestPath = 0
        self._graph=nx.Graph()
        self._airports=DAO.getAllAirports()
        self._idMapAirports={}
        for a in self._airports:
            self._idMapAirports[a.ID] = a



    def buildGraph(self, nMin):
        nodes=DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self.addAllArchiV1()
        print(len(self._graph.nodes))
        print(len(self._graph.edges))
        self._graph.clear_edges()
        self.addAllArchiV2()
        print(len(self._graph.edges))



    def addAllArchiV1(self):
        allEdges= DAO.getAllEdgesV1(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:
                if self._graph.has_edge(e.aeroportoP, e.aeroportoD):
                    self._graph[e.aeroportoP][e.aeroportoD]["weight"]+=e.peso
                    #sommi i voli di ritorno
                else:
                    self._graph.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)

    def addAllArchiV2(self):
        allEdges= DAO.getAllEdgesV2(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:
                self._graph.add_edge(e.aeroportoP,e.aeroportoD,weight=e.peso)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        node=list(self._graph.nodes)
        node.sort(key=lambda x:x.IATA_CODE)
        return node


    def getSortedNeighbors(self,node):
        neighbors=self._graph.neighbors(node)
        neighbTuples=[]
        #lista di tuple con nodi cvicini e peso arco
        for n in neighbors:
            neighbTuples.append((n,self._graph[node][n]["weight"]))
        neighbTuples.sort(key=lambda x:x[1], reverse=True)
        return neighbTuples

    def getPath(self,v0,v1):
        path=nx.dijkstra_path(self._graph,v0,v1, weight=None)
        #è ottimo
        # path = nx.shortest_path(self._graph, v0, v1)
        # mydict=dict(nx.bfs_predecessors(self._graph, v0))
        # path=[v1]
        # while path[0]!= v0:
        #     path.insert(0,mydict[path[0]])
        return path

    def getCamminoOttimo(self,v0,v1,t):
        self._bestPath=[]
        self._bestObjFun=0
        parziale=[v0]
        self._ricorsione(parziale,v1,t)
        return self._bestPath, self._bestObjFun

    def _ricorsione(self,parziale,v1,t):
        #verificare se parziale è una possibile soluzione
        if parziale[-1]==v1:
            #verificare se parziale è ottimo, meglio del best corrente
            if self._getObjFunc(parziale)> self._bestObjFun:
                self._bestPath=copy.deepcopy(parziale)
                self._bestObjFun=self._getObjFunc(parziale)
                return
                #esco
        if len(parziale)==t+1:
            return
        #posso ancora aggiungere nodi
        else:
            #prendo ultimo nodo, i vicini e poi ricomincio
            for n in self._graph.neighbors(parziale[-1]):
                if n not in parziale:
                    parziale.append(n)
                    self._ricorsione(parziale,v1,t)
                    parziale.pop()


    def _getObjFunc(self,parziale):
        objVal=0
        for i in range(0,len(parziale)-1):
            objVal+=self._graph[parziale[i]][parziale[i+1]]["weight"]
        return objVal

