<<<<<<< HEAD
from random import uniform
from quadEdge import *
from typing import List
from graph import *

N_VERTICES = 100
X_LIM = 100
Y_LIM = 100

def getVertices():
    verts = []
    for i in range(N_VERTICES):
        x = uniform(-X_LIM, X_LIM)
        y = uniform(-Y_LIM, Y_LIM)
        verts.append((x, y))
    return verts

def make_supertriangle():
    dx = 2 * X_LIM
    dy = 2 * Y_LIM
    dmax = max(dx, dy)

    # Vertices of a huge triangle
    p1 = (-2 * dmax, -dmax)
    p2 = (0, 2 * dmax)
    p3 = (2 * dmax, -dmax)

    return [p1, p2, p3]

def orient2d(a, b, p):
    """Return positive if p is left of ab, negative if right, 0 if collinear."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])

def in_circumcircle(a, b, c, d):
    """
    Return True if point d lies inside the circumcircle of triangle abc.
    Assumes (a,b,c) are in counter-clockwise order.
    """
    ax, ay = a[0] - d[0], a[1] - d[1]
    bx, by = b[0] - d[0], b[1] - d[1]
    cx, cy = c[0] - d[0], c[1] - d[1]

    det = (
        (ax * ax + ay * ay) * (bx * cy - cx * by)
        - (bx * bx + by * by) * (ax * cy - cx * ay)
        + (cx * cx + cy * cy) * (ax * by - bx * ay)
    )

    return det > 0

def locate_point(p: tuple[int, int], start_edge: QuarterEdge, points: List[tuple[int, int]]):
    """Locate the triangle containing point p, starting from start_edge."""
    e = start_edge
    while True:
        a = points[e.data()]
        b = points[e.lnext().data()]
        c = points[e.lnext().lnext().data()]

        # Check if p is inside triangle (a,b,c) using barycentric/area test
        if (orient2d(a, b, p) >= 0 and
            orient2d(b, c, p) >= 0 and
            orient2d(c, a, p) >= 0):
            return e  # found a containing edge (triangle is e’s face)

        # Otherwise, decide which edge to cross
        if orient2d(a, b, p) < 0:
            e = e.sym()          # cross AB
        elif orient2d(b, c, p) < 0:
            e = e.lnext().sym()  # cross BC
        else:
            e = e.lnext().lnext().sym()  # cross CA

def isLocallyDelauney(edge: QuarterEdge, points: List[tuple[int, int]]):
    a = points[edge.data()]
    b = points[edge.dest()]
    c = points[edge.lnext().lnext().data()]
    d = points[edge.sym().lnext().lnext().data()]

    return not in_circumcircle(a, b, c, d)

def delauney(points, superPts):
    points = superPts + points

    superTri = makeTriangle(0, 1, 2)
    
    for index, pt in enumerate(points[3:], start=3):
        triEdge = locate_point(pt, superTri, points)
        firstSpoke = insertPoint(triEdge, index)

        spoke = firstSpoke
        while True:
            edge = spoke.next()
            if isLocallyDelauney(edge, points):
                spoke = spoke.lnext().sym()
                if (spoke == firstSpoke):
                    break
            else:
                flip(edge)


    return superTri

def obtainGraph(start: QuarterEdge, points: List[tuple[int, int]]) -> Graph:
    graph = Graph(points[3:])
    vertices = graph.vertices

    visited = set()
    stack = [start]
    while stack:
        e = stack.pop()
        if e in visited:
            continue
        visited.add(e)

        if e.data() is not None and e.data() not in (0, 1, 2) and e.dest() not in (0, 1, 2):
            vertices[e.data() - 3].connect(e.dest() - 3)   
            vertices[e.dest() - 3].connect(e.data() - 3)        
            p1 = points[e.data()]
            p2 = points[e.dest()]

        # neighbors of an edge you can reach directly
        for nxt in (e.next(), e.rot(), e.sym()):
            if nxt is not None and nxt not in visited:
                stack.append(nxt)

    return graph  
    # plt.show()

def getDelauneyGraph() -> Graph:
    vertices = getVertices()
    superPts = make_supertriangle()

    start = delauney(vertices, superPts)
    graph = obtainGraph(start, superPts + vertices)
    return graph

=======
from random import uniform
from quadEdge import *
from typing import List
from graph import *

N_VERTICES = 100
X_LIM = 100
Y_LIM = 100

def getVertices():
    verts = []
    for i in range(N_VERTICES):
        x = uniform(-X_LIM, X_LIM)
        y = uniform(-Y_LIM, Y_LIM)
        verts.append((x, y))
    return verts

def make_supertriangle():
    dx = 2 * X_LIM
    dy = 2 * Y_LIM
    dmax = max(dx, dy)

    # Vertices of a huge triangle
    p1 = (-2 * dmax, -dmax)
    p2 = (0, 2 * dmax)
    p3 = (2 * dmax, -dmax)

    return [p1, p2, p3]

def orient2d(a, b, p):
    """Return positive if p is left of ab, negative if right, 0 if collinear."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])

