from collections import deque
import random
def print_states(state):
    for i in range(0,9,3):
        print(state[i:i+3])
    print()
def check_solvability(start):
    inv_count = 0
    for i in range(8):
        for j in range(i+1,9):
            if start[i] != 0 and start[j] != 0 and start[i] > start[j]:
                inv_count += 1
    return inv_count%2==0
def find_neighbours(state):
    neighbours = []
    #blank tile
    index = state.index(0)
    moves = []
    #can move up
    if index not in [0,1,2]:
        moves.append(index-3)
    #can move down
    if index not in [6,7,8]:
        moves.append(index+3)
    #can move left
    if index not in [0,3,6]:
        moves.append(index-1)
    #can move right    
    if index not in [2,5,8]:
        moves.append(index+1)
    for move in moves:
        new_state = state[:]
        new_state[index], new_state[move] = new_state[move], new_state[index]
        neighbours.append(new_state)
    return neighbours
def bfs(start, target):
    visited = set()
    bfsqueue = deque([[start]])
    while bfsqueue:
        path = bfsqueue.popleft()
        state = path[-1]
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))
        if state == target:
            return path
        for neighbour in find_neighbours(state):
            new_path = list(path)
            new_path.append(neighbour)
            bfsqueue.append(new_path)
    return None
def dfs(start, target):
    MAX_CAP = 100
    visited = set()
    stack = [[start]]
    while stack:
        path = stack.pop()
        state = path[-1]
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))
        if state == target:
            return path
        if len(path) >= MAX_CAP:
            continue
        for neighbour in find_neighbours(state):
            new_path = list(path)
            new_path.append(neighbour)
            stack.append(new_path)
    return None
def init_random_initial_state():
    state = list(range(9))
    random.shuffle(state)
    return state

# start_state = [8,1,6,0,3,4,5,7,2]
start_state = init_random_initial_state()
target_state = [0,1,2,3,4,5,6,7,8]
print("\nInitial State:")
print_states(start_state)

print("Target State:")
print_states(target_state)

# bfs attempt
print("BFS Search:")
bfs_result = bfs(start_state, target_state)
if bfs_result:
    for step in bfs_result:
        print_states(step)
    print(f"Solution found in {len(bfs_result)-1} moves:")
else:
    print("No solution found using bfs.")
#dfs attempt
print("DFS Search:")
dfs_result = dfs(start_state, target_state)
if dfs_result:
    for step in dfs_result:
        print_states(step)
    print(f"Solution found in {len(dfs_result)-1} moves:")
else:
    print("No solution found using dfs.")
if check_solvability(start_state):
    print("It is solvable")
else:
    print("It is not solvable")