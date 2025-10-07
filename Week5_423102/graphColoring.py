<<<<<<< HEAD
from delauney import getDelauneyGraph, N_VERTICES
from graph import Graph
from typing import List, Tuple
from matplotlib import pyplot as plt
import time, tracemalloc

K = 4

def validColoring(colors: List[int], color: int, current: int, graph: Graph):
    for v in graph.vertices[current].adjacency:
        if colors[v] == color:
            return False
    return True

def backtrackingColoring(graph: Graph, colors: List[int], current: int):
    if current == N_VERTICES:
        return colors    
    for i in range(K):
        if validColoring(colors, i, current, graph):
            colors[current] = i
            c = backtrackingColoring(graph, colors, current + 1)
            if c is not None:
                return c
    return None


def largestDegreeFirst(graph: Graph):
    order = sorted(range(N_VERTICES), key=lambda v: -len(graph.vertices[v].adjacency))
    colors = [-1] * N_VERTICES
    for v in order:
        neighbor_colors = {colors[n] for n in graph.vertices[v].adjacency if colors[n] != -1}
        for c in range(K):
            if c not in neighbor_colors:
                colors[v] = c
                break
    return colors


def plotColoredGraph(graph: Graph, colors, palette: Tuple[str]):
    vertices = graph.vertices
    for i, v in enumerate(vertices):
        p1 = v.coordinates
        for idx in v.adjacency:
            p2 = vertices[idx].coordinates
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color="black", linewidth=1, zorder=1)
        plt.scatter(p1[0], p1[1], color=palette[colors[i]], zorder=2)
    plt.show()

def benchmark(method_name, func, *args):
    tracemalloc.start()
    start = time.time()
    colors = func(*args)
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "Method": method_name,
        "Time (s)": end - start,
        "Memory (KB)": round(peak / 1024, 2),
        "Colors": colors
    }

# --------------------
# Run Experiments
# --------------------
graph = getDelauneyGraph()

results = []
results.append(benchmark("Naïve Backtracking", backtrackingColoring, graph, [0] * N_VERTICES, 0))
results.append(benchmark("Largest Degree First", largestDegreeFirst, graph))

# Print results as a table
print(f"{'Method':<20} {'Time (s)':<10} {'Memory (KB)':<12}")
for r in results:
    print(f"{r['Method']:<20} {r['Time (s)']:<10} {r['Memory (KB)']:<12}")

# Plot the heuristic result (faster one)
plotColoredGraph(graph, results[1]["Colors"], ("red", "green", "blue", "orange"))
=======
from delauney import getDelauneyGraph, N_VERTICES
from graph import Graph
from typing import List, Tuple
from matplotlib import pyplot as plt
import time, tracemalloc

K = 4

def validColoring(colors: List[int], color: int, current: int, graph: Graph):
    for v in graph.vertices[current].adjacency:
        if colors[v] == color:
            return False
    return True

def backtrackingColoring(graph: Graph, colors: List[int], current: int):
    if current == N_VERTICES:
        return colors    
    for i in range(K):
        if validColoring(colors, i, current, graph):
            colors[current] = i
            c = backtrackingColoring(graph, colors, current + 1)
            if c is not None:
                return c
    return None


def largestDegreeFirst(graph: Graph):
    order = sorted(range(N_VERTICES), key=lambda v: -len(graph.vertices[v].adjacency))
    colors = [-1] * N_VERTICES
    for v in order:
        neighbor_colors = {colors[n] for n in graph.vertices[v].adjacency if colors[n] != -1}
        for c in range(K):
            if c not in neighbor_colors:
                colors[v] = c
                break
    return colors


def plotColoredGraph(graph: Graph, colors, palette: Tuple[str]):
    vertices = graph.vertices
    for i, v in enumerate(vertices):
        p1 = v.coordinates
        for idx in v.adjacency:
            p2 = vertices[idx].coordinates
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color="black", linewidth=1, zorder=1)
        plt.scatter(p1[0], p1[1], color=palette[colors[i]], zorder=2)
    plt.show()

def benchmark(method_name, func, *args):
    tracemalloc.start()
    start = time.time()
    colors = func(*args)
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "Method": method_name,
        "Time (s)": end - start,
        "Memory (KB)": round(peak / 1024, 2),
        "Colors": colors
    }

# --------------------
# Run Experiments
# --------------------
graph = getDelauneyGraph()

results = []
results.append(benchmark("Naïve Backtracking", backtrackingColoring, graph, [0] * N_VERTICES, 0))
results.append(benchmark("Largest Degree First", largestDegreeFirst, graph))

# Print results as a table
print(f"{'Method':<20} {'Time (s)':<10} {'Memory (KB)':<12}")
for r in results:
    print(f"{r['Method']:<20} {r['Time (s)']:<10} {r['Memory (KB)']:<12}")

# Plot the heuristic result (faster one)
plotColoredGraph(graph, results[1]["Colors"], ("red", "green", "blue", "orange"))
>>>>>>> 52317de (Week 6,7,8 added.)
