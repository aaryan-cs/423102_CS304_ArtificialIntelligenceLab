import random
import time
import heapq
from collections import deque
import math
def generate_connected_weighted_graph(n_nodes,extra_edge_prob=0.01,max_weight=10):
    adj = {i:[] for i in range(n_nodes)}
    nodes = list(range(n_nodes))
    random.shuffle(nodes)
    for i in range(1, n_nodes):
        u = nodes[i]
        v = nodes[random.randrange(0, i)]
        w = random.randint(1, max_weight)
        adj[u].append((v,w))
        adj[v].append((u,w))
    for u in range(n_nodes):
        for v in range(u+1,n_nodes):
            if random.random() < extra_edge_prob:
                w = random.randint(1, max_weight)
                adj[u].append((v,w))
                adj[v].append((u,w))
    return adj

# BFS
def bfs(adj,start,goal):
    visited = {start}
    q = deque([start])
    parent = {start: None}
    nodes_expanded = 0
    t0 = time.time()
    while q:
        u = q.popleft()
        nodes_expanded += 1
        if u == goal:
            t1 = time.time()
            path = []
            while u is not None:
                path.append(u)
                u = parent[u]
            return {"time": t1-t0, "nodes": nodes_expanded, "path": path[::-1]}
        for v, _ in adj[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                q.append(v)
    return {"time": time.time()-t0, "nodes": nodes_expanded, "path": None}

# DFS
def dfs(adj,start,goal):
    visited= set()
    parent= {start: None}
    stack= [start]
    nodes_expanded = 0
    t0 = time.time()
    while stack:
        u = stack.pop()
        if u in visited: 
            continue
        visited.add(u)
        nodes_expanded += 1
        if u == goal:
            t1 = time.time()
            path = []
            while u is not None:
                path.append(u)
                u = parent[u]
            return {"time": t1-t0, "nodes": nodes_expanded, "path": path[::-1]}
        for v, _ in adj[u]:
            if v not in visited:
                parent[v] = u
                stack.append(v)
    return {"time": time.time()-t0, "nodes": nodes_expanded, "path": None}

# UCS
def ucs(adj,start,goal):
    heap = [(0,start)]
    parent = {start: None}
    dist = {start: 0}
    visited = set()
    nodes_expanded = 0
    t0 = time.time()
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited: 
            continue
        visited.add(u)
        nodes_expanded += 1
        if u == goal:
            t1 = time.time()
            path = []
            while u is not None:
                path.append(u)
                u = parent[u]
            return {"time": t1-t0, "nodes": nodes_expanded, "path": path[::-1], "cost": d}
        for v, w in adj[u]:
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))
    return {"time": time.time()-t0, "nodes": nodes_expanded, "path": None}

# IDS
def ids(adj,start,goal,max_depth=50):
    def dls(limit):
        stack = [(start, 0)]
        parent = {start: None}
        visited = set()
        nodes = 0
        while stack:
            u, depth = stack.pop()
            if (u, depth) in visited: 
                continue
            visited.add((u, depth))
            nodes += 1
            if u == goal:
                return True, nodes, parent
            if depth<limit:
                for v, _ in adj[u]:
                    parent[v] = u
                    stack.append((v, depth+1))
        return False, nodes, parent

    total_nodes = 0
    t0 = time.time()
    for depth in range(max_depth+1):
        found, nodes, parent = dls(depth)
        total_nodes += nodes
        if found:
            t1 = time.time()
            path = []
            u = goal
            while u is not None:
                path.append(u)
                u = parent.get(u)
            return {"time": t1-t0, "nodes": total_nodes, "path": path[::-1]}
    return {"time": time.time()-t0, "nodes": total_nodes, "path": None}


def path_cost(adj,path):
    if not path: return None
    cost = 0
    for i in range(len(path)-1):
        for v, w in adj[path[i]]:
            if v == path[i+1]:
                cost += w
                break
    return cost

def run_experiments(n_nodes=1000, trials=3):
    adj = generate_connected_weighted_graph(n_nodes)
    algos = {"BFS": bfs, "DFS": dfs, "UCS": ucs, "IDS": ids}
    results = {a: {"time": [], "nodes": [], "cost": []} for a in algos}
    for _ in range(trials):
        start, goal = random.sample(range(n_nodes), 2)
        for name, func in algos.items():
            res = func(adj, start, goal)
            results[name]["time"].append(res["time"])
            results[name]["nodes"].append(res["nodes"])
            if res["path"]:
                results[name]["cost"].append(path_cost(adj, res["path"]))
    print("\nComparison Table (averaged over", trials, "trials):")
    print("{:<5} {:<12} {:<15} {:<10}".format("Algo", "Avg Time (s)", "Avg Nodes Expanded", "Avg Path Cost"))
    for name in algos:
        t = sum(results[name]["time"])/len(results[name]["time"])
        n = sum(results[name]["nodes"])/len(results[name]["nodes"])
        c = sum(results[name]["cost"])/len(results[name]["cost"]) if results[name]["cost"] else None
        print("{:<5} {:<12.6f} {:<15.1f} {:<10}".format(name, t, n, str(c)))

if __name__ == "__main__":
    run_experiments(n_nodes=1000, trials=3)
