import heapq
import random
import math
<<<<<<< HEAD
=======
import time
import tracemalloc
>>>>>>> 52317de (Week 6,7,8 added.)

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
    return inv_count % 2 == 0

def find_neighbours(state):
    neighbours = []
    index = state.index(0)
    moves = []
    if index not in [0,1,2]:
        moves.append(index-3)
    if index not in [6,7,8]:
        moves.append(index+3)
    if index not in [0,3,6]:
        moves.append(index-1)
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
        if state[i] != i and state[i] != 0:
            numMisplaced += 1
    return numMisplaced
<<<<<<< HEAD
=======
def manhattanHeuristic(state):
    dist = 0
    for i in range(1,9):
        idx = state.index(i)
        correct_idx = i
        x1, y1 = divmod(idx, 3)
        x2, y2 = divmod(correct_idx, 3)
        dist += abs(x1 - x2) + abs(y1 - y2)
    return dist

>>>>>>> 52317de (Week 6,7,8 added.)

# A* 
def AStar(start, target):
    openlist = []
    heapq.heappush(openlist, (manhattanHeuristic(start), 0, start, [start]))
    closedset = set()
    while openlist:
        f, g, state, path = heapq.heappop(openlist)
        state_tuple = tuple(state)
        if state_tuple in closedset:
            continue
        closedset.add(state_tuple)
        if state == target:
            return path
        for neighbour in find_neighbours(state):
            neighbour_tuple = tuple(neighbour)
            if neighbour_tuple not in closedset:
                new_g = g + 1
                new_h = manhattanHeuristic(neighbour)
                new_f = new_g + new_h
                heapq.heappush(openlist, (new_f, new_g, neighbour, path + [neighbour]))
    return None


<<<<<<< HEAD
def manhattanHeuristic(state):
    dist = 0
    for i in range(1,9):
        idx = state.index(i)
        correct_idx = i
        x1, y1 = divmod(idx, 3)
        x2, y2 = divmod(correct_idx, 3)
        dist += abs(x1 - x2) + abs(y1 - y2)
    return dist
=======
>>>>>>> 52317de (Week 6,7,8 added.)

# RBFS

def RBFS(start, target):
    def rbfs(node, f_limit):
        state, path, g = node
        f = g + manhattanHeuristic(state)

        if state == target:
            return path, True, f

        successors = []
        for neighbour in find_neighbours(state):
            if neighbour not in path:
                new_g = g + 1
                f_val = max(new_g + manhattanHeuristic(neighbour), f)  
                successors.append((neighbour, path + [neighbour], new_g, f_val))

        if not successors:
            return None, False, math.inf

        while True:

            successors.sort(key=lambda x: x[3])
            best = successors[0]

            # If best exceeds f_limit, fail
            if best[3] > f_limit:
                return None, False, best[3]

            # Alternative f (2nd best)
            alternative = successors[1][3] if len(successors) > 1 else math.inf

            # Recursive call on best
            result, found, new_f = rbfs((best[0], best[1], best[2]), min(f_limit, alternative))

            # Update f-value of best after recursion
            successors[0] = (best[0], best[1], best[2], new_f)

            if found:
                return result, True, new_f

    # Start RBFS
    path, found, _ = rbfs((start, [start], 0), math.inf)
    return path if found else None

def init_random_initial_state():
    state = list(range(9))
    random.shuffle(state)
    return state

# Use either a fixed start or a random one
start_state = init_random_initial_state()
target_state = [0,1,2,3,4,5,6,7,8]
print("\nInitial State:")
print_states(start_state)
print("Target State:")
print_states(target_state)

if check_solvability(start_state):
    # A* attempt
    print("A* Search:")
<<<<<<< HEAD
    a_star_result = AStar(start_state, target_state)
=======
    a_start_time = time.time()
    a_star_result = AStar(start_state, target_state)
    astartime = time.time() - a_start_time
>>>>>>> 52317de (Week 6,7,8 added.)
    if a_star_result:
        for step in a_star_result:
            print_states(step)
        print(f"Solution found in {len(a_star_result)-1} moves:")
<<<<<<< HEAD
=======
        print(f"Time taken : {astartime:.8f} s.")
>>>>>>> 52317de (Week 6,7,8 added.)
    else:
        print("No solution found using A*.")

    # RBFS attempt
    print("RBFS Search:")
<<<<<<< HEAD
    rbfs_result = RBFS(start_state, target_state)
=======
    rbfs_start_time = time.time()
    rbfs_result = RBFS(start_state, target_state)
    rbfs_time = time.time() - rbfs_start_time
>>>>>>> 52317de (Week 6,7,8 added.)
    if rbfs_result:
        for step in rbfs_result:
            print_states(step)
        print(f"Solution found in {len(rbfs_result)-1} moves:")
<<<<<<< HEAD
=======
        print(f"Time taken : {rbfs_time:.8f} s.")

>>>>>>> 52317de (Week 6,7,8 added.)
    else:
        print("No solution found using RBFS.")
    print("It is solvable")
else:
    print("It is not solvable")