def in_circumcircle(a, b, c, d):
    """
    Return True if point d lies inside the circumcircle of triangle abc.
    Assumes (a,b,c) are in counter-clockwise order.
    """
    ax, ay = a[0] - d[0], a[1] - d[1]
    bx, by = b[0] - d[0], b[1] - d[1]
    cx, cy = c[0] - d[0], c[1] - d[1]

    det = (
        (ax * ax + ay * ay) * (bx * cy - cx * by)
        - (bx * bx + by * by) * (ax * cy - cx * ay)
        + (cx * cx + cy * cy) * (ax * by - bx * ay)
    )

    return det > 0

def locate_point(p: tuple[int, int], start_edge: QuarterEdge, points: List[tuple[int, int]]):
    """Locate the triangle containing point p, starting from start_edge."""
    e = start_edge
    while True:
        a = points[e.data()]
        b = points[e.lnext().data()]
        c = points[e.lnext().lnext().data()]

        # Check if p is inside triangle (a,b,c) using barycentric/area test
        if (orient2d(a, b, p) >= 0 and
            orient2d(b, c, p) >= 0 and
            orient2d(c, a, p) >= 0):
            return e  # found a containing edge (triangle is e’s face)

        # Otherwise, decide which edge to cross
        if orient2d(a, b, p) < 0:
            e = e.sym()          # cross AB
        elif orient2d(b, c, p) < 0:
            e = e.lnext().sym()  # cross BC
        else:
            e = e.lnext().lnext().sym()  # cross CA

def isLocallyDelauney(edge: QuarterEdge, points: List[tuple[int, int]]):
    a = points[edge.data()]
    b = points[edge.dest()]
    c = points[edge.lnext().lnext().data()]
    d = points[edge.sym().lnext().lnext().data()]

    return not in_circumcircle(a, b, c, d)

def delauney(points, superPts):
    points = superPts + points

    superTri = makeTriangle(0, 1, 2)
    
    for index, pt in enumerate(points[3:], start=3):
        triEdge = locate_point(pt, superTri, points)
        firstSpoke = insertPoint(triEdge, index)

        spoke = firstSpoke
        while True:
            edge = spoke.next()
            if isLocallyDelauney(edge, points):
                spoke = spoke.lnext().sym()
                if (spoke == firstSpoke):
                    break
            else:
                flip(edge)


    return superTri

def obtainGraph(start: QuarterEdge, points: List[tuple[int, int]]) -> Graph:
    graph = Graph(points[3:])
    vertices = graph.vertices

    visited = set()
    stack = [start]
    while stack:
        e = stack.pop()
        if e in visited:
            continue
        visited.add(e)

        if e.data() is not None and e.data() not in (0, 1, 2) and e.dest() not in (0, 1, 2):
            vertices[e.data() - 3].connect(e.dest() - 3)   
            vertices[e.dest() - 3].connect(e.data() - 3)        
            p1 = points[e.data()]
            p2 = points[e.dest()]

        # neighbors of an edge you can reach directly
        for nxt in (e.next(), e.rot(), e.sym()):
            if nxt is not None and nxt not in visited:
                stack.append(nxt)

    return graph  
    # plt.show()

def getDelauneyGraph() -> Graph:
    vertices = getVertices()
    superPts = make_supertriangle()

    start = delauney(vertices, superPts)
    graph = obtainGraph(start, superPts + vertices)
    return graph

>>>>>>> 52317de (Week 6,7,8 added.)
