""" 
For each node you need at least one edge.
Start with one node. In each iteration, 
create a new node and a new edge. 
The edge is to connect the new node with a 
random node from the previous node set.
After all nodes are created, 
create random edges until S is fulfilled. 
Make sure not to create double edges 
(for this you can use an adjacency matrix).

Random graph is done in O(S).
"""

from random import choice, randint

class Vertex:
    def __init__(self, id):
        self.id = id
        self.edges = set()

class Edge:
    def __init__(self, vertexA, vertexB, weight):
        self.vertexA = vertexA
        self.vertexB = vertexB
        self.weight = weight
        
        vertexA.edges.add(self)
        vertexB.edges.add(self)

class Graph:
    def __init__(self, n, s, minWeight, maxWeight):
        self.vertices = []
        self.edges = set()
        
        self.n = n
        self.s = s
        self.minWeight = minWeight
        self.maxWeight = maxWeight
        
        if n > 0:
            self.vertices.append(Vertex(0))
            
        for i in range(1, n):
            vertex = Vertex(i)
            self.edges.add(Edge(vertex, choice(self.vertices), randint(self.minWeight, self.maxWeight)))
            self.vertices.append(vertex)
        
        nEdges = n - 1
        while nEdges < s:
            vertexA = choice(self.vertices)
            vertexB = choice(self.vertices)
            if vertexA != vertexB and vertexA not in vertexB.edges:
                self.edges.add(Edge(vertexA, vertexB, randint(self.minWeight, self.maxWeight)))
                nEdges += 1
    
    def ids(self, source, destination):
        depth = 0
        while (solution := self.search(source, destination, algo='dfs', max_depth=depth)) is None:
            depth += 1
        return solution
    
    def search(self, source, destination, algo='ucs', max_depth=999999):       
        if algo == 'ids':
            return self.ids(source, destination)
        
        frontier = HeapFrontier()
        if algo == 'dfs':
            frontier = StackFrontier()
        elif algo == 'bfs':
            frontier = QueueFrontier()
            
        initialNode = Node(self.vertices[source])
        
        frontier.add(initialNode)
        visited = set()    
        
        while not frontier.isEmpty():
            node = frontier.remove()
            visited.add(node.vertex.id)
            
            if node.depth <= max_depth:
                if node.vertex.id == destination:
                    return node.path()
                
                for edge in node.vertex.edges:
                    otherVertex = edge.vertexB if edge.vertexA == node.vertex else edge.vertexA
                    if otherVertex.id not in visited:
                        new_node = Node(otherVertex, node, node.cost + edge.weight)
                        frontier.add(new_node)          
                    
            