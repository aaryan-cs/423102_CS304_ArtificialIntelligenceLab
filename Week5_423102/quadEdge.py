class QuarterEdge:
    def __init__(self, data: int | None=None):
        self._data = data
        self._next: QuarterEdge | None = None
        self._rot: QuarterEdge | None = None
    
    def rot(self):
        """Rotate anticlockwise, same Quad Edge"""
        return self._rot
    
    def sym(self):
        """Flip Quarter Edge, same Quad Edge"""
        return self.rot().rot()
    
    def tor(self):
        """Rotate clockwise, same Quad Edge"""
        return self.rot().rot().rot()
    
    def next(self):
        """Rotate anticlockwise, same source"""
        return self._next
    
    def prev(self):
        """Rotate clockwise, same source"""
        return self.rot().next().rot()
    
    def lnext(self):
        """Navigate triangle towards left"""
        return self.tor().next().rot()
    
    def rnext(self):
        """Navigate triangle towards right"""
        return self.sym().next()
    
    def data(self):
        return self._data
    
    def dest(self):
        return self.sym().data()
    
def makeQuadEdge(start: int, end: int):
    startEnd = QuarterEdge(start)
    leftRight = QuarterEdge()
    endStart = QuarterEdge(end)
    rightLeft = QuarterEdge()

    startEnd._rot = leftRight
    leftRight._rot = endStart
    endStart._rot = rightLeft
    rightLeft._rot = startEnd

    startEnd._next = startEnd
    endStart._next = endStart
    leftRight._next = rightLeft
    rightLeft._next = leftRight

    return startEnd

def swapNexts(a: QuarterEdge, b: QuarterEdge):
    a._next, b._next = b._next, a._next

def splice(a : QuarterEdge, b : QuarterEdge):
    swapNexts(a.next().rot(), b.next().rot())
    swapNexts(a, b)

def makeTriangle(a: int, b: int, c: int):
    ab = makeQuadEdge(a, b)
    bc = makeQuadEdge(b, c)
    ca = makeQuadEdge(c, a)

    splice(ab.sym(), bc)
    splice(bc.sym(), ca)
    splice(ca.sym(), ab)

    return ab

def connect(a: QuarterEdge, b: QuarterEdge):
    newEdge = makeQuadEdge(a.dest(), b.data())
    splice(newEdge, a.lnext())
    splice(newEdge.sym(), b)
    return newEdge

def sever(edge: QuarterEdge):
    splice(edge, edge.prev())
    splice(edge.sym(), edge.sym().prev())

def insertPoint(polygonEdge: QuarterEdge, point: int):
    firstSpoke = makeQuadEdge(polygonEdge.data(), point)
    splice(firstSpoke, polygonEdge)
    spoke = firstSpoke
    while True:
        spoke = connect(polygonEdge, spoke.sym())
        polygonEdge = spoke.prev()
        if polygonEdge.lnext() == firstSpoke:
            break
    return firstSpoke

def flip(edge: QuarterEdge):
    a = edge.prev()
    b = edge.sym().prev()
    splice(edge, a)
    splice(edge.sym(), b)
    splice(edge, a.lnext())
    splice(edge.sym(), b.lnext())
    edge._data = a.dest()
    edge.sym()._data = b.dest()