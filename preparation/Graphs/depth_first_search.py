from collections import defaultdict
class Graph():
    def __init__(self):
        self.graph=defaultdict(list)

    def addEdge(self,u,v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def dfs(self,node,visited):
        visited[node]=True
        print(node)

        for each in self.graph[node]:
            if each not in visited:
                self.dfs(each,visited)


var=Graph()
var.addEdge(1,2)
var.addEdge(1,3)
var.addEdge(2,4)
var.addEdge(3,5)
var.addEdge(5,6)
var.addEdge(6,7)

var.dfs(7,{})


