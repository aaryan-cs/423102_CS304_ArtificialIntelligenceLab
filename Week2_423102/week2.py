<<<<<<< HEAD
import random, time, heapq, collections
from typing import List, Tuple, Dict

def generate_connected_weighted_graph(n:int, avg_degree:int=6, min_w=1, max_w=20, seed=None):
    """
    Generates a connected undirected weighted graph as adjacency list.
    - Build a random spanning tree (guarantees connectivity).
    - Add extra edges until average degree ≈ avg_degree.
    Returns adjacency list: {node: [(neighbor, weight), ...]}
    """
    if seed is not None:
        random.seed(seed)
    adj = {i: [] for i in range(n)}

    # spanning tree to ensure graph is connected
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(1, n):
        u = nodes[i]
        v = nodes[random.randint(0, i-1)]
        w = random.randint(min_w, max_w)
        adj[u].append((v,w)); adj[v].append((u,w))

    edges = n-1
    target_edges = max(edges, (n * avg_degree) // 2)
    attempts = 0
    while edges < target_edges and attempts < target_edges * 5:
        a, b = random.randrange(n), random.randrange(n)
        if a == b:
            attempts += 1
            continue
        if any(nb == b for nb,_ in adj[a]):
            attempts += 1
            continue
        w = random.randint(min_w, max_w)
        adj[a].append((b,w)); adj[b].append((a,w))
        edges += 1
    return adj

def is_connected(adj:Dict[int,List[Tuple[int,int]]], start=0)->bool:
    """Check if graph is connected via BFS"""
    n = len(adj)
    seen = {start}
    q = collections.deque([start])
    while q:
        u = q.popleft()
        for v,_ in adj[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    return len(seen) == n


def dfs(adj, start, goal, max_steps=10_000_000):
    t0 = time.perf_counter()
    stack = [(start, [start])]
    visited = set()
    nodes_expanded = 0
    while stack:
        node, path = stack.pop()
        nodes_expanded += 1
        if nodes_expanded > max_steps:
            break
        if node == goal:
            return path, nodes_expanded, time.perf_counter()-t0
        if node in visited:
            continue
        visited.add(node)
        for (nbr,_) in adj[node]:
            if nbr not in visited:
                stack.append((nbr, path+[nbr]))
    return None, nodes_expanded, time.perf_counter()-t0

def bfs(adj, start, goal):
    t0 = time.perf_counter()
    q = collections.deque([(start,[start])])
    visited = {start}
    nodes_expanded = 0
    while q:
        node, path = q.popleft()
        nodes_expanded += 1
        if node == goal:
            return path, nodes_expanded, time.perf_counter()-t0
        for (nbr,_) in adj[node]:
            if nbr not in visited:
                visited.add(nbr)
                q.append((nbr, path+[nbr]))
    return None, nodes_expanded, time.perf_counter()-t0

def ucs(adj, start, goal):
    t0 = time.perf_counter()
    dist = {start: 0}
    parent = {}
    visited = set()
    heap = [(0, start)]
    nodes_expanded = 0
    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited: continue
        visited.add(node); nodes_expanded += 1
        if node == goal:
            path = []
            cur = node
            while cur != start:
                path.append(cur); cur = parent[cur]
            path.append(start); path.reverse()
            return path, nodes_expanded, time.perf_counter()-t0, cost
        for (nbr,w) in adj[node]:
            if nbr in visited: continue
            nc = cost + w
            if nbr not in dist or nc < dist[nbr]:
                dist[nbr] = nc; parent[nbr] = node
                heapq.heappush(heap,(nc,nbr))
    return None, nodes_expanded, time.perf_counter()-t0, float('inf')

def depth_limited_dfs(adj, node, goal, limit, visited_local):
    expanded = 1
    if node == goal: return [node], expanded, False
    if limit == 0: return None, expanded, True
    cutoff_any = False
    for (nbr,_) in adj[node]:
        if nbr in visited_local: continue
        visited_local.add(nbr)
        path,e,cutoff = depth_limited_dfs(adj,nbr,goal,limit-1,visited_local)
        expanded += e
        visited_local.remove(nbr)
        if path is not None:
            return [node]+path, expanded, False
        if cutoff: cutoff_any = True
    return None, expanded, cutoff_any

def ids(adj, start, goal, max_depth=50):
    t0 = time.perf_counter()
    total_expanded = 0
    for depth in range(max_depth+1):
        visited_local = {start}
        path,e,cutoff = depth_limited_dfs(adj,start,goal,depth,visited_local)
        total_expanded += e
        if path is not None:
            return path, total_expanded, time.perf_counter()-t0, depth
        if not cutoff: break
    return None, total_expanded, time.perf_counter()-t0, None


def compare_algorithms_on_graph(adj, trials=5, seed=None):
    if seed is not None:
        random.seed(seed)
    n = len(adj)
    results = {'DFS': [], 'BFS': [], 'UCS': [], 'IDS': []}
    pairs = []
    for _ in range(trials):
        s = random.randrange(n); d = random.randrange(n)
        while d == s: d = random.randrange(n)
        pairs.append((s,d))

    for s,d in pairs:
        p_dfs, n_dfs, t_dfs = dfs(adj,s,d)
        p_bfs, n_bfs, t_bfs = bfs(adj,s,d)
        p_ucs, n_ucs, t_ucs, c_ucs = ucs(adj,s,d)
        p_ids, n_ids, t_ids, d_ids = ids(adj,s,d,max_depth=50)

        results['DFS'].append((p_dfs,n_dfs,t_dfs))
        results['BFS'].append((p_bfs,n_bfs,t_bfs))
        results['UCS'].append((p_ucs,n_ucs,t_ucs,c_ucs))
        results['IDS'].append((p_ids,n_ids,t_ids,d_ids))

    header = "Alg | Avg nodes_expanded | Avg time (s) | Avg path_len(edges)"
    lines = [header, "-"*len(header)]
    for alg in ['DFS','BFS','UCS','IDS']:
        runs = results[alg]
        avg_nodes = sum(r[1] for r in runs)/len(runs)
        avg_time = sum(r[2] for r in runs)/len(runs)
        path_lens = []
        for r in runs:
            path = r[0]
            path_lens.append(len(path)-1 if path else float('inf'))
        finite_paths = [p for p in path_lens if p!=float('inf')]
        avg_path_len = sum(finite_paths)/len(finite_paths) if finite_paths else float('inf')
        lines.append(f"{alg:3} | {avg_nodes:17.2f} | {avg_time:11.6f} | {avg_path_len:17.2f} ")

    detail = ["\nDetails per (s,d) pair (showing UCS shortest path cost & path length):"]
    for i,(s,d) in enumerate(pairs):
        p_ucs,n_ucs,t_ucs,c_ucs = results['UCS'][i]
        detail.append(f"Pair {i+1}: {s} -> {d} : UCS cost={c_ucs:.2f}, path_len(edges)={(len(p_ucs)-1) if p_ucs else 'N/A'}")

    return "\n".join(lines), detail


if __name__ == "__main__":
    NUM_NODES = 1000
    AVG_DEGREE = 6
    TRIALS = 3

    print(f"Generating connected weighted graph with n={NUM_NODES}, avg_degree≈{AVG_DEGREE} ...")
    adj = generate_connected_weighted_graph(NUM_NODES, avg_degree=AVG_DEGREE, seed=42)
    print("Checking connectivity... ", "Connected" if is_connected(adj) else "Not connected")

    print("Running algorithms on random pairs...")
    table, details = compare_algorithms_on_graph(adj, trials=TRIALS, seed=123)
    print("\n"+table)
    for line in details:
        print(line)
=======
import random, time, heapq, collections
from typing import List, Tuple, Dict

def generate_connected_weighted_graph(n:int, avg_degree:int=6, min_w=1, max_w=20, seed=None):
    """
    Generates a connected undirected weighted graph as adjacency list.
    - Build a random spanning tree (guarantees connectivity).
    - Add extra edges until average degree ≈ avg_degree.
    Returns adjacency list: {node: [(neighbor, weight), ...]}
    """
    if seed is not None:
        random.seed(seed)
    adj = {i: [] for i in range(n)}

    # spanning tree to ensure graph is connected
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(1, n):
        u = nodes[i]
        v = nodes[random.randint(0, i-1)]
        w = random.randint(min_w, max_w)
        adj[u].append((v,w)); adj[v].append((u,w))

    edges = n-1
    target_edges = max(edges, (n * avg_degree) // 2)
    attempts = 0
    while edges < target_edges and attempts < target_edges * 5:
        a, b = random.randrange(n), random.randrange(n)
        if a == b:
            attempts += 1
            continue
        if any(nb == b for nb,_ in adj[a]):
            attempts += 1
            continue
        w = random.randint(min_w, max_w)
        adj[a].append((b,w)); adj[b].append((a,w))
        edges += 1
    return adj

def is_connected(adj:Dict[int,List[Tuple[int,int]]], start=0)->bool:
    """Check if graph is connected via BFS"""
    n = len(adj)
    seen = {start}
    q = collections.deque([start])
    while q:
        u = q.popleft()
        for v,_ in adj[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    return len(seen) == n


def dfs(adj, start, goal, max_steps=10_000_000):
    t0 = time.perf_counter()
    stack = [(start, [start])]
    visited = set()
    nodes_expanded = 0
    while stack:
        node, path = stack.pop()
        nodes_expanded += 1
        if nodes_expanded > max_steps:
            break
        if node == goal:
            return path, nodes_expanded, time.perf_counter()-t0
        if node in visited:
            continue
        visited.add(node)
        for (nbr,_) in adj[node]:
            if nbr not in visited:
                stack.append((nbr, path+[nbr]))
    return None, nodes_expanded, time.perf_counter()-t0

def bfs(adj, start, goal):
    t0 = time.perf_counter()
    q = collections.deque([(start,[start])])
    visited = {start}
    nodes_expanded = 0
    while q:
        node, path = q.popleft()
        nodes_expanded += 1
        if node == goal:
            return path, nodes_expanded, time.perf_counter()-t0
        for (nbr,_) in adj[node]:
            if nbr not in visited:
                visited.add(nbr)
                q.append((nbr, path+[nbr]))
    return None, nodes_expanded, time.perf_counter()-t0

def ucs(adj, start, goal):
    t0 = time.perf_counter()
    dist = {start: 0}
    parent = {}
    visited = set()
    heap = [(0, start)]
    nodes_expanded = 0
    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited: continue
        visited.add(node); nodes_expanded += 1
        if node == goal:
            path = []
            cur = node
            while cur != start:
                path.append(cur); cur = parent[cur]
            path.append(start); path.reverse()
            return path, nodes_expanded, time.perf_counter()-t0, cost
        for (nbr,w) in adj[node]:
            if nbr in visited: continue
            nc = cost + w
            if nbr not in dist or nc < dist[nbr]:
                dist[nbr] = nc; parent[nbr] = node
                heapq.heappush(heap,(nc,nbr))
    return None, nodes_expanded, time.perf_counter()-t0, float('inf')

def depth_limited_dfs(adj, node, goal, limit, visited_local):
    expanded = 1
    if node == goal: return [node], expanded, False
    if limit == 0: return None, expanded, True
    cutoff_any = False
    for (nbr,_) in adj[node]:
        if nbr in visited_local: continue
        visited_local.add(nbr)
        path,e,cutoff = depth_limited_dfs(adj,nbr,goal,limit-1,visited_local)
        expanded += e
        visited_local.remove(nbr)
        if path is not None:
            return [node]+path, expanded, False
        if cutoff: cutoff_any = True
    return None, expanded, cutoff_any

def ids(adj, start, goal, max_depth=50):
    t0 = time.perf_counter()
    total_expanded = 0
    for depth in range(max_depth+1):
        visited_local = {start}
        path,e,cutoff = depth_limited_dfs(adj,start,goal,depth,visited_local)
        total_expanded += e
        if path is not None:
            return path, total_expanded, time.perf_counter()-t0, depth
        if not cutoff: break
    return None, total_expanded, time.perf_counter()-t0, None


def compare_algorithms_on_graph(adj, trials=5, seed=None):
    if seed is not None:
        random.seed(seed)
    n = len(adj)
    results = {'DFS': [], 'BFS': [], 'UCS': [], 'IDS': []}
    pairs = []
    for _ in range(trials):
        s = random.randrange(n); d = random.randrange(n)
        while d == s: d = random.randrange(n)
        pairs.append((s,d))

    for s,d in pairs:
        p_dfs, n_dfs, t_dfs = dfs(adj,s,d)
        p_bfs, n_bfs, t_bfs = bfs(adj,s,d)
        p_ucs, n_ucs, t_ucs, c_ucs = ucs(adj,s,d)
        p_ids, n_ids, t_ids, d_ids = ids(adj,s,d,max_depth=50)

        results['DFS'].append((p_dfs,n_dfs,t_dfs))
        results['BFS'].append((p_bfs,n_bfs,t_bfs))
        results['UCS'].append((p_ucs,n_ucs,t_ucs,c_ucs))
        results['IDS'].append((p_ids,n_ids,t_ids,d_ids))

    header = "Alg | Avg nodes_expanded | Avg time (s) | Avg path_len(edges)"
    lines = [header, "-"*len(header)]
    for alg in ['DFS','BFS','UCS','IDS']:
        runs = results[alg]
        avg_nodes = sum(r[1] for r in runs)/len(runs)
        avg_time = sum(r[2] for r in runs)/len(runs)
        path_lens = []
        for r in runs:
            path = r[0]
            path_lens.append(len(path)-1 if path else float('inf'))
        finite_paths = [p for p in path_lens if p!=float('inf')]
        avg_path_len = sum(finite_paths)/len(finite_paths) if finite_paths else float('inf')
        lines.append(f"{alg:3} | {avg_nodes:17.2f} | {avg_time:11.6f} | {avg_path_len:17.2f} ")

    detail = ["\nDetails per (s,d) pair (showing UCS shortest path cost & path length):"]
    for i,(s,d) in enumerate(pairs):
        p_ucs,n_ucs,t_ucs,c_ucs = results['UCS'][i]
        detail.append(f"Pair {i+1}: {s} -> {d} : UCS cost={c_ucs:.2f}, path_len(edges)={(len(p_ucs)-1) if p_ucs else 'N/A'}")

    return "\n".join(lines), detail


if __name__ == "__main__":
    NUM_NODES = 1000
    AVG_DEGREE = 6
    TRIALS = 3

    print(f"Generating connected weighted graph with n={NUM_NODES}, avg_degree≈{AVG_DEGREE} ...")
    adj = generate_connected_weighted_graph(NUM_NODES, avg_degree=AVG_DEGREE, seed=42)
    print("Checking connectivity... ", "Connected" if is_connected(adj) else "Not connected")

    print("Running algorithms on random pairs...")
    table, details = compare_algorithms_on_graph(adj, trials=TRIALS, seed=123)
    print("\n"+table)
    for line in details:
        print(line)
>>>>>>> 52317de (Week 6,7,8 added.)
