#Solve 8 puzzle using A* search and RBFS.
import heapq
import random
import math
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

def misplacedTilesHeuristic(state):
    numMisplaced = 0
    for i in range(len(state)):
        if state[i] !=  i:
            numMisplaced += 1
    return numMisplaced

def AStar(start,target):
    openlist = []
    heapq.heappush(openlist, (0 + misplacedTilesHeuristic(start), 0, start, [start]))  
    closedset = set()
    while openlist:
        f, g, state, path = heapq.heappop(openlist)
        if tuple(state) in closedset:
            continue
        closedset.add(tuple(state))
        if state == target:
            return path  
        for neighbour in find_neighbours(state):
            if tuple(neighbour) not in closedset:
                new_g = g + 1
                new_h = misplacedTilesHeuristic(neighbour)
                new_f = new_g + new_h
                heapq.heappush(openlist, (new_f, new_g, neighbour, path + [neighbour]))
    return None    

def RBFS(start, target):
    def rbfs(node, f_limit):
        state, path, g = node
        f = g + misplacedTilesHeuristic(state)
        if state == target:
            return path, True, 0
        successors = []
        for neighbour in find_neighbours(state):
            if neighbour not in path:
                new_g = g + 1
                f_val = max(new_g + misplacedTilesHeuristic(neighbour), f)
                successors.append((neighbour, path + [neighbour], new_g, f_val))
        if not successors:
            return None, False, math.inf
        while True:
            successors.sort(key=lambda x: x[3])  
            best = successors[0]
            if best[3] > f_limit:
                return None, False, best[3]
            alternative = successors[1][3] if len(successors) > 1 else math.inf
            result, found, new_f = rbfs((best[0], best[1], best[2]), min(f_limit, alternative))
            best[3] = new_f
            if found:
                return result, True, 0


    path, found, _ = rbfs((start, [start], 0), math.inf)
    return path if found else None

def init_random_initial_state():
    state = list(range(9))
    random.shuffle(state)
    return state

# start_state = [7,2,4,5,0,6,8,3,1]
start_state = init_random_initial_state()
target_state = [0,1,2,3,4,5,6,7,8]
print("\nInitial State:")
print_states(start_state)

print("Target State:")
print_states(target_state)

# A* attempt
print("A* Search:")
a_star_result = AStar(start_state, target_state)
if a_star_result:
    for step in a_star_result:
        print_states(step)
    print(f"Solution found in {len(a_star_result)-1} moves:")
else:
    print("No solution found using A*.")
# rbfs attempt
print("RBFS Search:")
rbfs_result = RBFS(start_state, target_state)
if rbfs_result:
    for step in rbfs_result:
        print_states(step)
    print(f"Solution found in {len(rbfs_result)-1} moves:")
else:
    print("No solution found using dfs.")
if check_solvability(start_state):
    print("It is solvable")
else:
    print("It is not solvable")