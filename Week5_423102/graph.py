<<<<<<< HEAD
from typing import List

class Vertex:
    def __init__(self, coordinates: tuple[int, int]):
        self.coordinates = coordinates
        self.adjacency = set()
    
    def connect(self, vertexId: int):
        self.adjacency.add(vertexId)

class Graph:
    def __init__(self, points : tuple[int, int], ):
        self.vertices : List[Vertex] = []
        for pt in points:
            self.vertices.append(Vertex(pt))

=======
from typing import List

class Vertex:
    def __init__(self, coordinates: tuple[int, int]):
        self.coordinates = coordinates
        self.adjacency = set()
    
    def connect(self, vertexId: int):
        self.adjacency.add(vertexId)

class Graph:
    def __init__(self, points : tuple[int, int], ):
        self.vertices : List[Vertex] = []
        for pt in points:
            self.vertices.append(Vertex(pt))

>>>>>>> 52317de (Week 6,7,8 added.)
