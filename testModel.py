from datetime import datetime

import networkx as nx

from model.model import Model

myModel=Model()
myModel.buildGraph(5)

v0=myModel.getAllNodes()[0]
connessa=list(nx.node_connected_component(myModel._graph,v0))
v1=connessa[10]

print(v0,v1)
tic=datetime.now()
path,obj=myModel.getCamminoOttimo(v0,v1,4)
print("-----------")
print(f"Cammino ottimo trovato in {datetime.now()-tic} con peso: ")
print(obj)
print(*path,sep="\n")